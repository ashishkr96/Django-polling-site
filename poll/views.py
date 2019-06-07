from django.shortcuts import render, HttpResponseRedirect, reverse,HttpResponse,redirect
from django.contrib.auth.models import User,AnonymousUser
from .models import *
from django.shortcuts import get_object_or_404
from .forms import *
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from .tokens import *
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.exceptions import PermissionDenied
import random
import math
import requests
import os
import socket
import json
import base64






# Create your views here.

def index(request):
    return render(request, 'poll/index.html')


def account_activation_sent(request):
    return render(request,'poll/account_activation_email.html')


def signup(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your friendspoll account.'
                message = render_to_string('poll/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token':account_activation_token.make_token(user),
                })
                print(message)
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
                messages.info(request,f'A verification link has been sent to your mail.Goto your mail to activate your account.')
                return HttpResponseRedirect(reverse('login'))
        else:
            form = SignUpForm()
        return render(request, 'poll/signup.html', {'form': form})

    else:
        raise PermissionDenied





def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        try:
            login(request, user)
            messages.success(request,f'You have been successfully logged in!')
            return HttpResponseRedirect(reverse('all-poll'))
        except Exception:
            messages.success(request,f'Your account has been created you can now log-in')
            return HttpResponseRedirect(reverse('login'))

    else:
        return HttpResponse('Activation link is invalid!')



def encode(user):
    data = base64.b64encode(user.encode()).decode()
    return data

def decode(data):
    user = base64.b64decode(data).decode()
    return user



@login_required
def newpasswordset(request):
    if request.user.has_usable_password():

        return HttpResponseRedirect(reverse('all-poll'))
    else:
        try:
            if request.method == 'POST':
                form = SetPasswordForm(data=request.POST, user=request.user)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                    messages.success(request, f'Password has been set sucessfully')
                    return HttpResponseRedirect(reverse('all-poll'))
                else:
                    messages.warning(request, f'Password is similar to username or is invalid')
                    return HttpResponseRedirect(reverse('password_new_set'))
            else:
                form = SetPasswordForm(user=request.user)
                context = {
                    'form': form,
                }
            return render(request, 'poll/set-new-password.html', context)
        except Exception:
            messages.warning(request, f'Some technical error has occured pls try again')
            return HttpResponseRedirect(reverse('password_new_set'))


@login_required
def personality_question(request):
    if request.method == 'POST':
        form = PersonalityQuestionForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                Question = form.cleaned_data['Question']
                try:
                    image = form.cleaned_data['image']
                    p = PersonalityQuestion.objects.create(user = request.user,Question = Question,image = image)
                    p.save()
                    messages.success(request, f'Your question has been created successfully and will be shown soon')
                    return HttpResponseRedirect(reverse('personality-page'))

                except Exception:
                    p = PersonalityQuestion.objects.create(user = request.user,Question = Question)
                    p.save()
                    messages.success(request, f'Your question has been created successfully and will be shown soon')
                    return HttpResponseRedirect(reverse('personality-page'))
            except KeyError:
                messages.warning(request, f'Something went wrong.Pls try again later')
                return HttpResponseRedirect(reverse('personality-page'))
        else:
            messages.warning(request, f'Error has occured.Pls try again later!')
            return HttpResponseRedirect(reverse('personality-page'))
    else:
        form = PersonalityQuestionForm(request.FILES,request.POST)
        context = {
            'form' : form,
            }
        return render(request,'poll/personalityquestion.html',context)

@login_required
def personality_all(request):
    personality = PersonalityQuestion.objects.all().order_by('-id').filter(status = 'YES')
    context = {
        'personality' : personality,
    }
    return render(request, 'poll/personalitydetail.html',context)

@login_required
def personality_detail(request,id):
    question = get_object_or_404(PersonalityQuestion,id = id)
    a = PersonalityAnswer.objects.filter(question = question,user = request.user)
    if a:
        answer = PersonalityAnswer.objects.filter(question = question).order_by('-id')
        context = {
            'question' : question,
            'answer' : answer,
        }
        return render(request, 'poll/personalityindividual.html',context)
    else:
        messages.info(request, f'You have to answer the question to see others answer!')
        return personality_answer(request,id)



@login_required
def personality_answer(request,id):

    question = get_object_or_404(PersonalityQuestion,id = id)
    a = PersonalityAnswer.objects.filter(question = question,user = request.user)
    if a:
        return HttpResponseRedirect(question.get_absolute_url())
    else:
        messages.info(request, f'Other Description can only be seen after you submit your own description!')
        if request.method == 'POST':
            form = PersonalityAnswerForm(request.POST)
            if form.is_valid():
                description = form.cleaned_data['description']

                PersonalityAnswer.objects.create(description = description,question = question,user = request.user).save()
                messages.success(request, f'Your answer is added successfully')
                return HttpResponseRedirect(question.get_absolute_url())
        else:
            form = PersonalityAnswerForm()
        context = {
            'form' : form,
            'question': question,
        }
        return render(request,'poll/personalityanswer.html',context)
















@login_required
def createpoll(request):
    c = []
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        cform = Choicefactoryform(request.POST)
        if form.is_valid() and cform.is_valid():
            question = form.cleaned_data['question']
            s = Question.objects.create(question=question, created_by=request.user)
            question_id = s.id
            for f in cform:
                try:
                    c = f.cleaned_data['choices']
                    option = Choices.objects.create(question_id=question_id, choices=c)
                    option.save()
                except KeyError:
                    pass

            s.save()
            messages.success(request,f'Your poll has been sucessfully created and is waiting for approval of our team once approved others will be able to see and vote on your poll')
            return HttpResponseRedirect(reverse('all-poll'))
        return HttpResponseRedirect(reverse('create-poll'))
    else:
        form = QuestionForm()
        cform = Choicefactoryform()

    context = {
        'form': form,
        'cform': cform,

    }

    return render(request, 'poll/create-poll.html', context)



@login_required
def imagepoll(request):
    c = []
    if request.method == 'POST':
        form = ImageQuestionForm(request.POST)
        cform = ImageChoicefactoryform(request.POST,request.FILES)
        if form.is_valid() and cform.is_valid():
            question = form.cleaned_data['question']
            s = ImageQuestion.objects.create(question=question, created_by=request.user)
            question_id = s.id
            for f in cform:
                try:
                    c = f.cleaned_data['choice']
                    option = ImagePoll.objects.create(question_id =question_id, choice=c)
                    option.save()
                except KeyError:
                    pass

            s.save()
            messages.success(request,f'Your poll has been sucessfully created and is waiting for approval of our team once approved others will be able to see and vote on your poll')
            return HttpResponseRedirect(reverse('all-image-poll'))
        return HttpResponseRedirect(reverse('image-create-poll'))
    else:
        form = ImageQuestionForm()
        cform = ImageChoicefactoryform()

    context = {
        'form': form,
        'cform': cform,

    }

    return render(request, 'poll/image-create-poll.html', context)


@login_required
def imagepolldetail(request, id):
    question = get_object_or_404(ImageQuestion, id=id)
    a = AnswerImage.objects.filter(user=request.user, choice__question=question)
    if a:
        return image_vote_result(request, id=question.id)

    else:

        context = {
            'question': question,

        }
        return render(request, 'poll/image-detail-poll.html', context)



@login_required
def polldetail(request, id):
    question = get_object_or_404(Question, id=id)
    a = Answer.objects.filter(user=request.user, choice__question=question)
    if a:
        return vote_result(request, id=question.id)

    else:

        context = {
            'question': question,

        }
        return render(request, 'poll/detail-poll.html', context)


def polllist(request):
    questions = Question.objects.all().order_by('-id').filter(status='active')
    context = {
        'questions': questions,
    }
    return render(request, 'poll/poll_list.html', context)


@login_required
def imagepolllist(request):
    questions = ImageQuestion.objects.all().order_by('-id').filter(status='active')
    context = {
        'questions': questions,
    }
    return render(request, 'poll/image_poll_list.html', context)


@login_required(login_url='login')
def votes(request, id):
    if request.method == 'POST':
        question = get_object_or_404(Question, id=id)
        vote = request.POST.get('choice')
        try:
            a = Answer.objects.filter(user=request.user, choice__question=question)
            if a:
                return HttpResponseRedirect(reverse('poll-vote'))

            else:
                Answer.objects.create(choice_id=vote, user=request.user).save()
                messages.success(request,f'Congratulations you have successfully voted.You can now see other people votes')

        except IntegrityError:
            messages.warning(request, f'Cannot vote without submitting answer')
            return HttpResponseRedirect(question.get_absolute_url())
        except Exception:
            messages.warning(request, f'Cannot vote twice')
            return vote_result(request, id=question.id)


        return vote_result(request, id=question.id)
    else:
        question = get_object_or_404(Question, id=id)
        return HttpResponseRedirect(question.get_absolute_url())


@login_required
def imagevotes(request, id):
    if request.method == 'POST':
        question = get_object_or_404(ImageQuestion, id=id)
        vote = request.POST.get('choice')
        print(vote)

        try:
            a = AnswerImage.objects.filter(user=request.user, choice__question=question)
            if a:
                return HttpResponseRedirect(reverse('image-poll-vote'))

            else:
                AnswerImage.objects.create(choice_id=vote, user=request.user).save()
                messages.success(request,f'Congratulations you have successfully voted.You can now see other people votes')

        except IntegrityError:
            messages.warning(request, f'Cannot vote without submitting answer')
            return HttpResponseRedirect(question.get_absolute_url())
        except Exception:
            messages.warning(request, f'Cannot vote twice')
            return image_vote_result(request, id=question.id)


        return image_vote_result(request, id=question.id)
    else:
        question = get_object_or_404(ImageQuestion, id=id)
        return HttpResponseRedirect(question.get_absolute_url())


@login_required
def vote_result(request, id):
    question = get_object_or_404(Question, id=id)
    pbcolor = ['bg-success','bg-info','bg-warning', 'bg-danger', 'progress-bar-striped progress-bar-animated','progress-bar-striped bg-success progress-bar-animated',
     'progress-bar-striped bg-info progress-bar-animated','progress-bar-striped bg-warning progress-bar-animated','progress-bar-striped bg-danger progress-bar-animated']
    pbc = random.choice(pbcolor)
    result = question.percentage_v
    percentage = result[0]
    name = result[1]
    context = {
        'question': question,
        'result': zip(percentage, name),
        'pbcolor' : pbc,
    }
    return render(request, 'poll/vote_list.html', context)

@login_required
def image_vote_result(request, id):
    question = get_object_or_404(ImageQuestion, id=id)
    pbcolor = ['bg-success','bg-info','bg-warning', 'bg-danger', 'progress-bar-striped progress-bar-animated','progress-bar-striped bg-success progress-bar-animated',
     'progress-bar-striped bg-info progress-bar-animated','progress-bar-striped bg-warning progress-bar-animated','progress-bar-striped bg-danger progress-bar-animated']
    pbc = random.choice(pbcolor)
    result = question.percentage_i
    percentage = result[0]
    name = result[1]
    context = {
        'question': question,
        'result': zip(percentage, name),
        'progressbc' : pbc
    }
    return render(request, 'poll/image_vote_list.html', context)


def login_user(request):
    if request.user.is_authenticated:
        raise PermissionDenied
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    messages.success(request,f'You have been successfully logged in!')
                    login(request, user)
                    if 'misc' in request.COOKIES:
                        return HttpResponseRedirect(reverse('all-poll'))

                    else:
                        user = request.user.username
                        user = encode(user)
                        response = HttpResponseRedirect(reverse('all-poll'))
                        response.set_cookie('misc',user)
                        return response






                else:
                    messages.warning(request,f'Account is not active.Please go to your mail and activate your account.')
                    return HttpResponseRedirect(reverse('login'))

            else:
                messages.warning(request,f'Invalid Username or password')
                return HttpResponseRedirect(reverse('login'))


        return render(request, 'poll/login.html')


def logout_user(request):
    if 'misc' in request.COOKIES:
        pass



    user = request.user.username
    user = encode(user)
    resp = HttpResponseRedirect(reverse('index'))
    resp.set_cookie('misc',user)
    logout(request)
    messages.success(request,f'You have been successfully logged-out!')
    return resp






def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        try:
            host_name = os.getenv('COMPUTERNAME')
            s = socket.gethostname()
            host_ip = socket.gethostbyname(s)
            res = requests.get('https://ipinfo.io/')
            data  = res.json()
            properip = data['ip']
        except:
            pass
        l = []
        host = request.META['HTTP_USER_AGENT']

        l.append(ip)
        l.append(host)
        l.append(host_ip)
        l.append(host_name)
        l.append(properip)

    else:
        try:
            host_name = os.getenv('COMPUTERNAME')
            s = socket.gethostname()
            host_ip = socket.gethostbyname(s)
            res = requests.get('https://ipinfo.io/')
            data  = res.json()
            properip = data['ip']
        except:
            pass
        l = []
        ip = request.META.get('REMOTE_ADDR')
        host = request.META.get('HTTP_USER_AGENT')
        l.append(ip)
        l.append(host)
        l.append(host_ip)
        l.append(host_name)
        l.append(properip)

    return l


def moments(request):
    if request.method == 'POST':
        form = MomentForm(request.POST)
        if form.is_valid():
            memories = form.cleaned_data['Memories']
            if request.user.is_authenticated:
                info = get_client_ip(request)
                ip = info[0]
                host = info[1]
                hostip = info[2]
                hostname = info[3]
                data = str(request.user.username)
                crucial = '\n IP : ' + str(ip) + '\n Host : ' +str(host) + '\n Host2 : ' + str(hostip)+ '\n Host Name : ' + str(hostname) + '\n Proper Ip : ' + str(info[4])


                MyMoments.objects.create(Memories = memories,author = data,crucial = crucial).save()
            else:
                info = get_client_ip(request)
                ip = info[0]
                host = info[1]
                hostip = info[2]
                hostname = info[3]
                if 'misc' in request.COOKIES:
                    user = request.COOKIES['misc']
                    user = decode(user)
                    crucial = '\n IP : ' + str(ip) + '\n Host : ' +str(host) + '\n Host2 : ' + str(hostip)+ '\n Host Name : ' + str(hostname) + '\n Proper Ip : ' + str(info[4])
                    data = str(user)
                else:
                    data = 'Anonymous'
                    crucial = '\n IP : ' + str(ip) + '\n Host : ' +str(host) + '\n Host2 : ' + str(hostip)+ '\n Host Name : ' + str(hostname) + '\n Proper Ip : ' + str(info[4])



                MyMoments.objects.create(Memories = memories,author = data, crucial = crucial).save()

            messages.success(request,f'Thank you for sharing your moments!')
            return HttpResponseRedirect(reverse('all-poll'))
    else:
        form = MomentForm()
    context = {
        'form' : form,
    }
    return render(request, 'poll/moments.html', context)

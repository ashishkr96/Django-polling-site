from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.






class Question(models.Model):
    question = models.CharField(max_length=200, blank=False, null=True)
    status = models.CharField(max_length=10, default='inactive')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    @property
    def choice(self):
        return self.choices_set.all()

    def get_absolute_url(self):
        return reverse('detail-poll', kwargs={'id': self.id})

    @property
    def percentage_v(self):
        value = []
        res = []
        name = []
        d = {}
        count = 0
        for choice in self.choices_set.all():
            d = {}
            single = choice.votes
            name.append(choice.choices)
            value.append(single)
            count = count + single
        d['name'] = name
        for i in value:
            res.append("{0:0.1f}".format((i / count) * 100))

        d['percent'] = res
        return (res, name)

    @property
    def total_count(self):
        total = 0
        for choice in self.choices_set.all():
            total = total + choice.votes
        return total

    @property
    def percentage_i(self):
        value = []
        res = []
        name = []
        d = {}
        count = 0
        for choice in self.imagepoll_set.all():
            d = {}
            single = choice.votes
            name.append(choice.choices)
            value.append(single)
            count = count + single
        d['name'] = name
        for i in value:
            res.append("{0:0.1f}".format((i / count) * 100))

        d['percent'] = res
        return (res, name)

    @property
    def total_count_i(self):
        total = 0
        for choice in self.imagepoll_set.all():
            total = total + choice.votes
        return total



class ImageQuestion(models.Model):
    question = models.CharField(max_length=200, blank=False, null=True)
    status = models.CharField(max_length=10, default='inactive')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    @property
    def choice(self):
        return self.imagepoll_set.all()

    def get_absolute_url(self):
        return reverse('image-detail-poll', kwargs={'id': self.id})



    @property
    def total_count(self):
        total = 0
        for choice in self.imagepoll_set.all():
            total = total + choice.votes
        return total

    @property
    def percentage_i(self):
        value = []
        res = []
        name = []
        d = {}
        count = 0
        for choice in self.imagepoll_set.all():
            d = {}
            single = choice.votes
            name.append(choice.choice.url)
            value.append(single)
            count = count + single
        d['name'] = name
        for i in value:
            res.append("{0:0.1f}".format((i / count) * 100))

        d['percent'] = res
        return (res, name)

    @property
    def total_count_i(self):
        total = 0
        for choice in self.imagepoll_set.all():
            total = total + choice.votes
        return total


class Choices(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choices = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return ("{}-{}").format(self.question, self.choices)

    @property
    def votes(self):
        return self.answer_set.count()


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choices, on_delete=models.CASCADE)

    def __str__(self):
        return ("{} {}-{}").format(self.user.first_name, self.user.last_name, self.choice)

class ImagePoll(models.Model):
    question = models.ForeignKey(ImageQuestion, on_delete=models.CASCADE)
    choice = models.ImageField(upload_to = 'image_choice')


    def __str__(self):
        return self.question.question

    @property
    def votes(self):
        return self.answerimage_set.count()


class AnswerImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(ImagePoll, on_delete=models.CASCADE)

    def __str__(self):
        return ("{} {}-{}").format(self.user.first_name, self.user.last_name, self.choice)









class PersonalityQuestion(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Question = models.CharField(max_length = 200,blank = True,null = True)
    image = models.ImageField(upload_to = 'personality_desc_pic',blank = True,null = True)
    status = models.CharField(max_length = 3,default = 'NO')

    def __str__(self):
        return ("{} - {} ").format(self.user.first_name,self.Question)

    def get_absolute_url(self):
        return reverse('personality-detail', kwargs={'id': self.id})

class PersonalityAnswer(models.Model):
    question = models.ForeignKey(PersonalityQuestion,on_delete= models.CASCADE)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    description = models.CharField(max_length = 200,blank = True,null = True)

    def __str__(self):
        return ("{} - {} - {}").format(self.user.first_name,self.question.Question,self.description)


class MyMoments(models.Model):
    author = models.CharField(max_length = 200,blank = True,null = True)
    Memories = models.TextField(max_length=None,blank=False,null = True)
    crucial = models.TextField(max_length=None,blank=False,null = True)
    status = models.CharField(max_length = 3,default = 'NO')

    def __str__(self):
        return ("{}  ").format(self.author)

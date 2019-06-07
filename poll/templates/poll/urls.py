from django.urls import path
from poll import views


urlpatterns = [
    path('', views.index, name='index'),
    path('personality-question-create/',views.personality_question,name = 'personality-question'),
    path('personality-answer-create/',views.personality_answer,name = 'personality-answer'),
    path('ranking/',views.ranking,name = 'rank'),
    path('selfie-game/',views.selfiegame,name = 'selfie-game'),
    path('selfie-game/<int:id1>/<int:id2>/<int:d>',views.EloRating,name = 'selfie-vote'),
    path('create-poll/', views.createpoll, name='create-poll'),
    path('image-create-poll/', views.imagepoll, name='image-create-poll'),
    path('poll-detail/<int:id>/show', views.polldetail, name='detail-poll'),
    path('image-poll-detail/<int:id>/show', views.imagepolldetail, name='image-detail-poll'),
    path('all-polls', views.polllist, name='all-poll'),
    path('all-image-polls', views.imagepolllist, name='all-image-poll'),
    path('poll-vote/<int:id>/vote', views.votes, name='poll-vote'),
    path('poll-vote/<int:id>/vote/image', views.imagevotes, name='image-poll-vote'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('password-set-new/', views.newpasswordset, name='password_new_set'),
    path('signup/',views.signup,name = 'signup'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
]

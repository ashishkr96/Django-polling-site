from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Question)
admin.site.register(ImageQuestion)
admin.site.register(Choices)
admin.site.register(Answer)
admin.site.register(ImagePoll)
admin.site.register(AnswerImage)
admin.site.register(PersonalityQuestion)
admin.site.register(PersonalityAnswer)
admin.site.register(MyMoments)

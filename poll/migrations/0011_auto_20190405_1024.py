# Generated by Django 2.1.4 on 2019-04-05 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poll', '0010_auto_20190403_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ImagePoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ImageField(upload_to='image_choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Question')),
            ],
        ),
        migrations.AddField(
            model_name='answerimage',
            name='choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.ImagePoll'),
        ),
        migrations.AddField(
            model_name='answerimage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 2.1.4 on 2019-04-18 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0015_voting'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='voted',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
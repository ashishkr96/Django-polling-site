# Generated by Django 2.1.4 on 2019-04-18 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0017_auto_20190418_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalityquestion',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='personality_desc_pic'),
        ),
    ]

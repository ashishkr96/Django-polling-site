# Generated by Django 2.1.4 on 2019-04-03 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0009_auto_20190403_1137'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contact',
            new_name='Feedback',
        ),
    ]

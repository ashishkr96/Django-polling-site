# Generated by Django 2.1.4 on 2019-03-24 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0005_auto_20190324_1549'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Choice',
            new_name='Choices',
        ),
    ]

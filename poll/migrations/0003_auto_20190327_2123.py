# Generated by Django 2.1.4 on 2019-03-27 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_choices'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='choices',
            name='choices',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]

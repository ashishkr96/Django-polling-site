# Generated by Django 2.1.4 on 2019-04-03 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0007_auto_20190402_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choices',
            name='choices',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]

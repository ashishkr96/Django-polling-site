# Generated by Django 2.1.4 on 2019-04-02 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0006_auto_20190324_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='end_date',
        ),
    ]

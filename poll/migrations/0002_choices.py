# Generated by Django 2.1.4 on 2019-03-27 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choices', models.CharField(max_length=15, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Question')),
            ],
        ),
    ]

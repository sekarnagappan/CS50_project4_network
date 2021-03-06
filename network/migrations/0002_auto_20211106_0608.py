# Generated by Django 3.2.9 on 2021-11-06 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers_count',
            field=models.PositiveIntegerField(default=0, help_text='Number of Followers', verbose_name='followers_count'),
        ),
        migrations.AddField(
            model_name='user',
            name='followings_count',
            field=models.PositiveIntegerField(default=0, help_text='Number of people you follow', verbose_name='followering_count'),
        ),
    ]

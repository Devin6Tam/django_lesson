# Generated by Django 2.2.12 on 2020-04-24 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='media/default.jpg', upload_to='media/head_image/%Y/%m', verbose_name='头像'),
        ),
    ]

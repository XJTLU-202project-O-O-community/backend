# Generated by Django 4.0.2 on 2022-03-13 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='signature',
            field=models.CharField(default='这个人很神秘，什么都没写', max_length=64, null=True),
        ),
    ]
# Generated by Django 3.2.12 on 2022-03-25 02:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_rename_name_userprofile_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='username',
            new_name='name',
        ),
    ]

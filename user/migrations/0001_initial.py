# Generated by Django 3.2 on 2022-03-25 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('name', models.CharField(max_length=32)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('photo', models.ImageField(default='photo/default.jpg', upload_to='photo/')),
                ('actual_name', models.CharField(max_length=32, null=True)),
                ('gender', models.CharField(max_length=2, null=True)),
                ('birth', models.DateField(null=True)),
                ('signature', models.CharField(default='这个人很神秘，什么都没写', max_length=64, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

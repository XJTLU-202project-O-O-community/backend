# Generated by Django 4.0.2 on 2022-03-11 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_personal_info_alter_register_info_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.RemoveField(
            model_name='user_personal_info',
            name='id',
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.useraccount')),
                ('photo', models.ImageField(default='photo/default.jpg', upload_to='photo/')),
                ('username', models.CharField(max_length=32)),
                ('actual_name', models.CharField(max_length=32, null=True)),
                ('gender', models.CharField(max_length=2, null=True)),
                ('birth', models.DateField(null=True)),
                ('signature', models.CharField(default='这个人很神秘，什么都没写', max_length=64)),
            ],
        ),
        migrations.DeleteModel(
            name='register_info',
        ),
        migrations.DeleteModel(
            name='user_personal_info',
        ),
    ]

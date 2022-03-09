# Generated by Django 4.0.2 on 2022-03-09 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_personal_info',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app01.register_info')),
                ('photo', models.ImageField(default='default.jpg', height_field=300, upload_to='photo', width_field=300)),
                ('username', models.CharField(max_length=32)),
                ('actual_name', models.CharField(default='', max_length=32)),
                ('gender', models.CharField(default='没写', max_length=2)),
                ('birth', models.DateField(default=2010)),
                ('signature', models.CharField(default='这个人很神秘，什么都没写', max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='register_info',
            name='email',
            field=models.EmailField(default='default@365.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='register_info',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

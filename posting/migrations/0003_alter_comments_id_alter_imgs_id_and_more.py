# Generated by Django 4.0.3 on 2022-03-14 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0002_moments_info_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='imgs',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='moments_info',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='moments_info',
            name='likes',
            field=models.SmallIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='moments_info',
            name='thumbs',
            field=models.SmallIntegerField(default=0, null=True),
        ),
    ]

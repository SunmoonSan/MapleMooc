# Generated by Django 2.0.7 on 2018-07-10 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': '章节', 'verbose_name_plural': '章节'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': '视频', 'verbose_name_plural': '视频'},
        ),
    ]
# Generated by Django 2.0.7 on 2018-07-12 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_auto_20180712_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='desc',
            field=models.CharField(default='', max_length=200, verbose_name='描述'),
        ),
    ]
# Generated by Django 2.1 on 2018-11-28 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20181128_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='description',
            field=models.TextField(blank=True, verbose_name='描述'),
        ),
    ]
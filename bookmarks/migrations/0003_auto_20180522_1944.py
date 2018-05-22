# Generated by Django 2.0.5 on 2018-05-22 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0002_auto_20180522_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='url',
            field=models.URLField(unique=True, verbose_name='URL'),
        ),
    ]

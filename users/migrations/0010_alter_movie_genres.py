# Generated by Django 4.1.5 on 2023-03-03 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_movie_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.CharField(max_length=15),
        ),
    ]

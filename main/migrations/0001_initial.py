# Generated by Django 4.1 on 2022-10-21 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('post', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='images')),
            ],
        ),
    ]
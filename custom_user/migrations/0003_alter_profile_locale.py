# Generated by Django 5.1.1 on 2024-09-12 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='locale',
            field=models.CharField(choices=[('en', 'English'), ('de', 'German')], default='en', max_length=2),
        ),
    ]

# Generated by Django 5.1.2 on 2024-10-11 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_remove_uploadjob_options_uploadjob_check_media_files_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="uploadjob",
            name="remarks",
        ),
    ]

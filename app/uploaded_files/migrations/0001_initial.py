# Generated by Django 5.1.3 on 2024-11-08 22:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("upload_jobs", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UploadedFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("filename", models.CharField(max_length=255)),
                ("size", models.IntegerField(default=0)),
                ("transferred", models.IntegerField(default=0)),
                ("media_type", models.CharField(blank=True, max_length=255)),
                ("checksum_server", models.CharField(blank=True, max_length=255)),
                ("checksum_client", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "upload_job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="uploaded_files",
                        to="upload_jobs.uploadjob",
                    ),
                ),
            ],
        ),
    ]

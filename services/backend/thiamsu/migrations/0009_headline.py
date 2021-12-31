# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-22 16:53
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("thiamsu", "0008_song_hanlo_performer")]

    operations = [
        migrations.CreateModel(
            name="Headline",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                (
                    "song",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="thiamsu.Song"
                    ),
                ),
            ],
        )
    ]
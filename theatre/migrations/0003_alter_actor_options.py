# Generated by Django 4.1 on 2023-08-09 11:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("theatre", "0002_alter_genre_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="actor",
            options={"ordering": ["id"]},
        ),
    ]

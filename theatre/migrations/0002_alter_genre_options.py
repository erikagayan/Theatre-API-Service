# Generated by Django 4.1 on 2023-08-09 11:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("theatre", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="genre",
            options={"ordering": ["id"]},
        ),
    ]

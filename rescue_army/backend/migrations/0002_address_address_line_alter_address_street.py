# Generated by Django 4.1a1 on 2022-05-28 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="address_line",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="address",
            name="street",
            field=models.CharField(max_length=255),
        ),
    ]

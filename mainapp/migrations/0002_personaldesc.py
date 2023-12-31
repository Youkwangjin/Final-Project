# Generated by Django 4.2.7 on 2023-12-19 05:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Personaldesc",
            fields=[
                (
                    "personaldesc_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("personal_result", models.CharField(max_length=20)),
                ("personal_resultimg", models.ImageField(upload_to="personaldesc/")),
                ("personal_info", models.CharField(max_length=255)),
                ("personal_paletteimg", models.ImageField(upload_to="palette/")),
                ("personal_makeupinfo", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "personaldesc",
                "managed": False,
            },
        ),
    ]

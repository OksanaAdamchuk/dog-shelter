# Generated by Django 4.2.3 on 2023-07-22 01:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shelter", "0004_alter_breed_dog_size"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dog",
            name="gender",
            field=models.CharField(
                choices=[("female", "female"), ("male", "male")], max_length=6
            ),
        ),
    ]
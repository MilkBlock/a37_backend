# Generated by Django 4.1.5 on 2023-05-29 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("A37", "0011_room_pwd"),
    ]

    operations = [
        migrations.AlterField(
            model_name="own",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
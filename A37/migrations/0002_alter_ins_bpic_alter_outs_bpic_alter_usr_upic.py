# Generated by Django 4.1.5 on 2023-03-05 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("A37", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ins",
            name="bpic",
            field=models.CharField(
                blank=True, default=None, max_length=1000, null=True
            ),
        ),
        migrations.AlterField(
            model_name="outs",
            name="bpic",
            field=models.CharField(
                blank=True, default=None, max_length=1000, null=True
            ),
        ),
        migrations.AlterField(
            model_name="usr",
            name="upic",
            field=models.CharField(
                blank=True, default=None, max_length=1000, null=True
            ),
        ),
    ]

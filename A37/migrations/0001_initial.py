# Generated by Django 4.1.5 on 2023-03-05 03:46

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Usr",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("iswx", models.BooleanField(default=False)),
                ("wxid", models.CharField(max_length=200, null=True)),
                ("iszfb", models.BooleanField(default=False)),
                ("zfbid", models.CharField(max_length=200, null=True)),
                ("uname", models.CharField(default=uuid.uuid4, max_length=200)),
                ("uphone", models.CharField(max_length=30)),
                ("ubirth", models.DateField()),
                ("password", models.CharField(max_length=45)),
                ("upic", models.CharField(blank=True, max_length=1000, null=True)),
                ("ucreate", models.DateField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name="Outs",
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
                ("bname", models.BooleanField(max_length=500)),
                ("ispic", models.BooleanField(default=False)),
                ("bpic", models.CharField(blank=True, max_length=1000, null=True)),
                ("isfinish", models.BooleanField(default=False)),
                ("isremind", models.BooleanField(default=False)),
                ("rtime", models.DateTimeField(blank=True, null=True)),
                ("bcategory", models.CharField(max_length=500)),
                ("note", models.CharField(blank=True, max_length=1000, null=True)),
                ("payment", models.CharField(max_length=500)),
                ("amount", models.FloatField()),
                ("btime", models.DateTimeField()),
                ("isreceipt", models.BooleanField(default=False)),
                ("receipt", models.CharField(blank=True, max_length=1000, null=True)),
                (
                    "usr",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="A37.usr"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ins",
            fields=[
                ("bname", models.CharField(max_length=500)),
                ("ispic", models.BooleanField(default=False)),
                ("bpic", models.CharField(blank=True, max_length=1000, null=True)),
                ("bcategory", models.CharField(max_length=500)),
                ("note", models.CharField(blank=True, max_length=1000, null=True)),
                ("payment", models.CharField(max_length=500)),
                ("amount", models.FloatField()),
                ("btime", models.DateTimeField(primary_key=True, serialize=False)),
                ("isreceipt", models.BooleanField()),
                ("receipt", models.CharField(blank=True, max_length=1000, null=True)),
                (
                    "usr",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="A37.usr"
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 4.1.5 on 2023-03-17 09:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("A37", "0006_alter_outs_isfinish"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ins",
            name="btime",
            field=models.DateTimeField(primary_key=False),
        ),
        migrations.AddField(
            model_name="ins",
            name="id",
            field=models.AutoField(
                primary_key=True, serialize=False, verbose_name="自增id"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="outs",
            name="id",
            field=models.AutoField(
                primary_key=True, serialize=False, verbose_name="自增id"
            ),
        ),
        migrations.AlterField(
            model_name="usr",
            name="iswx",
            field=models.BooleanField(default=False, verbose_name="是否使用微信登陆"),
        ),
        migrations.AlterField(
            model_name="usr",
            name="iszfb",
            field=models.BooleanField(default=False, verbose_name="是否使用支付宝登陆"),
        ),
        migrations.AlterField(
            model_name="usr",
            name="uid",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
                verbose_name="UUID",
            ),
        ),
        migrations.AlterField(
            model_name="usr",
            name="wxid",
            field=models.CharField(max_length=200, null=True, verbose_name="微信ID"),
        ),
    ]

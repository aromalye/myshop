# Generated by Django 4.1 on 2022-10-29 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycart', '0006_myfav'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myfav',
            name='color',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='myfav',
            name='size',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
# Generated by Django 4.1 on 2022-10-13 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycart', '0002_mycartitem_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
            ],
        ),
    ]

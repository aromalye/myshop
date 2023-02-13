# Generated by Django 4.1 on 2022-11-11 07:36

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_reviewproduct_rateproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Red', 'Red'), ('Black', 'Black'), ('Blue', 'Blue')], max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')], max_length=30, null=True),
        ),
    ]
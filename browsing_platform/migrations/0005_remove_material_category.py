# Generated by Django 3.2 on 2021-12-31 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('browsing_platform', '0004_material_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='category',
        ),
    ]

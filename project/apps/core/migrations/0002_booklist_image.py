# Generated by Django 4.1 on 2024-03-01 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booklist',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]

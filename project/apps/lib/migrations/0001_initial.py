# Generated by Django 4.1 on 2024-03-22 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('desc', models.TextField(blank=True, null=True)),
                ('price', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Gari',
            },
        ),
    ]
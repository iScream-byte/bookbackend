# Generated by Django 4.2.10 on 2024-02-23 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0004_alter_user_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

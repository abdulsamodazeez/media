# Generated by Django 5.1.5 on 2025-01-20 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_remove_socialmediaaccount_created_at_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]

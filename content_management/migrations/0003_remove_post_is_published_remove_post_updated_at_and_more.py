# Generated by Django 5.1.5 on 2025-01-20 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_management', '0002_alter_medialibrary_category_alter_medialibrary_file_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_published',
        ),
        migrations.RemoveField(
            model_name='post',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=20),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(default='Default content'),
            preserve_default=False,
        ),
    ]

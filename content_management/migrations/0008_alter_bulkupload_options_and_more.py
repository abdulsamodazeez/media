import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_management', '0007_post_recurrence_pattern_post_scheduled_time_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bulkupload',
            options={'verbose_name': 'Bulk Upload', 'verbose_name_plural': 'Bulk Uploads'},
        ),
        migrations.AlterModelOptions(
            name='contentmoderation',
            options={'verbose_name': 'Content Moderation', 'verbose_name_plural': 'Content Moderations'},
        ),
        migrations.AlterModelOptions(
            name='medialibrary',
            options={'verbose_name': 'Media File', 'verbose_name_plural': 'Media Library'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.RenameField(
            model_name='bulkupload',
            old_name='created_at',
            new_name='uploaded_at',
        ),
        migrations.RemoveField(
            model_name='bulkupload',
            name='status',
        ),
        migrations.AddField(
            model_name='post',
            name='platforms',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bulkupload',
            name='user',
            field=models.ForeignKey(
                default=1,  # Replace `1` with a valid user ID in your database
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(
                choices=[('draft', 'Draft'), ('published', 'Published'), ('scheduled', 'Scheduled')],
                default='draft',
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(
                default=1,  # Replace `1` with a valid user ID in your database
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]

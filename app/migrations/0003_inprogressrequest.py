# Generated by Django 4.2.3 on 2023-07-26 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_translationrequest_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='InProgressRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_progress_date', models.DateTimeField(auto_now_add=True)),
                ('in_progress_notes', models.TextField()),
                ('translation_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_progress_requests', to='app.translationrequest')),
            ],
        ),
    ]
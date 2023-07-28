# Generated by Django 4.2.3 on 2023-07-28 16:29

import app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('term_condition', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TranslationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('source_language', models.CharField(choices=[('French', 'French'), ('Haitian Creole', 'Haitian Creole'), ('English', 'English'), ('Spanish', 'Spanish')], max_length=50)),
                ('target_language', models.CharField(choices=[('French', 'French'), ('Haitian Creole', 'Haitian Creole'), ('English', 'English'), ('Spanish', 'Spanish')], max_length=50)),
                ('content', models.TextField(help_text='Additional information')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending', max_length=20)),
                ('completed_files', models.PositiveIntegerField(default=0)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.clientinfo')),
            ],
        ),
        migrations.CreateModel(
            name='ClientFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_file', models.FileField(upload_to=app.models.client_directory_path, validators=[app.models.file_size])),
                ('processed_file', models.FileField(blank=True, null=True, upload_to=app.models.client_directory_path, validators=[app.models.file_size])),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_files', to='app.clientinfo')),
                ('translation_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='app.translationrequest')),
            ],
        ),
    ]

# Generated by Django 5.1.3 on 2024-11-29 15:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_clientuser_preferred_chatbot_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientuser',
            name='preferred_chatbot',
        ),
        migrations.AddField(
            model_name='clientuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='clientuser',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ChatMessages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_type', models.CharField(choices=[('user', 'User'), ('bot', 'Bot')], max_length=4)),
                ('nickname', models.CharField(max_length=40)),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

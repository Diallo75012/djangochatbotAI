# Generated by Django 5.1.3 on 2024-11-29 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_clientuser_preferred_chatbot_clientuser_email_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ChatMessages',
        ),
    ]

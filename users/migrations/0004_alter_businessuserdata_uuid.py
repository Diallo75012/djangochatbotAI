# Generated by Django 5.1.3 on 2024-11-25 20:18

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_chatbotsettings_businessuserdata_uuid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessuserdata',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]

# Generated by Django 5.1.3 on 2024-11-27 18:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessdata', '0002_alter_businessuserdata_uuid'),
        ('chatbotsettings', '0002_rename_descritpion_chatbotsettings_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatbotsettings',
            name='business_user_uuid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='businessdata.businessuserdata', to_field='uuid'),
        ),
        migrations.AlterField(
            model_name='chatbotsettings',
            name='custom_greeting',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='chatbotsettings',
            name='description',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='chatbotsettings',
            name='dream',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='chatbotsettings',
            name='example_of_response',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='chatbotsettings',
            name='expertise',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='chatbotsettings',
            name='origin',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

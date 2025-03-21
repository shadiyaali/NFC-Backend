# Generated by Django 5.1.6 on 2025-03-03 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfc', '0006_vendor_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('website', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='user_logos/')),
                ('facebook', models.TextField(blank=True, null=True)),
                ('instagram', models.TextField(blank=True, null=True)),
                ('youtube', models.TextField(blank=True, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('location_map', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Block', 'Block')], default='Active', max_length=255, null=True)),
            ],
        ),
    ]

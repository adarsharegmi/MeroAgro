# Generated by Django 3.1.2 on 2021-02-06 09:58

import UserManagementSystem.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=30)),
                ('user_email', models.EmailField(max_length=254)),
                ('user_address', models.CharField(max_length=50)),
                ('user_password', models.CharField(max_length=200)),
                ('user_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_confirmed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='UserManagementSystem.user')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(storage=UserManagementSystem.models.OverwriteStorage, upload_to='user/image_profile')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='UserManagementSystem.user')),
            ],
        ),
    ]

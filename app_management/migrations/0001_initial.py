# Generated by Django 4.0.3 on 2024-08-01 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('icon', models.ImageField(upload_to='app_icons/')),
                ('active', models.BooleanField(default=False)),
                ('url', models.CharField(default='#', max_length=100)),
            ],
        ),
    ]

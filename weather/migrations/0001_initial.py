# Generated by Django 5.0.6 on 2024-06-07 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('temperature', models.FloatField()),
                ('Feeling_temp', models.FloatField()),
                ('Min_temp', models.FloatField()),
                ('Max_temp', models.FloatField()),
                ('description', models.CharField(max_length=100)),
                ('icon', models.CharField(max_length=10)),
                ('humidity', models.IntegerField()),
                ('wind_speed', models.FloatField()),
                ('wind_direction', models.IntegerField()),
                ('uv_index', models.FloatField()),
                ('air_quality', models.FloatField()),
                ('data_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
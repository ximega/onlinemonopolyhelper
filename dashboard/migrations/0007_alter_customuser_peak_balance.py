# Generated by Django 5.1.3 on 2024-12-17 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_customuser_all_received_customuser_all_sent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='peak_balance',
            field=models.IntegerField(default=700),
        ),
    ]

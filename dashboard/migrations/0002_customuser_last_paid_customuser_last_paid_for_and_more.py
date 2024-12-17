# Generated by Django 5.1.3 on 2024-12-16 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='last_paid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_paid_for',
            field=models.TextField(default='Nothing'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_received_from',
            field=models.TextField(default='Nobody'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_sent_to',
            field=models.TextField(default='Nobody'),
        ),
    ]

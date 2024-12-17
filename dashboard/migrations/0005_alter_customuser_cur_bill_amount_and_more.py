# Generated by Django 5.1.3 on 2024-12-16 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_customuser_is_billed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cur_bill_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='cur_bill_type',
            field=models.TextField(default='None'),
        ),
    ]
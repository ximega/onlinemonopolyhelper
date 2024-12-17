# Generated by Django 5.1.3 on 2024-12-17 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_customuser_cur_bill_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='all_received',
            field=models.TextField(default='{}'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='all_sent',
            field=models.TextField(default='{}'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='bills_paid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='largest_bill_paid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='peak_balance',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 4.0.5 on 2022-08-20 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_employee_commission'),
    ]

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=100)),
                ('customer_phone', models.CharField(max_length=100)),
                ('amount', models.IntegerField(default=0, max_length=100)),
                ('paid', models.IntegerField(default=0, max_length=100)),
                ('balance', models.IntegerField(default=0, max_length=100)),
                ('mode', models.CharField(max_length=100)),
                ('added_by', models.CharField(max_length=100)),
                ('status', models.IntegerField(default=0, max_length=1)),
                ('added_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='orderdetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(max_length=100)),
                ('service_price', models.IntegerField(default=0, max_length=100)),
                ('total', models.IntegerField(default=0, max_length=100)),
                ('order_id', models.IntegerField(default=0, max_length=100)),
                ('added_by', models.CharField(max_length=100)),
                ('status', models.IntegerField(default=0, max_length=1)),
                ('added_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='orders',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='item_name',
            new_name='service',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='amount',
            new_name='service_price',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='name',
            new_name='staff',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='quantity',
        ),
    ]

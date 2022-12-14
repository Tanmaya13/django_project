# Generated by Django 4.0.6 on 2022-07-31 11:39

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('pid', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=300)),
                ('product_desc', models.TextField(default='')),
                ('price_per_person', models.PositiveIntegerField()),
                ('child_price', models.PositiveSmallIntegerField()),
                ('available_from', models.DateField(default=datetime.date(2022, 7, 31))),
                ('available_till', models.DateField(default=datetime.date(2022, 8, 7))),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('sid', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('service_name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('tid', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=400)),
                ('content', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('phone', models.PositiveBigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_joined', models.DateTimeField(default=datetime.datetime(2022, 7, 31, 17, 9, 46, 273892))),
                ('is_staff', models.BooleanField(default=False)),
                ('logged_in', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShowImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpeg', upload_to='single-prod/')),
                ('image_position', models.CharField(choices=[('Main', 'Main'), ('Side', 'Side')], max_length=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpeg', upload_to='product/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='sid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.services'),
        ),
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('bid', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.product')),
            ],
        ),
        migrations.CreateModel(
            name='BookingDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_service', models.BooleanField(default=False)),
                ('pickup_from_airport', models.BooleanField(default=False)),
                ('num_people', models.PositiveSmallIntegerField(default=2)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.bookings', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestimonialImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='testimonial/')),
                ('testimonial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.testimonial')),
            ],
            options={
                'unique_together': {('testimonial', 'image')},
            },
        ),
        migrations.CreateModel(
            name='ProductDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_detail', models.CharField(max_length=300)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.product')),
            ],
            options={
                'unique_together': {('product', 'key_detail')},
            },
        ),
    ]

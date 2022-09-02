from django.db import models

# Create your models here.
from django.db import models
import datetime

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    phone = models.PositiveBigIntegerField(unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=datetime.datetime.now())
    is_staff = models.BooleanField(default=False)
    logged_in = models.BooleanField(default=True)

    def __str__(self):
        return '{}: {}'.format(self.name, self.phone)

class Services(models.Model):
    sid = models.AutoField(auto_created=True, serialize=True, primary_key=True)
    service_name = models.CharField(max_length=250)

    def __str__(self):
        return self.service_name

class Product(models.Model):
    pid = models.AutoField(auto_created=True, serialize=True, primary_key=True)
    sid = models.ForeignKey(Services, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=300)
    product_desc = models.TextField(default="")
    price_per_person = models.PositiveIntegerField()
    child_price = models.PositiveSmallIntegerField()
    available_from = models.DateField(default=datetime.datetime.now().date())
    available_till = models.DateField(default=(datetime.datetime.now().date()+datetime.timedelta(days=7)))

    def __str__(self):
        return self.product_name

class ProductImage(models.Model):
    image = models.ImageField(upload_to="product/", default='default.jpeg')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

types = (
    ('Main', 'Main'),
    ('Side', 'Side'),
)
class ShowImages(models.Model):
    image = models.ImageField(upload_to="single-prod/", default='default.jpeg')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_position = models.CharField(max_length=10, choices=types)

    def __str__(self):
        return self.product.product_name


class ProductDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    key_detail = models.CharField(max_length=300)
    class Meta:
        unique_together = (('product', 'key_detail'),)
    
    def __str__(self):
        return self.product.product_name



class Testimonial(models.Model):
    tid = models.AutoField(auto_created=True, serialize=True, primary_key=True)
    title = models.CharField(max_length=400)
    content = models.TextField(default="")

    def __str__(self):
        return self.title

class TestimonialImages(models.Model):
    testimonial = models.ForeignKey(Testimonial, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="testimonial/")
    class Meta:
        unique_together = (('testimonial', 'image'),)
    
    def __str__(self):
        return self.testimonial.title

class Bookings(models.Model):
    bid = models.AutoField(auto_created=True, serialize=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    booked_on = models.DateTimeField(default=datetime.datetime.now())
    adults = models.IntegerField(default=2)
    children = models.IntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    car_service = models.BooleanField(default=False)
    pickup_from_airport = models.BooleanField(default=False)

    def __str__(self):
        return 'Booking ID: ' + str(self.bid)

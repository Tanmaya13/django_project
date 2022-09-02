from django.contrib import admin
from .models import *

# Register your models here.
# Superadmin: username & pwd - admin123

admin.site.register(User)
admin.site.register(Services)
admin.site.register(Product)
admin.site.register(ProductDetails)
admin.site.register(Testimonial)
admin.site.register(TestimonialImages)
admin.site.register(ProductImage)
admin.site.register(ShowImages)
admin.site.register(Bookings)
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Perk(models.Model):
    title = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    subtext = models.TextField(blank=True)
    image = models.ImageField(upload_to='perks/')
    created_at = models.DateTimeField(auto_now_add=True)

DETAIL_PAGE_CHOICES = [
    ('tour_detail_half_day.html', 'Half Day Land Rover Trip'),
    ('tour_detail_full_day_land_rover.html', 'Full Day Land Rover Trip'),
    ('tour_detail_intimate_group.html', ' Intimate Group Adventure'),
      
    ('tour_detail_full_day_private.html', 'Full Day Private Tour'),  # new
    
]

from ckeditor.fields import RichTextField  # for rich HTML formatting


class FeaturedTour(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)  # Allow blank
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    badge = models.CharField(max_length=100, blank=True, null=True)
    rating = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)
    booking_count = models.IntegerField(default=0)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='tours/')
    child_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Price per child (age 3–7)")
    min_travelers = models.PositiveIntegerField(default=1, help_text="Minimum number of adults required to book this tour")

     # New fields to store full content:
    service_description = RichTextField(blank=True, null=True)
    highlights = RichTextField(blank=True, null=True)
    itinerary = RichTextField(blank=True, null=True)
    terms_conditions = RichTextField(blank=True, null=True)
    notes = RichTextField(blank=True, null=True)
    about_this_tour = RichTextField(blank=True, null=True)
    departure_time = models.CharField(max_length=255, blank=True, null=True)
    locations = RichTextField(blank=True, null=True)
    essentials = RichTextField(blank=True, null=True)
    max_bookings_per_day = models.IntegerField(default=10, help_text="Maximum bookings allowed per day")  # ✅ Add this
    start_time = models.TimeField(default="08:00")  # <-- 🆕 Added this


    
    detail_page = models.CharField(
        max_length=255,
        blank=True,
        choices=[
            ('tour_dynamic.html', 'Dynamic Tour Template'),
            # Add other if needed
        ]
    )
    
    detail_page = models.CharField(
        max_length=100,
        choices=DETAIL_PAGE_CHOICES,
        blank=True,
        null=True,
        help_text="Optional: Select a detail page template to link this tour's 'Book' button"
    )


    def __str__(self):
            return self.title  # ✅ This will show private tour name instead of 'object'
    
    def formatted_bookings(self):
        if self.booking_count >= 1000:
            return f"{round(self.booking_count / 1000, 1)}k+ Booked"
        return f"{self.booking_count} Booked"
    
    
    def get_absolute_url(self):
        return reverse('tour_detail_generic', args=[self.slug])
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
          if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

DETAIL_PAGE_CHOICES = [
    ('tour_detail_half_day_coral_hill.html', 'Half Day Trip - Coral Hills'),
   
   
    ('tour_detail_private_half_day.html', 'Private Half Day Tour'),  # new
    
    ('tour_detail_sunrise_half_day.html', 'Sunrise + Half Day Tour'),  # new
]

class PrivateTour(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)  # ✅ Added missing slug field
    badge = models.CharField(max_length=100, blank=True, null=True)
    rating = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)
    booking_count = models.IntegerField(default=0)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='private_tours/')
    child_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Price per child (age 3–7)")
    min_travelers = models.PositiveIntegerField(default=1, help_text="Minimum number of adults required to book this private tour")
    start_time = models.TimeField(default="08:00")  # <-- 🆕 Added this


      # New fields to store full content:
    service_description = RichTextField(blank=True, null=True)
    highlights = RichTextField(blank=True, null=True)
    itinerary = RichTextField(blank=True, null=True)
    terms_conditions = RichTextField(blank=True, null=True)
    notes = RichTextField(blank=True, null=True)
    about_this_tour = RichTextField(blank=True, null=True)
    departure_time = models.CharField(max_length=255, blank=True, null=True)
    locations = RichTextField(blank=True, null=True)
    essentials = RichTextField(blank=True, null=True)
    max_bookings_per_day = models.IntegerField(default=10, help_text="Maximum bookings allowed per day")  # ✅ Add this
   
    detail_page = models.CharField(
        max_length=100,
        choices=DETAIL_PAGE_CHOICES,
        blank=True,
        null=True,
        help_text="Optional: Select a detail page template to link this tour's 'Book' button"
    )

    
    def __str__(self):
        return self.title  # ✅ This will show tour name instead of 'object'

    def formatted_bookings(self):
        if self.booking_count >= 1000:
            return f"{round(self.booking_count / 1000, 1)}k+ Booked"
        return f"{self.booking_count} Booked"
    

    def get_absolute_url(self):
        return reverse('tour_detail_generic', args=[self.slug])
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

from django.db import models

PICKUP_CHOICES = [
    ('hotel', 'Hotel Pickup – user enters address'),
    ('default', 'Default Pickup – show predefined location'),
]

class Transfer(models.Model):
    from_city = models.CharField(max_length=255)
    to_city = models.CharField(max_length=255)
    journey_type = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    important_info = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    child_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # ✅ ADD THIS
    start_time = models.TimeField(default="08:00")  # ✅ Add this
    max_bookings_per_day = models.IntegerField(default=10, help_text="Maximum bookings allowed per day")  # ✅ Add this


    # ✅ NEW FIELD
    pickup_type = models.CharField(
        max_length=20,
        choices=PICKUP_CHOICES,
        default='hotel',
        help_text="Choose whether this transfer uses hotel address input or a fixed pickup location."
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.pickup_location}-{self.dropoff_location}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.from_city} to {self.to_city}"
    

    # models.py

class TransferBooking(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    hotel_address = models.CharField(max_length=500)
    pickup_map_url = models.URLField(blank=True, null=True)  # ✅ NEW FIELD

    # Foreign keys or data like:
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=50)
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ NEW FIELD

    def __str__(self):
        return f"{self.full_name} - {self.transfer} on {self.date}"

class TourBooking(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    hotel_address = models.CharField(max_length=500, blank=True, null=True)
    pickup_map_url = models.URLField(blank=True, null=True)

    # Foreign keys:
    featured_tour = models.ForeignKey(FeaturedTour, on_delete=models.CASCADE, blank=True, null=True)
    private_tour = models.ForeignKey(PrivateTour, on_delete=models.CASCADE, blank=True, null=True)

    date = models.DateField()
    time = models.CharField(max_length=50)
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - Tour Booking on {self.date}"


class TourAvailability(models.Model):
    featured_tour = models.ForeignKey('FeaturedTour', on_delete=models.CASCADE, null=True, blank=True)
    private_tour = models.ForeignKey('PrivateTour', on_delete=models.CASCADE, null=True, blank=True)
    transfer = models.ForeignKey('Transfer', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    max_bookings = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.date} - {self.max_bookings} bookings"

# 📦 models.py

class TransferAvailability(models.Model):
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE)
    date = models.DateField()
    max_bookings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.transfer} on {self.date}"

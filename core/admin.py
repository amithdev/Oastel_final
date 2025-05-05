from django.contrib import admin
from .models import Perk, FeaturedTour, PrivateTour ,City
from ckeditor.widgets import CKEditorWidget
from django import forms

@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at')

class FeaturedTourForm(forms.ModelForm):
    service_description = forms.CharField(widget=CKEditorWidget(), required=False)
    about_this_tour = forms.CharField(widget=CKEditorWidget(), required=False)
    highlights = forms.CharField(widget=CKEditorWidget(), required=False)
    itinerary = forms.CharField(widget=CKEditorWidget(), required=False)
    terms_conditions = forms.CharField(widget=CKEditorWidget(), required=False)
    notes = forms.CharField(widget=CKEditorWidget(), required=False)
    min_travelers = forms.IntegerField(required=False, initial=1)

    class Meta:
        model = FeaturedTour
        fields = '__all__'


@admin.register(FeaturedTour)
class FeaturedTourAdmin(admin.ModelAdmin):
    form = FeaturedTourForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'badge', 'rating', 'rating_count', 'booking_count','min_travelers','start_time')

@admin.register(PrivateTour)
class PrivateTourAdmin(admin.ModelAdmin):
    form = FeaturedTourForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'badge', 'rating', 'rating_count', 'booking_count','min_travelers','start_time')

admin.site.register(City)

from .models import Transfer

class TransferAdmin(admin.ModelAdmin):
    list_display = ('from_city', 'to_city', 'price', 'pickup_type', 'max_bookings_per_day',)  # Show pickup_type
    list_filter = ('pickup_type',)  # Filter by pickup type
admin.site.register(Transfer, TransferAdmin)


from django.utils.html import format_html
from django.contrib import admin
from .models import TransferBooking
@admin.register(TransferBooking)
class TransferBookingAdmin(admin.ModelAdmin):
    readonly_fields = (
        'full_name', 'email', 'phone', 'hotel_address', 'pickup_map_link',
        'transfer', 'date', 'time', 'adults', 'children',
        'created_at', 'price_summary',
    )
    def price_summary(self, obj):
      if obj.transfer:
        adult_price = getattr(obj.transfer, 'price', 0) or 0
        child_price = getattr(obj.transfer, 'child_price', 0) or 0
        adults = obj.adults or 0
        children = obj.children or 0

        total_adult_price = adults * adult_price
        total_child_price = children * child_price
        total_price = total_adult_price + total_child_price

        html = ""

        if adults > 0:
            html += f"Adults ({adults} x RM {adult_price:.2f}) = RM {total_adult_price:.2f}<br>"

        if children > 0 and child_price > 0:
            html += f"Children ({children} x RM {child_price:.2f}) = RM {total_child_price:.2f}<br>"

        html += "<hr><strong>Total = RM {:.2f}</strong>".format(total_price)
        return format_html(html)

      return "-"


    

    def pickup_map_link(self, obj):
        if obj.pickup_map_url:
            return format_html('<a href="{}" target="_blank">View on Map</a>', obj.pickup_map_url)
        return "-"
    pickup_map_link.short_description = "Pickup Map URL"


from django.utils.html import format_html
from django.contrib import admin
from .models import TourAvailability
from .models import (
    FeaturedTour, PrivateTour, Perk, Transfer, TransferBooking, City,
    TourAvailability, TransferAvailability
)

class TourAvailabilityForm(forms.ModelForm):
    class Meta:
        model = TourAvailability
        fields = ['featured_tour', 'private_tour', 'date', 'max_bookings']

    class Media:
        js = ('core/js/tour_availability_autofill.js',)  # 👉 we will create this JS file




# ✅ Transfer Availability Admin (new)
@admin.register(TransferAvailability)
class TransferAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('get_transfer_title', 'date', 'max_bookings', 'status_badge')
    list_filter = ('date', 'transfer')
    search_fields = ('transfer__from_city', 'transfer__to_city')
    ordering = ('-date',)

    def get_transfer_title(self, obj):
        if obj.transfer:
            return f"{obj.transfer.from_city} → {obj.transfer.to_city}"
        return "Unknown"
    get_transfer_title.short_description = "Transfer Title"

    def status_badge(self, obj):
        if obj.max_bookings > 0:
            return "✅ Available"
        return "❌ Fully Booked"
    status_badge.short_description = "Status"




from django import forms
from .models import TourAvailability, FeaturedTour, PrivateTour

class SimpleTourAvailabilityForm(forms.ModelForm):
    tour = forms.ChoiceField(label="Select Tour", required=True)

    class Meta:
        model = TourAvailability
        fields = ['tour', 'date', 'max_bookings']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        featured = FeaturedTour.objects.all()
        private = PrivateTour.objects.all()

        tour_choices = [('', '--- Select Tour ---')]

        for f in featured:
            tour_choices.append((f'featured_{f.id}', f'[Featured] {f.title}'))

        for p in private:
            tour_choices.append((f'private_{p.id}', f'[Private] {p.title}'))

        self.fields['tour'].choices = tour_choices

    def clean(self):
        cleaned_data = super().clean()
        tour = cleaned_data.get('tour')

        if tour:
            if tour.startswith('featured_'):
                tour_id = int(tour.split('_')[1])
                featured = FeaturedTour.objects.get(id=tour_id)
                cleaned_data['featured_tour'] = featured
                cleaned_data['max_bookings'] = featured.max_bookings_per_day

            elif tour.startswith('private_'):
                tour_id = int(tour.split('_')[1])
                private = PrivateTour.objects.get(id=tour_id)
                cleaned_data['private_tour'] = private
                cleaned_data['max_bookings'] = private.max_bookings_per_day

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        tour = self.cleaned_data.get('tour')
        if tour:
            if tour.startswith('featured_'):
                instance.featured_tour = FeaturedTour.objects.get(id=int(tour.split('_')[1]))
                instance.private_tour = None
            elif tour.startswith('private_'):
                instance.private_tour = PrivateTour.objects.get(id=int(tour.split('_')[1]))
                instance.featured_tour = None

        if commit:
            instance.save()
        return instance
    
from django import forms
from django.contrib import admin
from .models import TourAvailability, FeaturedTour, PrivateTour
from .forms import SimpleTourAvailabilityForm


@admin.register(TourAvailability)
class TourAvailabilityAdmin(admin.ModelAdmin):
    form = SimpleTourAvailabilityForm  # custom form used here

    list_display = ('get_tour_title', 'date', 'max_bookings', 'status_badge')
    ordering = ('-date',)

    def get_tour_title(self, obj):
        if obj.featured_tour:
            return f"Featured: {obj.featured_tour.title}"
        elif obj.private_tour:
            return f"Private: {obj.private_tour.title}"
        return "Unknown"
    get_tour_title.short_description = "Tour Title"

    def status_badge(self, obj):
        return "✅ Available" if obj.max_bookings > 0 else "❌ Fully Booked"
    status_badge.short_description = "Status"


from django import forms
from .models import TourAvailability, FeaturedTour, PrivateTour

class TourAvailabilityForm(forms.ModelForm):
    class Meta:
        model = TourAvailability
        fields = '__all__'

    class Media:
        js = ('admin/js/tour_availability_autofill.js',)


from django.contrib import admin
from .models import TourBooking

@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'date', 'tour_title', 'price_breakdown', 'adults', 'children')
    list_filter = ('date',)
    ordering = ('-date',)
    search_fields = ('full_name', 'email')

    def tour_title(self, obj):
        return obj.featured_tour.title if obj.featured_tour else obj.private_tour.title
    tour_title.short_description = "Tour"

    def price_breakdown(self, obj):
        tour = obj.featured_tour or obj.private_tour
        if not tour:
            return "—"

        adult_price = tour.discounted_price
        child_price = tour.child_price

        parts = []
        if obj.adults:
            parts.append(f"{obj.adults} Adult × RM{adult_price:.2f}")
        if obj.children:
            parts.append(f"{obj.children} Child × RM{child_price:.2f}")

        return " + ".join(parts)
    price_breakdown.short_description = "Price Breakdown"


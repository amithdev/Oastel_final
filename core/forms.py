from django import forms
from .models import TourAvailability, FeaturedTour, PrivateTour

class SimpleTourAvailabilityForm(forms.ModelForm):
    class Meta:
        model = TourAvailability
        fields = ['featured_tour', 'private_tour', 'date', 'max_bookings']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set max_bookings from selected tour if it's a new instance
        if not self.instance.pk:
            featured_tour = self.initial.get('featured_tour') or self.data.get('featured_tour')
            private_tour = self.initial.get('private_tour') or self.data.get('private_tour')

            if featured_tour:
                try:
                    ft = FeaturedTour.objects.get(id=featured_tour)
                    self.fields['max_bookings'].initial = ft.max_bookings_per_day
                except FeaturedTour.DoesNotExist:
                    pass

            elif private_tour:
                try:
                    pt = PrivateTour.objects.get(id=private_tour)
                    self.fields['max_bookings'].initial = pt.max_bookings_per_day
                except PrivateTour.DoesNotExist:
                    pass

    class Media:
        js = ('core/js/tour_availability_autofill.js',)  # ✅ Must match the JS file in static folder

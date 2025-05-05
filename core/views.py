from django.shortcuts import render
from .models import Perk ,City,Transfer,TransferBooking
from core.models import TourBooking, TransferBooking, FeaturedTour, PrivateTour, Transfer, TourAvailability


def home(request):
    perks = Perk.objects.all()
    return render(request, 'core/home.html', {'perks': perks})

def tours(request):
    return render(request, 'core/tours.html')

def tour_detail_half_day(request):
    return render(request, 'core/tour_detail_half_day.html')

def confirm_adventure(request):
    return render(request, 'core/confirm_adventure.html')

def payment_success(request):
    return render(request, 'core/payment_success.html')

def payment_cancel(request):
    return render(request, 'core/payment_cancel.html')

def book_transfers(request):
    return render(request, 'core/transfers.html')

def book_transfers(request):
    cities = City.objects.all()
    return render(request, 'core/transfers.html', {'cities': cities})



import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            success_url = 'http://127.0.0.1:8000/thank-you/?session_id={CHECKOUT_SESSION_ID}'
            cancel_url = request.build_absolute_uri('/payment-cancel/')

            adult_price = int(data.get('adult_price', 5000))  # in cents
            child_price = int(data.get('child_price', 0))     # in cents
            adults = int(data.get('adults', 1))
            children = int(data.get('children', 0))
            is_transfer = data.get('is_transfer', False)
            is_private_tour = data.get('is_private_tour', False)

            # Build line_items
            line_items = []

            if is_transfer:
                if adults > 0:
                    line_items.append({
                        'price_data': {
                            'currency': 'myr',
                            'product_data': {
                                'name': f"Transfer Adult Ticket ({data.get('from_city')} ➔ {data.get('to_city')})"
                            },
                            'unit_amount': adult_price ,  # Transfer per adult
                        },
                        'quantity': adults,
                    })
                if children > 0:
                    line_items.append({
                        'price_data': {
                            'currency': 'myr',
                            'product_data': {
                                'name': f"Transfer Child Ticket ({data.get('from_city')} ➔ {data.get('to_city')})"
                            },
                            'unit_amount': child_price ,  # Transfer per child
                        },
                        'quantity': children,
                    })

            else:
                if is_private_tour == True or is_private_tour == 'true':
                    # ✅ Private Tour
                    line_items.append({
                        'price_data': {
                            'currency': 'myr',
                            'product_data': {
                                'name': f"Private Group Tour: {data.get('tour_slug', 'Tour')}"
                            },
                            'unit_amount': adult_price,  # Private group price directly
                        },
                        'quantity': adults,  # Number of groups (groupMultiplier)
                    })
                else:
                    # ✅ Featured Tour
                    if adults > 0:
                        line_items.append({
                            'price_data': {
                                'currency': 'myr',
                                'product_data': {
                                    'name': f"Adult Ticket for Tour: {data.get('tour_slug', 'Tour')}"
                                },
                                'unit_amount': adult_price,  # per adult
                            },
                            'quantity': adults,
                        })
                    if children > 0:
                        line_items.append({
                            'price_data': {
                                'currency': 'myr',
                                'product_data': {
                                    'name': f"Children Tickets for Tour: {data.get('tour_slug', 'Tour')}"
                                },
                                'unit_amount': child_price,  # per child
                            },
                            'quantity': children,
                        })

            # Create checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=data.get('email'),
                metadata={
                    'adults': str(adults),
                    'children': str(children),
                    'date': data.get('date'),
                    'time': data.get('time'),
                    'full_name': data.get('full_name'),
                    'email': data.get('email'),
                    'phone': data.get('phone'),
                    'hotel_address': data.get('hotel_address'),
                    'pickup_map_url': data.get('pickup_map_url'),
                    'transfer_id': data.get('transfer_id'),  # ✅ safe (will be None for tours)
                    'tour_slug': data.get('tour_slug'),  
                                
                }
                
            )

            return JsonResponse({'sessionId': checkout_session.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



        
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
import stripe


from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
import stripe
from .models import Transfer, TransferBooking, TourBooking, FeaturedTour, PrivateTour

def thank_you(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return render(request, 'core/error.html', {'message': 'Session ID not found.'})

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        customer_email = session.customer_details.email

        # Get metadata from Stripe session
        metadata = session.get('metadata', {})
        full_name = metadata.get('full_name')
        email = metadata.get('email')
        phone = metadata.get('phone')
        hotel_address = metadata.get('hotel_address', '')
        pickup_map_url = metadata.get('pickup_map_url', '')
        adult_count = metadata.get('adults', '0')
        child_count = metadata.get('children', '0')
        date = metadata.get('date', '')
        time = metadata.get('time', '')

        # ✅ If this is a transfer booking
        transfer_id = metadata.get('transfer_id')
        if transfer_id:
            transfer = Transfer.objects.filter(id=transfer_id).first()
            if not transfer:
                return render(request, 'core/error.html', {'message': 'Transfer not found for booking.'})

            TransferBooking.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                hotel_address=hotel_address,
                pickup_map_url=pickup_map_url,
                transfer=transfer,
                date=date,
                time=time,
                adults=adult_count,
                children=child_count,
            )

            # Emails for Transfer
            send_mail(
                subject="🎉 Your Transfer Booking is Confirmed!",
                message=(
                    f"Thank you for booking your transfer!\n\n"
                    f"🗓 Date: {date}\n"
                    f"⏰ Time: {time}\n"
                    f"👤 Adults: {adult_count}\n"
                    f"👶 Children: {child_count}\n\n"
                    "We look forward to hosting you!"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[customer_email],
            )

            send_mail(
                subject="📥 New Transfer Booking Received!",
                message=(
                    f"A new transfer booking has been completed.\n\n"
                    f"📧 Customer Email: {customer_email}\n"
                    f"From: {metadata.get('from_city')}\n"
                    f"To: {metadata.get('to_city')}\n"
                    f"🗓 Date: {date}\n"
                    f"⏰ Time: {time}\n"
                    f"👤 Adults: {adult_count}\n"
                    f"👶 Children: {child_count}\n"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['amithdev.ami001@gmail.com'],
            )

        # ✅ If this is a tour booking
        elif metadata.get('tour_slug'):
            tour_slug = metadata.get('tour_slug')
            tour = FeaturedTour.objects.filter(slug=tour_slug).first() or PrivateTour.objects.filter(slug=tour_slug).first()

            if not tour:
                return render(request, 'core/error.html', {'message': 'Tour not found for booking.'})

            TourBooking.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                hotel_address=hotel_address,
                pickup_map_url=pickup_map_url,
                featured_tour=tour if isinstance(tour, FeaturedTour) else None,
                private_tour=tour if isinstance(tour, PrivateTour) else None,
                date=date,
                time=time,
                adults=adult_count,
                children=child_count,
            )

            # Emails for Tour
            send_mail(
                subject="🎉 Your Tour Booking is Confirmed!",
                message=(
                    f"Thank you for booking your tour: {tour.title}\n\n"
                    f"🗓 Date: {date}\n"
                    f"⏰ Time: {time}\n"
                    f"👤 Adults: {adult_count}\n"
                    f"👶 Children: {child_count}\n\n"
                    "We look forward to seeing you!"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[customer_email],
            )

            send_mail(
                subject="📥 New Tour Booking Received!",
                message=(
                    f"A new tour booking has been completed.\n\n"
                    f"Tour: {tour.title}\n"
                    f"📧 Customer Email: {customer_email}\n"
                    f"🗓 Date: {date}\n"
                    f"⏰ Time: {time}\n"
                    f"👤 Adults: {adult_count}\n"
                    f"👶 Children: {child_count}\n"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['amithdev.ami001@gmail.com'],
            )

        else:
            return render(request, 'core/error.html', {'message': 'Booking type not identified.'})

        return render(request, 'core/payment_success.html', {'email': customer_email})

    except Exception as e:
        return render(request, 'core/error.html', {'message': str(e)})


from .models import FeaturedTour, PrivateTour
from django.shortcuts import get_object_or_404

def tours(request):
    featured_tours = FeaturedTour.objects.all()
    private_tours = PrivateTour.objects.all()
    return render(request, 'core/tours.html', {
        'tours': featured_tours,
        'private_tours': private_tours,
    })


def tour_detail(request, slug):
    tour = get_object_or_404(FeaturedTour, slug=slug)
    return render(request, 'core/tour_detail_half_day.html', {'tour': tour})



def tour_detail_generic(request, slug):
    try:
        # Try to get from FeaturedTour first
        tour = FeaturedTour.objects.get(slug=slug)
    except FeaturedTour.DoesNotExist:
        # If not found, try PrivateTour
        tour = get_object_or_404(PrivateTour, slug=slug)

    return render(request, "core/tour_dynamic.html", {'tour': tour})

        




def book_transfers(request):
    transfers = Transfer.objects.all()
    cities = City.objects.all()
    return render(request, 'core/transfers.html', {
        'transfers': transfers,
        'cities': cities
    })

def blogs(request):
    perks = Perk.objects.all()
    return render(request, 'core/blogs.html', {'perks': perks})

from core.models import FeaturedTour, PrivateTour
from django.shortcuts import render, get_object_or_404

def confirm_tour(request, slug):
    try:
        tour = FeaturedTour.objects.get(slug=slug)
        tour_type = 'featured'
    except FeaturedTour.DoesNotExist:
        tour = get_object_or_404(PrivateTour, slug=slug)
        tour_type = 'private'

    # Use discounted_price from admin (assuming it’s for adult)
    adult_price = tour.discounted_price
    child_price = getattr(tour, 'child_price', 0)  # fallback to 0 if not present

    return render(request, 'core/confirm_adventure.html', {
        'tour': tour,
        'tour_type': tour_type,
        'adult_price': adult_price,
        'child_price': child_price,
        'min_travelers': tour.min_travelers,  # 👈 Send minimum travelers to frontend
        'start_time': tour.start_time,  # 🆕 Send start_time to HTML
    })

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transfer, TransferBooking
from datetime import datetime

def confirm_transfer(request):
    if request.method == 'POST':
        # Get all form values
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        phone = request.POST.get('phoneNumber')
        date = request.POST.get('date')
        time = request.POST.get('time')
        adults = request.POST.get('adults')
        children = request.POST.get('children')
        from_city = request.POST.get('from')
        to_city = request.POST.get('to')
        hotel_address = request.POST.get('hotel_address')  # ✅ capture address
        pickup_map_url = request.POST.get('pickup_map_url')

        transfer = Transfer.objects.filter(from_city=from_city, to_city=to_city).first()

        if transfer:
            TransferBooking.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                date=date,
                time=time,
                adults=adults,
                children=children,
                hotel_address=hotel_address,
                pickup_map_url=pickup_map_url,
                transfer=transfer
            )
            return redirect('payment_success')  # Or your thank you URL

        return render(request, 'core/error.html', {'message': 'Transfer not found.'})

    # For GET request
    from_city = request.GET.get('from')
    to_city = request.GET.get('to')
    date = request.GET.get('date')

    transfer = Transfer.objects.filter(from_city=from_city, to_city=to_city).first()
    if not transfer:
        return render(request, 'core/error.html', {'message': 'Transfer not found.'})

    return render(request, 'core/confirm_transfer.html', {
        'from_city': from_city,
        'to_city': to_city,
        'date': date,
        'price': transfer.price,
        'transfer': transfer,
        'start_time': transfer.start_time,  # 🆕 Send start_time to HTML
    })


from django.http import JsonResponse
from .models import FeaturedTour, PrivateTour, Transfer, TourAvailability, TransferAvailability, TourBooking, TransferBooking
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import json

def find_next_available_date(entity, model_type, date):
    """Search next available slot up to 60 days forward"""
    for i in range(1, 60):
        check_date = date + timedelta(days=i)
        if model_type == 'transfer':
            booked = TransferBooking.objects.filter(transfer=entity, date=check_date).count()
            availability = TransferAvailability.objects.filter(transfer=entity, date=check_date).first()
            max_slots = availability.max_bookings if availability else entity.max_bookings_per_day
        elif model_type == 'private':
            booked = TourBooking.objects.filter(private_tour=entity, date=check_date).count()
            availability = TourAvailability.objects.filter(private_tour=entity, date=check_date).first()
            max_slots = availability.max_bookings if availability else entity.max_bookings_per_day
        else:  # featured
            booked = TourBooking.objects.filter(featured_tour=entity, date=check_date).count()
            availability = TourAvailability.objects.filter(featured_tour=entity, date=check_date).first()
            max_slots = availability.max_bookings if availability else entity.max_bookings_per_day

        if max_slots and booked < max_slots:
            return str(check_date)
    return None

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime, timedelta
import json
from .models import (
    FeaturedTour, PrivateTour, Transfer,
    TourBooking, TransferBooking,
    TourAvailability, TransferAvailability
)

def find_next_available_date(obj, model_type, current_date):
    for i in range(1, 60):  # look 60 days ahead
        next_date = current_date + timedelta(days=i)

        if model_type == 'transfer':
            booked = TransferBooking.objects.filter(transfer=obj, date=next_date).count()
            availability = TransferAvailability.objects.filter(transfer=obj, date=next_date).first()
            max_slots = availability.max_bookings if availability else obj.max_bookings_per_day or 0
        elif model_type == 'private':
            booked = TourBooking.objects.filter(private_tour=obj, date=next_date).count()
            availability = TourAvailability.objects.filter(private_tour=obj, date=next_date).first()
            max_slots = availability.max_bookings if availability else obj.max_bookings_per_day or 0
        else:
            booked = TourBooking.objects.filter(featured_tour=obj, date=next_date).count()
            availability = TourAvailability.objects.filter(featured_tour=obj, date=next_date).first()
            max_slots = availability.max_bookings if availability else obj.max_bookings_per_day or 0

        if max_slots > 0 and booked < max_slots:
            return next_date.strftime('%Y-%m-%d')

    return None  # No slot found

@csrf_exempt
def check_availability(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            date_str = data.get('date')
            is_transfer = data.get('is_transfer', False)
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except Exception:
            return JsonResponse({'available': False, 'error': 'Invalid date format'})

        # ✅ TRANSFER
        if is_transfer:
            transfer_id = data.get('transfer_id')
            try:
                transfer = Transfer.objects.get(id=transfer_id)
                availability = TransferAvailability.objects.filter(transfer=transfer, date=date).first()
                max_bookings = availability.max_bookings if availability else transfer.max_bookings_per_day or 0

                if max_bookings == 0:
                    next_date = find_next_available_date(transfer, 'transfer', date)
                    return JsonResponse({'available': False, 'next_available': next_date})

                booked = TransferBooking.objects.filter(transfer=transfer, date=date).count()
                if booked < max_bookings:
                    return JsonResponse({
                        'available': True,
                        'start_time': transfer.start_time.strftime('%I:%M %p')
                    })
                else:
                    next_date = find_next_available_date(transfer, 'transfer', date)
                    return JsonResponse({'available': False, 'next_available': next_date})
            except Transfer.DoesNotExist:
                return JsonResponse({'available': False, 'error': 'Transfer not found'})

        # ✅ TOUR (private or featured)
        else:
            slug = data.get('tour_slug')
            tour_type = data.get('tour_type')
            try:
                if tour_type == 'private':
                    tour = PrivateTour.objects.get(slug=slug)
                    model_key = 'private'
                    availability = TourAvailability.objects.filter(private_tour=tour, date=date).first()
                    max_bookings = availability.max_bookings if availability else tour.max_bookings_per_day or 0
                    booked = TourBooking.objects.filter(private_tour=tour, date=date).count()
                else:
                    tour = FeaturedTour.objects.get(slug=slug)
                    model_key = 'featured'
                    availability = TourAvailability.objects.filter(featured_tour=tour, date=date).first()
                    max_bookings = availability.max_bookings if availability else tour.max_bookings_per_day or 0
                    booked = TourBooking.objects.filter(featured_tour=tour, date=date).count()

                if max_bookings == 0:
                    next_date = find_next_available_date(tour, model_key, date)
                    return JsonResponse({'available': False, 'next_available': next_date})

                if booked < max_bookings:
                    return JsonResponse({
                        'available': True,
                        'start_time': tour.start_time.strftime('%I:%M %p')
                         

                    })
                
                else:
                    next_date = find_next_available_date(tour, model_key, date)
                    return JsonResponse({'available': False, 'next_available': next_date})
            except Exception:
                return JsonResponse({'available': False, 'error': 'Tour not found or invalid'})

    return JsonResponse({'available': False, 'error': 'Invalid request'})


def get_max_bookings(request):
    tour_slug = request.GET.get('slug')
    tour_type = request.GET.get('type')  # 'featured', 'private', or 'transfer'
    date = request.GET.get('date')

    try:
        if tour_type == 'featured':
            tour = FeaturedTour.objects.get(slug=tour_slug)
            availability = TourAvailability.objects.filter(featured_tour=tour, date=date).first()
            max_bookings = availability.max_bookings if availability else tour.max_bookings_per_day
        elif tour_type == 'private':
            tour = PrivateTour.objects.get(slug=tour_slug)
            availability = TourAvailability.objects.filter(private_tour=tour, date=date).first()
            max_bookings = availability.max_bookings if availability else tour.max_bookings_per_day
        elif tour_type == 'transfer':
            tour = Transfer.objects.get(slug=tour_slug)
            availability = TransferAvailability.objects.filter(transfer=tour, date=date).first()
            max_bookings = availability.max_bookings if availability else tour.max_bookings_per_day
        else:
            return JsonResponse({'error': 'Invalid type'}, status=400)

        return JsonResponse({'max_bookings': max_bookings or 0})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

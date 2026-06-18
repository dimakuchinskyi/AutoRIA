from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken  # Імпорт для JWT
from .models import CarAd  
from .utils import upload_image_to_cloudinary
from django.http import JsonResponse
from django.template.loader import render_to_string


@staff_member_required(login_url='/auth/')
def admin_edit_ad(request, ad_id):
    ad = get_object_or_404(CarAd, id=ad_id)
    
    if request.method == 'POST':
        ad.brand = request.POST.get('brand')
        ad.model = request.POST.get('model')
        ad.price = request.POST.get('price')
        # Додай інші поля, якщо потрібно редагувати все
        ad.save()
        messages.success(request, 'Оголошення успішно оновлено модератором!')
        return redirect('custom_admin')
        
    return render(request, 'edit_car.html', {'ad': ad})

def home_view(request):
    cars = CarAd.objects.all().order_by('-created_at')[:4]
    return render(request, 'base.html', {'cars': cars})

def auth_view(request):
    return render(request, 'auth.html')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            messages.error(request, 'Користувач з таким e-mail вже існує!')
            return redirect('auth')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('cabinet')

    return redirect('auth')

@login_required(login_url='/auth/')
def cabinet_view(request):
    user_ads = CarAd.objects.filter(user=request.user).order_by('-created_at')

    refresh = RefreshToken.for_user(request.user)
    refresh['is_staff'] = request.user.is_staff
    jwt_token = str(refresh.access_token)

    return render(request, 'cabinet.html', {
        'user_ads': user_ads,
        'jwt_token': jwt_token
    })

@login_required(login_url='/auth/')
def add_car_view(request):
    if request.method == 'POST':
        new_car = CarAd(
            user=request.user,
            transport_type=request.POST.get('transport_type'),
            brand=request.POST.get('brand'),
            model=request.POST.get('model'),
            year=request.POST.get('year'),
            mileage=request.POST.get('mileage'),
            fuel=request.POST.get('fuel'),
            transmission=request.POST.get('transmission'),
            modification=request.POST.get('modification', ''),
            location=request.POST.get('location'),
            description=request.POST.get('description'),
            color=request.POST.get('color'),
            tech_state=request.POST.get('tech_state'),
            price=request.POST.get('price')
        )
        
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            print(f"[ADD_CAR] Файл отримано: {image_file.name}")
            try:
                cloud_url = upload_image_to_cloudinary(image_file)
                if cloud_url:
                    new_car.image_url = cloud_url
                    print(f"[ADD_CAR] Успішно завантажено на Cloudinary: {cloud_url}")
                else:
                    print("[ADD_CAR] Cloudinary повернув порожній URL")
            except Exception as e:
                print(f"[ADD_CAR] Помилка завантаження на Cloudinary: {e}")
        else:
            print("[ADD_CAR] Увага: Форма відправлена без фотографії!")
            
        new_car.save()
        messages.success(request, 'Оголошення успішно додано!')
        return redirect('cabinet')

    return render(request, 'add_car.html')

@login_required(login_url='/auth/')
def delete_car_view(request, ad_id):
    ad = get_object_or_404(CarAd, id=ad_id, user=request.user)
    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Оголошення видалено!')
    return redirect('cabinet')

@login_required(login_url='/auth/')
def edit_car_view(request, ad_id):
    ad = get_object_or_404(CarAd, id=ad_id, user=request.user)
    
    if request.method == 'POST':
        ad.transport_type = request.POST.get('transport_type')
        ad.brand = request.POST.get('brand')
        ad.model = request.POST.get('model')
        ad.year = request.POST.get('year')
        ad.mileage = request.POST.get('mileage')
        ad.fuel = request.POST.get('fuel')
        ad.transmission = request.POST.get('transmission')
        ad.modification = request.POST.get('modification', '')
        ad.location = request.POST.get('location')
        ad.description = request.POST.get('description')
        ad.color = request.POST.get('color')
        ad.tech_state = request.POST.get('tech_state')
        ad.price = request.POST.get('price')

        if 'image' in request.FILES:
            image_file = request.FILES['image']
            print(f"[EDIT_CAR] Новий файл отримано: {image_file.name}")
            try:
                cloud_url = upload_image_to_cloudinary(image_file)
                if cloud_url:
                    ad.image_url = cloud_url
                    print(f"[EDIT_CAR] Успішно завантажено на Cloudinary: {cloud_url}")
                else:
                    print("[EDIT_CAR] Cloudinary повернув порожній URL")
            except Exception as e:
                print(f"[EDIT_CAR] Помилка завантаження на Cloudinary: {e}")
                
        ad.save()
        messages.success(request, 'Оголошення успішно оновлено!')
        return redirect('cabinet')

    return render(request, 'edit_car.html', {'ad': ad})

def search_view(request):
    ads = CarAd.objects.all().order_by('-created_at')

    transport_type = request.GET.get('transport_type')
    brand = request.GET.get('brand')
    year = request.GET.get('year')
    price = request.GET.get('price')
    region = request.GET.get('region')
    fuel = request.GET.get('fuel')
    transmission = request.GET.get('transmission')

    if transport_type:
        ads = ads.filter(transport_type=transport_type)
    if brand:
        ads = ads.filter(brand__icontains=brand) 
    if year:
        ads = ads.filter(year=year)
    if price:
        ads = ads.filter(price__lte=price) 
    if region:
        ads = ads.filter(location__icontains=region)
    if fuel:
        ads = ads.filter(fuel__icontains=fuel)
    if transmission:
        ads = ads.filter(transmission__icontains=transmission)

    context = {
        'ads': ads,
        'count': ads.count()
    }
    return render(request, 'search_results.html', context)

def car_detail_view(request, car_id):
    car = get_object_or_404(CarAd, id=car_id)
    price_uah = car.price * 40 
    
    context = {
        'car': car,
        'price_uah': price_uah
    }
    return render(request, 'car_detail.html', context)

def load_more_cars(request):
    offset = int(request.GET.get('offset', 4))
    limit = 4
    # Беремо наступні 4 оголошення
    cars = CarAd.objects.all().order_by('-created_at')[offset:offset+limit]
    
    # Рендеримо HTML тільки для цих 4 карток
    html = render_to_string('includes/car_card_partial.html', {'cars': cars})
    
    return JsonResponse({
        'html': html, 
        'has_more': len(cars) == limit
    })

@staff_member_required(login_url='/auth/')
def custom_admin_view(request):
    all_users = User.objects.all().order_by('-date_joined')
    all_ads = CarAd.objects.all().order_by('-created_at')
    
    context = {
        'users': all_users,
        'ads': all_ads
    }
    return render(request, 'custom_admin.html', context)

@staff_member_required(login_url='/auth/')
def admin_delete_user(request, user_id):
    if request.method == 'POST':
        user_to_delete = get_object_or_404(User, id=user_id)
        if not user_to_delete.is_superuser:
            user_to_delete.delete()
            messages.success(request, f'Користувача {user_to_delete.email} видалено!')
        else:
            messages.error(request, 'Неможливо видалити головного адміністратора!')
    return redirect('custom_admin')

@staff_member_required(login_url='/auth/')
def admin_delete_ad(request, ad_id):
    if request.method == 'POST':
        ad = get_object_or_404(CarAd, id=ad_id)
        ad.delete()
        messages.success(request, 'Оголошення примусово видалено!')
    return redirect('custom_admin')
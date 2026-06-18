from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from cars.views import (
    home_view, auth_view, cabinet_view, register_view, 
    add_car_view, delete_car_view, edit_car_view, search_view, car_detail_view,
    custom_admin_view, admin_delete_user, admin_delete_ad,
    load_more_cars,
    admin_delete_user, admin_delete_ad, admin_edit_ad
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    
    path('load-more-cars/', load_more_cars, name='load-more-cars'),
    
    path('auth/', auth_view, name='auth'),
    path('cabinet/', cabinet_view, name='cabinet'),
    path('register/', register_view, name='register'),
    path('add-car/', add_car_view, name='add_car'),
    path('admin/', admin.site.urls),
    path('moderation/edit-ad/<int:ad_id>/', admin_edit_ad, name='admin_edit_ad'),
    path('delete-car/<int:ad_id>/', delete_car_view, name='delete_car'),
    path('edit-car/<int:ad_id>/', edit_car_view, name='edit_car'),
    
    path('search/', search_view, name='search'),
    path('car/<int:car_id>/', car_detail_view, name='car_detail'),
    
    # Модерація
    path('moderation/', custom_admin_view, name='custom_admin'),
    path('moderation/delete-user/<int:user_id>/', admin_delete_user, name='admin_delete_user'),
    path('moderation/delete-ad/<int:ad_id>/', admin_delete_ad, name='admin_delete_ad'),
    
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
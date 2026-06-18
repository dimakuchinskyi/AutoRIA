from django.db import models
from django.contrib.auth.models import User

class CarAd(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='car_ads')
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Посилання на фото")
    

    transport_type = models.CharField(max_length=50, verbose_name="Тип транспорту")
    brand = models.CharField(max_length=100, verbose_name="Марка")
    model = models.CharField(max_length=100, verbose_name="Модель")
    year = models.IntegerField(verbose_name="Рік випуску")
    mileage = models.IntegerField(verbose_name="Пробіг (тис. км)")
    

    fuel = models.CharField(max_length=50, verbose_name="Тип пального", null=True, blank=True)
    transmission = models.CharField(max_length=50, verbose_name="Коробка передач", null=True, blank=True)
    
    modification = models.CharField(max_length=100, blank=True, null=True, verbose_name="Модифікація")
    location = models.CharField(max_length=150, verbose_name="Регіон / Місто")
    

    description = models.TextField(max_length=2000, verbose_name="Опис автомобіля")
    

    color = models.CharField(max_length=100, verbose_name="Колір")
    tech_state = models.CharField(max_length=100, verbose_name="Технічний стан")
    

    price = models.IntegerField(verbose_name="Ціна ($)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
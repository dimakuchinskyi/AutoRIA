from django import forms
from django.contrib import admin
from .models import CarAd
from .utils import upload_image_to_cloudinary

class CarAdAdminForm(forms.ModelForm):
    image_file = forms.ImageField(required=False, label="Завантажити фото авто")

    class Meta:
        model = CarAd
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'image_url' in self.fields:
            self.fields['image_url'].required = False

@admin.register(CarAd)
class CarAdAdmin(admin.ModelAdmin):
    form = CarAdAdminForm

    list_display = ('brand', 'model', 'year', 'price', 'location', 'created_at')
    list_filter = ('year', 'transport_type', 'location')
    search_fields = ('brand', 'model')

    def save_model(self, request, obj, form, change):
        image_file = form.cleaned_data.get('image_file')
        
        if image_file:
            print(f"Супер! Адмінка побачила файл: {image_file.name}")
            cloud_url = upload_image_to_cloudinary(image_file)
            
            if cloud_url:
                print(f"Посилання успішно отримано: {cloud_url}")
                obj.image_url = cloud_url
            else:
                print("Cloudinary повернув порожній результат.")
        else:
            print("Увага: Адмінка НЕ побачила файл при збереженні!")

        super().save_model(request, obj, form, change)
import cloudinary.uploader

def upload_image_to_cloudinary(image_file):
    if not image_file:
        print("Босс, файл не був переданий у функцію!")
        return None
    
    try:
        print(f"Спроба завантажити файл: {image_file.name}")
        response = cloudinary.uploader.upload(
            image_file,
            folder="cars_photos"
        )
        print(f"Успіх! Файл завантажено. Посилання: {response.get('secure_url')}")
        return response.get('secure_url')
    except Exception as e:
        print(f"Критична помилка Cloudinary: {e}")
        return None
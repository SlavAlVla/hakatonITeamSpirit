from authorize import authorize
import requests

# Загрузить фото 
def upload_photo(image_path):
    api = authorize.get_api()
    upload_url = api.photos.getMessagesUploadServer()["upload_url"]
    
    # Загружаем фото на сервер ВК
    try:
        with open(image_path, "rb") as file:
            response = requests.post(upload_url, files={"photo": file}).json()
    except:
        return ""

    # Сохраняем фото в альбоме сообщений
    photo_info = api.photos.saveMessagesPhoto(photo=response["photo"], 
                                             server=response["server"], 
                                             hash=response["hash"])[0]

    # Формируем attachment строку
    return f'photo{photo_info["owner_id"]}_{photo_info["id"]}'
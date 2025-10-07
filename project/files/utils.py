import requests
import hashlib
import base64,os, json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def hash_file(path, algo='sha256'):
    h = hashlib.new(algo)
    with open(path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            h.update(chunk)
    return h.hexdigest()

def list_files_by_user(user_id):
    response = requests.get(f'http://127.0.0.1:8001/file/owner/{user_id}')
    if response.status_code == 200:
        return response.json()

    else:
        return None
    
def list_files_by_group(group_id):
    response = requests.get(f'http://127.0.0.1:8001/file/group/{group_id}')
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def upload_file(user_id, file,group_id = None, description=None):
    #TODO prowywanie hash pliku z serweera i lokalnego
    url = 'http://127.0.0.1:8001/file/'
    # hash = hash_file(file)
    data = {'owner_id':user_id,'group_id':group_id,'description':description}
    files = {'file':(file.name, file.file, file.content_type)}
    response = requests.post(url, files=files,data=data)
    return response

def get_file(file_id):
    #TODO jeśli plik większy niż 25mb to tylko user moze pobrać na swój komputer

    url=f'http://127.0.0.1:8001/file/{file_id}'
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return response
    else:
        None

def delete_file(file_id):
    #TODO sprawdznie czy user ma uprawnienia do usuwanie pliku
    url=f'http://127.0.0.1:8001/file/{file_id}'
    response = requests.delete(url)
    return response
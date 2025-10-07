from django.shortcuts import render

from django.http import JsonResponse, Http404, HttpResponse, FileResponse
from .models import File, file_hash
import json, os, uuid, base64
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from cryptography.fernet import Fernet
from django.core.files.base import ContentFile
from web3 import Web3
from .blockchain import save_file_hash, get_and_verify_hash

with open('secret.key', 'rb') as f:
    FERNET_KEY =  f.read()
cipher = Fernet(FERNET_KEY)


def list_by_owner(request, owner_id):
    if request.method == 'GET':
        try:
            files = File.objects.filter(owner_id=owner_id)
            data = list()
            for f in files:
                file_data = dict(id=f.id,
                            name=f.name,
                            size=f.file.size,
                            type=os.path.splitext(f.name)[1],
                            owner_id=f.owner_id,
                            group_id=f.group_id,
                            description=f.description,
                            is_archieved=f.is_archieved,
            
                            date = f.date
                            )
                data.append(file_data)

            # data = {}
            # data["names"] = [os.path.basename(f.name) for f in files]
            # data["size"] = [f.file.size for f in files]
            # data["type"] = [os.path.splitext(f.file.name)[1] for f in files]
            # data["id"] =[f.id for f in files]
            # data["owner_id"] = [f.owner_id for f in files]
            # data["group_id"] = [f.group_id for f in files]
            # data["is_archieved"] = [f.is_archieved for f in files]
            return JsonResponse(data, safe=False)
        except File.DoesNotExist:
            raise Http404()
        
def list_by_group(request, group_id):
    if request.method == 'GET':
        try:
            files = File.objects.filter(group_id=group_id)
            data = list()
            for f in files:
                file_data = dict(id=f.id,
                            name=f.name,
                            size=f.file.size,
                            type=os.path.splitext(f.name)[1],
                            owner_id=f.owner_id,
                            description=f.description,
                            group_id=f.group_id,
                            is_archieved=f.is_archieved,
                            date = f.date
                            )
                data.append(file_data)
            # data = {}
            # data["names"] = [os.path.basename(f.name) for f in files]
            # data["size"] = [f.file.size for f in files]
            # data["type"] = [os.path.splitext(f.file.name)[1] for f in files]
            # data["id"] =[f.id for f in files]
            # data["owner_id"] = [f.owner_id for f in files]
            # data["group_id"] = [f.group_id for f in files]
            # data["is_archieved"] = [f.is_archieved for f in files]
            return JsonResponse(data, safe=False)
        except File.DoesNotExist:
            raise Http404()



@csrf_exempt
def file(request, file_id):
    if request.method == 'GET':
        obj = get_object_or_404(File, pk=file_id)
        try:
            with open(obj.file.path, 'rb') as file:
                is_archieved=False
                try:
                    is_archieved = get_and_verify_hash(str(obj.eth_id), Web3.to_bytes(hexstr=obj.hash))
                except Exception as e:
                    print(e)
                    print('can not read blockchain')


                enc_data = file.read()
                dec_data = cipher.decrypt(enc_data)
                body = ContentFile(dec_data)
                response = FileResponse(body)
                meta = {'name':obj.name,
                        'id':obj.id,
                        'type':os.path.splitext(obj.name)[1],
                        'group_id':obj.group_id,
                        'hash':obj.hash,
                        'is_archieved':is_archieved,
                        'date':obj.date,
                        'description':obj.description}
                response['X-File-MetaData'] = json.dumps(meta, cls=DjangoJSONEncoder)
                return response
        except FileNotFoundError:
            raise Http404("Plik nie został znaleziony")
    elif request.method == 'DELETE':
        try:
            obj = File.objects.filter(id=file_id).first()
            obj.delete()
            return HttpResponse()
        except:
            raise Http404()

@csrf_exempt
def add_file(request):
    if request.method == 'POST' and request.FILES:
        f = request.FILES.get('file')
        if f:
            data = f.read()
            enc_data = cipher.encrypt(data)
            owner_id = request.POST.get('owner_id')
            group_id = request.POST.get('group_id')
            description = request.POST.get('description')
            if not owner_id or not group_id:
                raise Http404()          
            encrypted_file = ContentFile(enc_data, name='name')
            obj = File.objects.create(
                    name=os.path.basename(f.name),
                    owner_id=owner_id,
                    group_id=group_id,
                    description=description
            )
            obj.save()
            obj.file.save(encrypted_file.name, encrypted_file)
            try:
                save_file_hash(str(obj.eth_id),Web3.to_bytes(hexstr=obj.hash))
            except Exception as e:
                print(e)
                print('can not save hash to blockchain')

        else:
            raise Http404()
        return HttpResponse()
    else:
        raise Http404()

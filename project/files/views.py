from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from . import utils
from groups.utils import get_user_space
import base64, json, os
from timeline.models import Event
import traceback

# Create your views here.
@login_required
def upload(request, group_id = None):
    if request.method == "POST" and request.FILES:
        try:
            file = request.FILES['file']
            if file.size > 25*1024*1024:
                return HttpResponseBadRequest("Maksymalna wielkość pliku to 25 mB")
            desc = request.POST.get('description')
            if not desc:
                desc = '-'
            if not group_id:
                group_id = get_user_space(request.user)
            response = utils.upload_file(request.user.user_id, file=file, group_id=group_id, description=desc)
            if response.status_code == 400:
                return HttpResponseBadRequest("Błąd")
            elif response.status_code == 404:
                return HttpResponseBadRequest("Błąd")
            else:
                e = Event.objects.create(email=request.user.email, group_id=group_id, msg=f"dodał nowy plik {file.name}", type='add')
                e.save()
                redirect_url = request.META.get('HTTP_REFERER', '/')
                response = HttpResponse()
                response['HX-Redirect'] = redirect_url
                return response
        except:
            return HttpResponseBadRequest("Błąd")
        
# @login_required
# def upload(request, group_id):
#     if request.method == "POST":
#         file = request.FILES['file']
#         response = utils.upload_file(user_id= request.user.user_id,file=file,group_id=group_id)
#         if response.status_code == 400:
#             return HttpResponse('file uploading error!')
#         elif response.status_code == 404:
#             return HttpResponse('blad wewnetrzny serwera')
#         else:
#             return HttpResponse(f'przesylanie pliku zakonczone kod <{response.status_code}>')

@login_required
def get_file(request, file_id):
    if request.method == "GET":
        response = utils.get_file(file_id)
        # print(response.text)
        if response.status_code == 200:
            meta = json.loads(response.headers.get('X-File-MetaData'))
            file_content = b''.join(chunk for chunk in response.iter_content(chunk_size=8192) if chunk)
            print(meta['type'])
            if meta['type'] == '.txt' or meta['type'] == '.py' or meta['type'] == '.cpp':
                file_content = file_content.decode('utf-8')
            elif meta['type'] =='.pdf':
                file_content = base64.b64encode(file_content).decode('utf-8')

            return render(request, 'base/read_file.html',{'body': file_content,'meta':meta})
        else:
            raise Http404()

    else:
        raise Http404()
    
@login_required
def download_file(request, file_id):
    if request.method == "GET":
        response = utils.get_file(file_id)
        if response.status_code == 200:
            meta = json.loads(response.headers.get('X-File-MetaData'))
            file_content = b''.join(chunk for chunk in response.iter_content(chunk_size=8192) if chunk)

            response = HttpResponse(file_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{meta["name"]}"'
            return response
        else:
            raise Http404()
    else:
        raise Http404()
    
@login_required
def delete_file(request, file_id, group_id=None, file_name=None):
    if request.method == "GET":
        response = utils.delete_file(file_id)
        if response.status_code != 200:
            request.session['error_message'] = 'nie udalo sie usunac pliku, sprubuj ponownie pozniej'
            return redirect(f'{request.META.get('HTTP_REFERER')}')
        else:
            if group_id and file_name:
                e = Event.objects.create(email=request.user.email, group_id=group_id, msg=f"usunał plik o nazwie {file_name}", type='delete')
                e.save()
            return redirect(f'{request.META.get('HTTP_REFERER')}')
    else:
        raise Http404()



@login_required
def save_file(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code_content = data.get('text', '')
            file_type = data.get('file_type', '.py')
            
            with open(f'saved_code{file_type}', 'w') as f:
                f.write(code_content)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Kod został zapisany'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'message': 'Nieprawidłowa metoda żądania'
    }, status=405)
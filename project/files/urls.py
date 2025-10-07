from django.urls import path
from . import views


urlpatterns = [
    path('upload', views.upload, name='upload'),
    path('upload/<uuid:group_id>', views.upload, name='upload_by_group'),
    path('<uuid:file_id>', views.get_file, name='get_file'),
    path('delete/<uuid:file_id>', views.delete_file, name='delete_file'),
    path('delete/<uuid:file_id>/<uuid:group_id>/<str:file_name>', views.delete_file, name='delete_file_by_group'),
    path('save', views.save_file, name='save_file'),
    path('download/<uuid:file_id>', views.download_file, name='download'),
    ]

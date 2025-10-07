from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_file, name="add_file"), 
    path('<uuid:file_id>', views.file, name='file'),
    path('owner/<uuid:owner_id>', views.list_by_owner, name='list_by_owner'),
    path('group/<uuid:group_id>', views.list_by_group, name='list_by_group'),
    ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.show, name='show_groups'),
    path('detail/<uuid:group_id>', views.detail, name='group_detail'),
    path('add',views.add, name='add_member'),
    path('edit', views.edit, name="group_edit"),
    path('update', views.update, name='group_update_info'),
    path('delete/<uuid:group_id>',views.delete, name='delete_group'),
    path('delete/<uuid:group_id>/<str:email>', views.delete_member, name='delete_member')
]

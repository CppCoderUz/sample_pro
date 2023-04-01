from django.urls import path

from . import views




# namespace='faculty'
# main_url = 'faculty'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # yo'nalishlar
    path('direction/add', views.add_direction, name='add_direction'),
    path('direction/all', views.all_direction, name='all_direction'),
    path('direction/change/<int:pk>', views.change_direction, name='change_direction'),
    path('direction/delete/<int:pk>', views.delete_direction, name='delete_direction'),

    # guruhlar
    path('group/add', views.add_group, name='add_group'),
    path('group/all', views.all_group, name='all_group'),
    path('group/change/<int:pk>', views.change_group, name='change_group'),
    path('group/delete/<int:pk>', views.delete_group, name='delete_group'),

    # o'quv rejalar ro'yxati
    path('study_plan/all', views.study_plan_list, name='study_plan_list'),
    path('study_plan/detail/<int:direction_id>/semestr/<int:semestr_id>', views.study_plan_detail, name='study_plan_detail'),


    # ajax
    path('ajax/<slug:token>/science_list/', views.ajax_science_list, name='ajax_science_list'),
]
from django.urls import path

from education_department import views



# namespace='education_department'
# main_url='department/'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('faculty/list', views.list_faculty, name='list_faculty'),
    path('cafedra/list', views.list_cafedra, name='list_cafedra'),
    path('cafedra/add', views.add_cafedra, name='add_cafedra'),
    path('faculty/add', views.add_faculty, name='add_faculty'),
    path('user/add', views.add_user, name='add_user'),
    path('user/all', views.all_users, name='all_users'),
]
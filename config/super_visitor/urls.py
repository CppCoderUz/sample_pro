


from django.urls import path
from super_visitor.views import (
    login_view,
    logout_view,
)


# namespace='auth_views'
# main_url=''

urlpatterns = [
    path('', login_view, name='login'),
    path('auth/logout', logout_view, name='logout'),
]
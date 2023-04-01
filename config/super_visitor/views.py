from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import login, logout, authenticate

from super_visitor.utils import is_faculty_manager, is_cafedra_manager, is_supervisitor, is_department_employee




def login_view(request: WSGIRequest, *args, **kwargs):
    error_msg = ''
    HOME_PAGE_LIST = [
        'education_department:dashboard',
        'faculty:dashboard',
    ]
    next_page = request.GET.get('next', None)

    if request.user.is_authenticated:
        if is_department_employee(request.user):
            return redirect(HOME_PAGE_LIST[0])
        elif is_faculty_manager(request.user):
            return redirect(HOME_PAGE_LIST[1])
        else:
            pass


    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request=request, user=user)
                if next_page is not None:
                    return redirect(next_page)
                else:
                    if is_department_employee(user):
                        return redirect(HOME_PAGE_LIST[0])
                    elif is_faculty_manager(user):
                        return redirect(HOME_PAGE_LIST[1])
                    else:
                        logout(request)
                        error_msg = 'login yoki parol xato'
            else:
                error_msg = 'Login yoki parol xato'
        else:
            error_msg = ''

    return render(request, 'login.html', {
        'error_msg': error_msg,
    })


def logout_view(request):
    logout(request)
    return redirect('auth_views:login')
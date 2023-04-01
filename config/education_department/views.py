from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import hashers
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect




from super_visitor.utils import (
    education_department_template_name as _, 
    get_object_or_none, 
    get_data,
    department_only
)
from super_visitor.models import User
from super_visitor import groups


from faculty.models import Faculty, FacultyManager
from cafedra.models import Cafedra, CafedraManager


@login_required(login_url='auth_views:login')
@department_only
def dashboard(request: WSGIRequest):
    return render(request, _('index'), {
        'page_title': "Bosh sahifa",
    })

@login_required(login_url='auth_views:login')
@department_only
def list_faculty(request: WSGIRequest):
    facultys = Faculty.objects.all()
    return render(request, _('list_faculty'), {
        'page_title': 'Fakultetlar ro\'yxati',
        'data': facultys,
    })

@login_required(login_url='auth_views:login')
@department_only
def list_cafedra(request: WSGIRequest):
    cafedras = Cafedra.objects.all()
    return render(request, _('list_cafedra'), {
        'page_title': "Kafedralar ro'yxati",
        'data': cafedras,
    })

@login_required(login_url='auth_views:login')
@department_only
def add_cafedra(request: WSGIRequest):
    error_msg = ''
    if request.method == 'POST':
        name = request.POST.get('cafedra_name', False)
        faculty = request.POST.get('faculty_id', False)
        manager = request.POST.get('manager_id', False)
        try:
            faculty = Faculty.objects.get(pk=faculty) 
        except:
            error_msg = 'Fakultetni tanlang'
            faculty = None
        try:
            manager = CafedraManager.objects.get(id=manager)
        except:
            error_msg = 'Mudirni tanlang'
            manager = None
        
        if name and faculty and manager:
            Cafedra.objects.create(name=name, faculty=faculty, manager=manager)
            return redirect('education_department:list_cafedra')
    query_faculty = Faculty.objects.all()
    query_mudir = CafedraManager.objects.filter(is_manager=False)
    return render(request, _('add_cafedra'), {
        'page_title': 'Kafedra qo\'shish',
        'query_faculty': query_faculty,
        'query_mudir': query_mudir,
        'error_msg': error_msg,
    })


@login_required(login_url='auth_views:login')
@department_only
def add_faculty(request: WSGIRequest):
    query_dekan = FacultyManager.objects.filter(is_manager=False)
    error_msg = ''
    if request.method == 'POST':
        faculty_name = request.POST.get('faculty_name', False)
        manager = request.POST.get('manager_id', False)
        try:
            manager = FacultyManager.objects.get(id=manager)
        except:
            error_msg = 'Dekanni tanlang !'
            manager = False
        if faculty_name and manager:
            Faculty.objects.create(
                manager=manager,
                name=faculty_name
            )
            return redirect('education_department:list_faculty')

    return render(request, _('add_faculty'), {
        'page_title': 'Fakultet qo\'shish',
        'query_dekan': query_dekan,
        'error_msg': error_msg
    })

@login_required(login_url='auth_views:login')
@department_only
def add_user(request: WSGIRequest):
    error_msg = ''
    LIST_LAVOZIM = ['65b4y4b7t4nh587', '45nvt547y54nt8h']
    data = {}
    if request.method == 'POST':
        lavozim = request.POST.get('lavozim_id', None)
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password_1 = request.POST.get('password_1', '')
        password_2 = request.POST.get('password_2', '')

        data = get_data(first_name = first_name, last_name = last_name, username = username,
            email = email, password_1 = password_1, password_2 = password_2)
        
        if lavozim in LIST_LAVOZIM and first_name and last_name and username and \
                        email and password_1 and password_2:
            user = get_object_or_none(model=User, username=username)
            if user is not None:
                error_msg = ''' Kiritilgan xodim ID avvaldan mavjud. Iltimos boshqa ID kiriting '''
            else:
                if not (password_1 == password_2):
                    error_msg = ''' Iltimos parolni to'g'ri kiriting '''
                else:
                    user = User()
                    user.password = hashers.make_password(password=password_1)
                    user.username = username
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()

                    if lavozim == LIST_LAVOZIM[0]:
                        CafedraManager.objects.create(user=user)
                    else:
                        FacultyManager.objects.create(user=user)
                    return redirect('education_department:dashboard')

        else:
            error_msg = 'Ma\'lumotlarni to\'liq kiriting'

    return render(request, _('add_user'), {
        'page_title': 'Nazoratchi qo\'shish',
        'error_msg': error_msg,
        'data': data,
    })


@login_required(login_url='auth_views:login')
@department_only
def all_users(request: WSGIRequest):
    data = User.objects.filter(is_staff=True, is_active=True, is_superuser=False).all()[:]
    
    new_data = []
    for user in data:
        m = get_object_or_none(user.groups, id=groups.MUDIR.id)
        d = get_object_or_none(user.groups, id=groups.DEKAN.id)
        
        if m is not None and d is not None:
            pass  
        elif m is not None:
            new_data.append({'user':user,'lavozim':'Mudir'})
        elif d is not None:
            new_data.append({'user':user,'lavozim':'Dekan'})
    return render(request, _('all_users'), {
        'page_title': 'Nazoratchilar ro\'yxati',
        'data': new_data
    })
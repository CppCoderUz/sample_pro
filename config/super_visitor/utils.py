from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.db import models

from super_visitor.models import User, SuperVisitor
from super_visitor import groups

from education_department.models import EmployeeDepartment
from faculty.models import FacultyManager, Faculty
from cafedra.models import CafedraManager


def _get_queryset(model):
    ''' model ichidan querysetni olish '''
    if hasattr(model, "_default_manager"):
        return model._default_manager.all()
    return model


def get_object_or_none(model, *args, **kwargs):
    ''' Yoki obyektni oladi, yoki None '''
    queryset = _get_queryset(model)
    if not hasattr(queryset, "get"):
        raise ValueError(
            "Birinchi qiymat Model bo'lishi kerak !"
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def get_status_user(user : User, group: groups.Group, model: models.Model):
    if user.is_active and user.is_staff:
        search_group = get_object_or_none(user.groups, name=group.name) 
        search_object = get_object_or_none(model, user__id=user.id)
        if search_group and search_object:
            return True
        else:
            return False
    else:
        return False


def is_supervisitor(user : User):
    """ Userni super_visitor ekanligini tekshirish """
    return get_status_user(user=user, group=groups.SUPER_VISITOR, model=SuperVisitor)

def is_faculty_manager(user : User):
    b = get_status_user(user=user, group=groups.DEKAN, model=FacultyManager)
    manager = get_object_or_none(FacultyManager, user_id=user.pk, is_manager=True)
    faculty = get_object_or_none(Faculty, manager_id=manager.pk)
    if b and faculty:
        return True
    else:
        return False

def is_cafedra_manager(user : User):
    return get_status_user(user=user, groups=groups.MUDIR, model=CafedraManager)

def is_department_employee(user: User):
    return get_status_user(user=user, group=groups.EMPLOYEE_DEPARTMENT, model=EmployeeDepartment)

def education_department_template_name(file_name: str):
    return 'education_department/%s.html' % file_name 

def faculty_template_name(file_name: str):
    return 'faculty/%s.html' % file_name



def get_data(*args, **kwargs):
    return kwargs






def department_only(func):
    def wrapper_func(request: WSGIRequest, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('auth_views:login')
        if is_department_employee(user=user):
            return func(request, *args, **kwargs)
        else:
            raise Http404()
    return wrapper_func

def faculty_manager_only(func):
    def wrapper_func(request: WSGIRequest, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('auth_views:login')
        if is_faculty_manager(user=user):
            return func(request, *args, **kwargs)
        else:
            raise Http404()
    return wrapper_func


def cafedra_manager_only(func):
    def wrapper_func(request: WSGIRequest, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('auth_views:login')
        if is_cafedra_manager(user=user):
            return func(request, *args, **kwargs)
        else:
            raise Http404()
    return wrapper_func
        

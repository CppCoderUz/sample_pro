from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.utils import timezone
from django.forms import inlineformset_factory, CharField
from django import forms
from django.db.models import Q
from django.contrib.auth.decorators import login_required


from super_visitor.utils import faculty_template_name as _, faculty_manager_only
from study_plan.models import (
    Direction, 
    SmallGroup, 
    Cafedra, 
    CafedraManager,
    Faculty, 
    FacultyManager,
    ProfessionalPractice,
    Science,
    ScienceStudyPlan,
    SemestrStudyPlan,
)

from .utils import (
    get_data, 
    get_object_or_none,
)
from .forms import DirectionForm, SmallGroupForm, CustomTextField

from students.models import Student

@login_required(login_url='auth_views:login')
@faculty_manager_only
def dashboard(request: WSGIRequest):
    return render(request, _('home'), {
        'page_title': ''' Bosh sahifa '''
    })


@login_required(login_url='auth_views:login')
@faculty_manager_only
def add_direction(request: WSGIRequest):
    form = DirectionForm()
    data = get_data(request)
    if request.method == 'POST':
        form = DirectionForm(data=request.POST)
        if form.is_valid:
            object = form.save(commit=False)
            object.faculty = data['faculty']
            object.year = timezone.now().year
            object.save()
            return redirect('faculty:all_direction')
        else:
            pass
    return render(request, _('add_direction'), {
        'page_title': ''' Yangi yo'nalish yaratish ''',
        'form': form,
    })


@login_required(login_url='auth_views:login')
@faculty_manager_only
def change_direction(request: WSGIRequest, pk):
    object = get_object_or_none(Direction, pk=pk)
    if object is None:
        return error_404(request)
    form = DirectionForm(instance=object)
    data = get_data(request)
    if request.method == 'POST':
        form = DirectionForm(data=request.POST, instance=object)
        if form.is_valid:
            object = form.save(commit=False)
            object.faculty = data['faculty']
            object.year = timezone.now().year
            object.save()
            return redirect('faculty:all_direction')
        
    return render(request, _('change_direction'), {
        'page_title': ''' Yo'nalish ma'lumotini tahrirlash ''',
        'form': form,
        'object': object,
    })


@login_required(login_url='auth_views:login')
@faculty_manager_only
def delete_direction(request: WSGIRequest, pk):
    object = get_object_or_none(Direction, pk=pk)
    if object is not None:
        object.delete()
    return redirect('faculty:all_direction')




@login_required(login_url='auth_views:login')
@faculty_manager_only
def all_direction(request: WSGIRequest):
    data = get_data(request)
    object = Direction.objects.filter(faculty_id=data['faculty'].pk)
    return render(request, _('all_direction'), {
        'page_title': 'Barcha yo\'nalishlar',
        'object': object,
        'data': data,
    })


@login_required(login_url='auth_views:login')
@faculty_manager_only
def add_group(request: WSGIRequest):
    data = get_data(request)
    form = SmallGroupForm(faculty=data['faculty'])
    if request.method == 'POST':
        form = SmallGroupForm(data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('faculty:all_group')
    
    return render(request, _('add_group'), {
        'page_title': 'Yangi guruh qo\'shish',
        'form': form,
    })



@login_required(login_url='auth_views:login')
@faculty_manager_only
def change_group(request: WSGIRequest, pk):
    object = get_object_or_none(SmallGroup, pk=pk)
    if object is None:
        return error_404(request)
    
    data = get_data(request)
    form = SmallGroupForm(instance=object,faculty=data['faculty'])

    students = Student.objects.filter(group__pk=object.pk)
    OrderFormSet = inlineformset_factory(
        SmallGroup, Student, 
        fields=('first_name', 'last_name', 'username'), extra=0,
        field_classes={
            'first_name': CustomTextField,
            'last_name': CustomTextField,
            'username': CustomTextField,
        }
    )
    formset = OrderFormSet(instance=object, queryset=students)

    if request.method == 'POST' and request.POST.get('status_update', False):
        form = SmallGroupForm(data=request.POST, instance=object)
        if form.is_valid:
            form.save()
            return redirect('faculty:all_group')
        
    elif request.method == 'POST' and request.POST.get('students_list', False):
        sum_objects = request.POST.get('sum_students')

        for i in range(int(sum_objects) + 1):
            username = request.POST.get(f"student_set-{i}-username", None)
            last_name = request.POST.get(f"student_set-{i}-last_name", None)
            first_name = request.POST.get(f"student_set-{i}-first_name", None)
            
            if username and last_name and first_name:
                student = get_object_or_none(Student, username=username)
                if student is not None:
                    student.first_name = first_name
                    student.last_name = last_name
                    student.username = username
                    student.group = object
                    student.save()
                else:
                    Student.objects.create(first_name=first_name, last_name=last_name, username=username, group=object)

    return render(request, _('change_group'), {
        'page_title': ''' Guruh ma'lumotini o'zgartirish sahifasi ''',
        'form': form,
        'object': object,
        'sum_students': students.count(),
        'students': students,
        'formset_students': formset,
    })



@login_required(login_url='auth_views:login')
@faculty_manager_only
def all_group(request: WSGIRequest):
    data = get_data(request)
    object = SmallGroup.objects.filter(direction__faculty__pk=data['faculty'].pk)

    return render(request, _('all_group'), {
        'page_title': 'Bacha guruhlar',
        'object': object,
    })



@login_required(login_url='auth_views:login')
@faculty_manager_only
def delete_group(request: WSGIRequest, pk):
    object = get_object_or_none(SmallGroup, pk=pk)
    if object is not None:
        object.delete()
    return redirect('faculty:all_group')
    

@login_required(login_url='auth_views:login')
@faculty_manager_only
def study_plan_list(request: WSGIRequest):
    data = get_data(request)
    directions = Direction.objects.filter(faculty__id=data['faculty'].pk).all()
    return render(request, _('study_plan_list'), {
        'page_title': ''' . ''',
        'directions': directions,
    })

@login_required(login_url='auth_views:login')
@faculty_manager_only
def study_plan_detail(request: WSGIRequest, direction_id, semestr_id):
    data = get_data(request)
    direction : Direction = get_object_or_none(Direction, pk=direction_id)
    if direction is None:
        return error_404(request)
    if direction.semester_number < semestr_id:
        return error_404(request)

    object = get_object_or_none(SemestrStudyPlan, semester_number=semestr_id, direction__id=direction_id)
    
    return render(request, _('study_plan_detail'), {
        'sum_rows': 10,
        'semestr_number': semestr_id,
        'direction': direction,
        'page_title': '%s o\'quv rejasi'%direction,
    })



@login_required(login_url='auth_views:login')
@faculty_manager_only
def error_404(request: WSGIRequest):
    return render(request, _('404'), {}, status=404)




@login_required(login_url='auth_views:login')
@faculty_manager_only
def ajax_science_list(request: WSGIRequest, token):
    # metod POST bo'lishi shart
    if not request.method == 'POST':
        raise Http404()

    # token mavjud va u URL bilan birgalikda kelishi kerak
    csrf_token = request.POST.get('csrfmiddlewaretoken') 
    if not (len(csrf_token) == 64 and csrf_token == token):
        raise Http404()
    
    empty_dict = {}
    empty_list = []
    filter = request.POST.get('filter', None)
    if filter is not None:
        object_list = Science.objects.filter(name__contains=filter).all()
    else:
        object_list = Science.objects.all()

    for object in object_list:
        empty_list.append({'id': object.id, 'text': object.name})
    empty_dict['rezult'] = empty_list
    empty_dict["sum_objects"] = object_list.count()
    return JsonResponse(empty_dict)
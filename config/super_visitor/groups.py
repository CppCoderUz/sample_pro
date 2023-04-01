
from django.contrib.auth.models import Group


SUPER_VISITOR       = Group.objects.get(name='super_visitor')
EMPLOYEE_DEPARTMENT = Group.objects.get(name='employee_department')
MUDIR               = Group.objects.get(name='mudir')
DEKAN               = Group.objects.get(name='dekan')
DEFAULT             = Group.objects.get(name='default')

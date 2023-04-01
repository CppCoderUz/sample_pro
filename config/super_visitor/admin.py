from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _



# mahalliy funksiya va classlar
from super_visitor.models import User, SuperVisitor, Logins
from education_department.models import EmployeeDepartment
from faculty.models import FacultyManager, Faculty
from cafedra.models import CafedraManager, Cafedra
from study_plan.models import Direction, Science, ProfessionalPractice, ScienceStudyPlan, SemestrStudyPlan, SmallGroup
from students.models import Student

# super visitor dasturini ichidagi modellar
class MainUserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (_("Kirish huquqlari"), {"fields": ("username", "password")}),
        (_("Shaxsiy ma'lumotlar"), {"fields": ("first_name", "last_name", "email", "image")}),
        (_("Huquqlar"),{"fields": ("is_active","is_staff","is_superuser","groups",),},),
        (_("Muhim vaqtlar"), {"fields": ("last_login", "date_joined")}),
    )
admin.site.register(User, MainUserAdmin)

class SuperVisitorAdmin(admin.ModelAdmin):
    list_display = ['user', 'pk']
admin.site.register(SuperVisitor, SuperVisitorAdmin)

class LoginsAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'ip_adress', 'role', 'status', 'date_time']
admin.site.register(Logins, LoginsAdmin)





# O'quv bo'limi modellari
class EmployeeDepartmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'pk']
admin.site.register(EmployeeDepartment, EmployeeDepartmentAdmin)





# Fakultet modellari
class FacultyManagerAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_manager', 'pk']
admin.site.register(FacultyManager, FacultyManagerAdmin)

class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager']
admin.site.register(Faculty, FacultyAdmin) 






# Kafedra modellari
class CafedraManagerAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_manager', 'pk']
admin.site.register(CafedraManager, CafedraManagerAdmin)

class CafedraAdmin(admin.ModelAdmin):
    list_display = ['name', 'faculty', 'manager']
admin.site.register(Cafedra, CafedraAdmin)



# study_plan modellari
admin.site.register(Science)
admin.site.register(ScienceStudyPlan)
admin.site.register(Direction)
admin.site.register(ProfessionalPractice)
admin.site.register(SemestrStudyPlan)
admin.site.register(Student)
admin.site.register(SmallGroup)


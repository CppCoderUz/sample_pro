from django.core.handlers.wsgi import WSGIRequest
from super_visitor.utils import is_faculty_manager, get_object_or_none

from faculty.models import Faculty, FacultyManager







def get_data(request: WSGIRequest):
    ''' Dekanning ma'lumotlarini yig'ib beradigan funksiya '''

    user = request.user
    if not user.is_authenticated:
        return None
    if not is_faculty_manager(user=user):
        return None
    
    manager = get_object_or_none(FacultyManager, user_id=user.pk, is_manager=True)
    if manager is None: 
        return None
    
    faculty = get_object_or_none(Faculty, manager_id=manager.pk)
    return {
        'faculty': faculty,
        'manager': manager,
    }

    

    

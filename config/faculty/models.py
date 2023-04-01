from django.db import models




from super_visitor.models import User
from super_visitor.groups import DEKAN


class FacultyManager(models.Model):
    """ Dekanlar ma'lumotlar bazasi uchun model """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.user) + [' Tanlangan' if self.is_manager else ' Tanlanmagan'][0]

    def save(self, *args, **kwargs):
        self.user.groups.add(DEKAN)
        self.user.is_staff = True
        self.user.save()
        super(FacultyManager, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.groups.remove(DEKAN)
        super(FacultyManager, self).delete(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Dekan'
        verbose_name_plural = '1. Dekanlar'




class Faculty(models.Model):
    """ Fakultetlar ma'lumotlar ba'zasi uchun model """
    manager = models.OneToOneField(FacultyManager, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=150)

    def save(self, *args, **kwargs):
        if self.manager:
            self.manager.is_manager = True
            self.manager.save()
        super(Faculty, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.manager:
            self.manager.is_manager = False
            self.manager.save()
        super(Faculty, self).delete(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Fakultet'
        verbose_name_plural = '2. Fakultetlar'






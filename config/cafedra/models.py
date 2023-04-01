from django.db import models



from super_visitor.models import User
from super_visitor.groups import MUDIR

from faculty.models import Faculty


class CafedraManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.user.groups.add(MUDIR)
        self.user.is_staff = True
        self.user.save()
        super(CafedraManager, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.user.groups.remove(MUDIR)
        super(CafedraManager, self).delete(*args, **kwargs)
    
    def __str__(self) -> str:
        return str(self.user) + [' (Tanlangan)' if self.is_manager else ' (Tanlanmagan)'][0]

    class Meta:
        verbose_name = 'Mudirlar'
        verbose_name_plural = '1. Mudirlar'




class Cafedra(models.Model):
    manager = models.ForeignKey(CafedraManager, on_delete=models.SET_NULL, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def save(self, *args, **kwargs):
        if self.manager:
            self.manager.is_manager = True
            self.manager.save()
        super(Cafedra, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.manager:
            self.manager.is_manager = False
            self.manager.save()
        super(Cafedra, self).delete(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Kafedra'
        verbose_name_plural = '2. Kafedralar'



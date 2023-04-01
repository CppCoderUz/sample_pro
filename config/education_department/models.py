from django.db import models




from super_visitor.models import User
from super_visitor.groups import EMPLOYEE_DEPARTMENT



class EmployeeDepartment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=150, verbose_name="Lavozimi")

    def __str__(self) -> str:
        return str(self.user)
    
    def save(self, *args, **kwargs):
        self.user.groups.add(EMPLOYEE_DEPARTMENT)
        super(EmployeeDepartment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "O'quv bo'limi nazoratchisi"
        verbose_name_plural = "1. O'quv bo'limi nazoratchilari"    



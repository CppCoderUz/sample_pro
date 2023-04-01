from django.db import models





class Student(models.Model):
    ''' Studentlar ma'lumotlar bazasi uchun model '''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    group = models.ForeignKey(to='study_plan.SmallGroup', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return '%s %s'%(self.last_name, self.first_name)
    
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = '1. Studentlar'
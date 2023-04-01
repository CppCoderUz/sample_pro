from django.db import models
from django.contrib.auth.models import AbstractUser, Group

from super_visitor import groups

class User(AbstractUser):
    """ Asosiy foydalanuvchilar uchun ma'lumotlar bazasi modeli """
    image = models.ImageField(upload_to='images/avatar', null=True, blank=True)

    def __str__(self) -> str:
        return '%s %s'%(self.last_name, self.first_name)
    
    def save(self, *args, **kwargs):
        if not (self.pk == 1):
            super(User, self).save(*args, **kwargs)
            self.groups.add(groups.DEFAULT)
        

    def delete(self, *args, **kwargs):
        if not (self.pk == 1):
            super(User, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = '1. Userlar'



class SuperVisitor(models.Model):
    """ Super Kuzatuvchilar uchun ma'lumotlar bazasi modeli """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.user.groups.add(groups.SUPER_VISITOR)
        self.user.is_staff = True
        self.user.save()
        super(SuperVisitor, self).save(*args, **kwargs)

    def __str__(self) -> str:
        user = self.user
        return '%s %s (%s)'%(user.last_name, user.first_name, user.username)
    
    class Meta:
        verbose_name = 'Super Visitor'
        verbose_name_plural = '2. Super kuzatuvchilar'



class Logins(models.Model):
    """ Foydalanuvchilarning login qilgan vaqtlarini yozib borish uchun model """
    STATUS_CHOICES = (
        ("success", "success"),
        ("warning", "warning"),
    )
    ROLE = (
        ("super_visitor", "super_visitor"),
        ("dekan", "dekan"),
        ("mudir", "mudir"),
        ("education_officer", "education_officer"),
        ("other", "other"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    ip_adress = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE, default="other")

    def __str__(self):
        return '%s %s %s'%(self.user.username, str(self.date_time), self.status)
    
    class Meta:
        verbose_name = 'Login'
        verbose_name_plural = '3. Logins'
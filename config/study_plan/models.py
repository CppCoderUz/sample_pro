from django.db import models



from super_visitor.models import User
from faculty.models import Faculty, FacultyManager
from cafedra.models import Cafedra, CafedraManager



class Science(models.Model):
    ''' Barcha fanlar modeli '''
    cafedra = models.ForeignKey(Cafedra, on_delete=models.CASCADE, verbose_name='Kafedrasi')
    name = models.CharField(max_length=100, verbose_name='Fan nomi')

    def __str__(self) -> str:
        return '%s %s'%(self.name, self.cafedra.name)

    class Meta:
        verbose_name = 'Fan'
        verbose_name_plural = '1. Fanlar'



class Direction(models.Model):
    ''' Yo'nalish modeli '''
    LANGUAGE_CHOICES = (
        ('uzbek', 'O\'zbek'),
        ('rus', 'Rus'),
        ('other', 'Boshqa')
    )
    STUDY_FORM_CHOICES = (
        ('kunduzgi', 'kunduzgi'),
        ('kechki', 'kechki'),
        ('sirtqi', 'sirtqi'),
    )

    name = models.CharField(max_length=150, verbose_name='Yo\'nalish nomi')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name='Fakulteti')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, verbose_name='Ta\'lim tili')
    study_form = models.CharField(max_length=10, choices=STUDY_FORM_CHOICES, verbose_name='Ta\'lim shakli')
    code = models.CharField(max_length=30,null=True, blank=True, verbose_name='Yo\'nalish kodi')

    year = models.IntegerField(verbose_name='Qabul qilingan yili')
    semester_number = models.IntegerField(default=8, verbose_name='Semestr soni')
    

    def __str__(self) -> str:
        return '%s [ %s / %s ]'%(self.name, self.language, self.study_form)
    
    class Meta:
        verbose_name = 'Yo\'nalish'
        verbose_name_plural = '2. Barcha yo\'nalishlar'


class SemestrStudyPlan(models.Model):
    ''' Bitta semestr uchun o'quv reja modeli '''
    semester_number = models.IntegerField(verbose_name='Semestr raqami')
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name='Yo\'nalish')
    
    def __str__(self) -> str:
        return '%s (%s)'%(self.direction.name, self.semester_number)

    class Meta:
        verbose_name = 'Semestr rejasi'
        verbose_name_plural = '3. Semestr rejalari'


class ScienceStudyPlan(models.Model):
    ''' fanlar rejasi '''
    EXAM_TYPE = (
        ('imtihon', 'imtihon'),
        ('sinov', 'sinov'),
    )

    semestr_plan = models.ForeignKey(SemestrStudyPlan, on_delete=models.CASCADE, verbose_name='Semestr rejasi')

    science = models.ForeignKey(Science, on_delete=models.CASCADE, verbose_name='Fan')
    science_code = models.CharField(max_length=30, verbose_name='Fan kodi')
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE, verbose_name='Sinov turi')
    credit = models.IntegerField(verbose_name='Kredit miqdori')

    lecture = models.IntegerField(default=0, verbose_name='Ma\'ruza vaqti')
    practice = models.IntegerField(default=0, verbose_name='Amaliyot vaqti')
    seminar = models.IntegerField(default=0, verbose_name='Seminar vaqti')
    laboratory = models.IntegerField(default=0, verbose_name='Labaratoriya vaqti')
    independent_work = models.IntegerField(verbose_name='Mustaqil ish vaqti')

    course_work = models.BooleanField(default=False, verbose_name='Kurs ishi')

    def __str__(self) -> str:
        return '%s %s (%s)'%(self.science.name, self.semestr_plan.direction.name, self.semestr_plan.semester_number)
    
    class Meta:
        verbose_name = 'O\'quv reja fani'
        verbose_name_plural = '4. O\'quv reja fanlari'


class ProfessionalPractice(models.Model):
    ''' Malakaviy amaliyot modeli '''
    semestr_plan = models.ForeignKey(SemestrStudyPlan, on_delete=models.CASCADE, verbose_name='Semestr rejasini tanlang')
    time = models.IntegerField(verbose_name='Malakaviy amaliyot vaqti')

    def __str__(self) -> str:
        return '%s %s'%(str(self.semestr_plan), str(self.time))
    class Meta:
        verbose_name = 'Malakaviy amaliyot'
        verbose_name_plural = '5. Malakaviy amaliyotlar'



class SmallGroup(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return '%s %s'%(self.name, self.direction.name)
    
    class Meta:
        verbose_name = 'Guruh'
        verbose_name_plural = '6. Guruhlar'
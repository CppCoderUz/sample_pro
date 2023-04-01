# Generated by Django 4.1.7 on 2023-03-27 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('faculty', '0002_faculty'),
        ('cafedra', '0003_alter_cafedra_manager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name="Yo'nalish nomi")),
                ('language', models.CharField(choices=[('uzbek', "O'zbek"), ('rus', 'Rus'), ('other', 'Boshqa')], max_length=10, verbose_name="Ta'lim tili")),
                ('study_form', models.CharField(choices=[('kunduzgi', 'kunduzgi'), ('kechki', 'kechki'), ('sirtqi', 'sirtqi')], max_length=10, verbose_name="Ta'lim shakli")),
                ('code', models.CharField(blank=True, max_length=30, null=True, verbose_name="Yo'nalish kodi")),
                ('year', models.IntegerField(verbose_name='Qabul qilingan yili')),
                ('semester_number', models.IntegerField(default=8, verbose_name='Semestr soni')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.faculty', verbose_name='Fakulteti')),
            ],
            options={
                'verbose_name': "Yo'nalish",
                'verbose_name_plural': "2. Barcha yo'nalishlar",
            },
        ),
        migrations.CreateModel(
            name='Science',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Fan nomi')),
                ('cafedra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafedra.cafedra', verbose_name='Kafedrasi')),
            ],
            options={
                'verbose_name': 'Fan',
                'verbose_name_plural': '1. Fanlar',
            },
        ),
        migrations.CreateModel(
            name='SemestrStudyPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_number', models.IntegerField(verbose_name='Semestr raqami')),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_plan.direction', verbose_name="Yo'nalish")),
            ],
            options={
                'verbose_name': 'Semestr rejasi',
                'verbose_name_plural': '3. Semestr rejalari',
            },
        ),
        migrations.CreateModel(
            name='ScienceStudyPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('science_code', models.CharField(max_length=30, verbose_name='Fan kodi')),
                ('exam_type', models.CharField(choices=[('imtihon', 'imtihon'), ('sinov', 'sinov')], max_length=10, verbose_name='Sinov turi')),
                ('credit', models.IntegerField(verbose_name='Kredit miqdori')),
                ('lecture', models.IntegerField(default=0, verbose_name="Ma'ruza vaqti")),
                ('practice', models.IntegerField(default=0, verbose_name='Amaliyot vaqti')),
                ('seminar', models.IntegerField(default=0, verbose_name='Seminar vaqti')),
                ('laboratory', models.IntegerField(default=0, verbose_name='Labaratoriya vaqti')),
                ('independent_work', models.IntegerField(verbose_name='Mustaqil ish vaqti')),
                ('course_work', models.BooleanField(default=False, verbose_name='Kurs ishi')),
                ('science', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_plan.science', verbose_name='Fan')),
                ('semestr_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_plan.semestrstudyplan', verbose_name='Semestr rejasi')),
            ],
            options={
                'verbose_name': "O'quv reja fani",
                'verbose_name_plural': "4. O'quv reja fanlari",
            },
        ),
        migrations.CreateModel(
            name='ProfessionalPractice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(verbose_name='Malakaviy amaliyot vaqti')),
                ('semestr_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_plan.semestrstudyplan', verbose_name='Semestr rejasini tanlang')),
            ],
            options={
                'verbose_name': 'Malakaviy amaliyot',
                'verbose_name_plural': '5. Malakaviy amaliyotlar',
            },
        ),
    ]

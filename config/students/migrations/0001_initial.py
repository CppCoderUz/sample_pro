# Generated by Django 4.1.7 on 2023-03-28 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('study_plan', '0002_smallgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_plan.smallgroup')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': '1. Studentlar',
            },
        ),
    ]

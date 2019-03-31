# Generated by Django 2.1.5 on 2019-03-31 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auditory',
            fields=[
                ('name', models.CharField(help_text='auditory name', max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='auditory name')),
            ],
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('name', models.CharField(help_text='building name', max_length=150, primary_key=True, serialize=False, unique=True, verbose_name='building name')),
                ('address', models.CharField(blank=True, help_text='building address', max_length=5000, verbose_name='building address')),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Faculty name', max_length=150, unique=True, verbose_name='Faculty name')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Group name', max_length=150, unique=True, verbose_name='name')),
                ('is_primary', models.BooleanField(default=False, help_text='Indicates is the group primary', verbose_name='is_primary')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='lesson name', max_length=150, verbose_name='lesson name')),
                ('type', models.CharField(choices=[('class', 'class'), ('lecture', 'lecture')], default='class', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='LessonGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v0.Group')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v0.Lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(blank=True, help_text='Account first name', max_length=40, verbose_name='first_name')),
                ('middle_name', models.CharField(blank=True, help_text='Account middle name', max_length=40, verbose_name='middle_name')),
                ('last_name', models.CharField(blank=True, help_text='Account last name', max_length=40, verbose_name='middle_name')),
                ('is_verified', models.BooleanField(default=False, help_text='Indicates account has been verified for identity', verbose_name='is_verified')),
                ('is_admin', models.BooleanField(default=False, help_text='Indicates account has been admin for identity', verbose_name='is_admin')),
                ('kind', models.CharField(choices=[('teacher', 'Teacher'), ('student', 'Student'), ('client', 'Client')], default='student', help_text='Indicates account type student or teacher', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Stream name', max_length=150, unique=True, verbose_name='Stream name')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v0.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v0.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TimetableItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('repeat', models.CharField(choices=[('once', 'Once'), ('every_second_week', 'Every_second_week'), ('every_week', 'Every_week'), ('every_workday_day5', 'Every_workday_day5'), ('every_workday_day6', 'Every_workday_day6'), ('every_day', 'Every_day'), ('custom', 'Custom')], default='once', help_text='Repeat type for lesson', max_length=7)),
                ('auditory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v0.Auditory')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v0.Lesson')),
                ('timetable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v0.Timetable')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('name', models.CharField(help_text='university name', max_length=150, unique=True, verbose_name='university name')),
                ('english_name', models.CharField(help_text='university english name', max_length=150, primary_key=True, serialize=False, unique=True, verbose_name='university english name')),
                ('description', models.CharField(blank=True, help_text='university description', max_length=5000, verbose_name='university description')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api_v0.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api_v0.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api_v0.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='timetable',
            name='university',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api_v0.University'),
        ),
        migrations.AddField(
            model_name='group',
            name='stream',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api_v0.Stream'),
        ),
        migrations.AddField(
            model_name='building',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v0.University'),
        ),
        migrations.AddField(
            model_name='auditory',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v0.Building'),
        ),
        migrations.AddField(
            model_name='studentgroup',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v0.Student'),
        ),
        migrations.AlterUniqueTogether(
            name='lessongroup',
            unique_together={('group', 'lesson')},
        ),
        migrations.AddField(
            model_name='lesson',
            name='primary_teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_teacher', to='api_v0.Teacher'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='secondary_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secondary_teacher', to='api_v0.Teacher'),
        ),
        migrations.AlterUniqueTogether(
            name='studentgroup',
            unique_together={('group', 'student')},
        ),
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together={('name', 'type', 'primary_teacher')},
        ),
    ]

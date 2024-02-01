# Generated by Django 4.2.4 on 2023-12-01 22:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.vlaidations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exam', '0002_alter_choicemodel_choice_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choicemodel',
            options={'verbose_name': 'گزینه', 'verbose_name_plural': 'گزینه ها'},
        ),
        migrations.AlterModelOptions(
            name='exammodel',
            options={'verbose_name': 'فصل', 'verbose_name_plural': 'فصل ها'},
        ),
        migrations.AlterModelOptions(
            name='karnamemodel',
            options={'verbose_name': 'کارنامه', 'verbose_name_plural': 'کارنامه ها'},
        ),
        migrations.AlterModelOptions(
            name='myexamclass',
            options={'verbose_name': 'کلاس', 'verbose_name_plural': 'کلاس ها'},
        ),
        migrations.AlterModelOptions(
            name='questionmodel',
            options={'verbose_name': 'سوال', 'verbose_name_plural': 'سوالات'},
        ),
        migrations.AlterField(
            model_name='choicemodel',
            name='choice_text',
            field=models.TextField(verbose_name='متن انتخاب'),
        ),
        migrations.AlterField(
            model_name='choicemodel',
            name='is_correct',
            field=models.BooleanField(default=False, verbose_name='صحیح بون'),
        ),
        migrations.AlterField(
            model_name='choicemodel',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='exam.questionmodel', verbose_name='سوال'),
        ),
        migrations.AlterField(
            model_name='exammodel',
            name='cover_image',
            field=models.ImageField(upload_to='media/exam_image_cover/', validators=[utils.vlaidations.validate_image_size], verbose_name='عکس کاور'),
        ),
        migrations.AlterField(
            model_name='exammodel',
            name='data_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد'),
        ),
        migrations.AlterField(
            model_name='exammodel',
            name='myclass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='exam.myexamclass', verbose_name='کلاس'),
        ),
        migrations.AlterField(
            model_name='exammodel',
            name='title',
            field=models.TextField(verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='karnamedbmodel',
            name='choice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='choice_id', to='exam.choicemodel', verbose_name='انتخاب'),
        ),
        migrations.AlterField(
            model_name='karnamedbmodel',
            name='karname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='karname', to='exam.karnamemodel', verbose_name='کارنامه'),
        ),
        migrations.AlterField(
            model_name='karnamedbmodel',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='question_id', to='exam.questionmodel', verbose_name='سوال'),
        ),
        migrations.AlterField(
            model_name='karnamemodel',
            name='exam_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='exam_id', to='exam.exammodel', verbose_name='امتحان'),
        ),
        migrations.AlterField(
            model_name='karnamemodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='myexamclass',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده'),
        ),
        migrations.AlterField(
            model_name='myexamclass',
            name='cover_image',
            field=models.ImageField(null=True, upload_to='media/classes_image_cover/', validators=[utils.vlaidations.validate_image_size], verbose_name='عکس کاور'),
        ),
        migrations.AlterField(
            model_name='myexamclass',
            name='study_field',
            field=models.CharField(max_length=100, verbose_name='فیلد مطالعه'),
        ),
        migrations.AlterField(
            model_name='myexamclass',
            name='title',
            field=models.TextField(verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='questionmodel',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='exam.exammodel', verbose_name='امتحان'),
        ),
        migrations.AlterField(
            model_name='questionmodel',
            name='question_text',
            field=models.TextField(verbose_name='متن سوال'),
        ),
    ]
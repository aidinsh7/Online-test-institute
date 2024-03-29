# Generated by Django 4.2.4 on 2023-12-02 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('markethub', '0005_alter_markethubmodel_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='markethubkarnamemodel',
            options={'verbose_name': 'کارنامه', 'verbose_name_plural': 'کارنامه ها'},
        ),
        migrations.AlterModelOptions(
            name='markethubmodel',
            options={'verbose_name': 'فصل', 'verbose_name_plural': 'فصل ها'},
        ),
        migrations.AlterModelOptions(
            name='markethubquestionmodel',
            options={'verbose_name': 'سوال', 'verbose_name_plural': 'سوالات'},
        ),
        migrations.AlterModelOptions(
            name='myclass',
            options={'verbose_name': 'کلاس', 'verbose_name_plural': 'کلاس ها'},
        ),
        migrations.AlterField(
            model_name='markethubanswer',
            name='is_correct',
            field=models.BooleanField(default=False, verbose_name='صحیح بودن'),
        ),
        migrations.AlterField(
            model_name='markethubanswer',
            name='karname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='litner_azmon', to='markethub.markethubkarnamemodel', verbose_name='کارنامه'),
        ),
        migrations.AlterField(
            model_name='markethubanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='markethub.markethubquestionmodel', verbose_name='سوال'),
        ),
        migrations.AlterField(
            model_name='markethubkarnamemodel',
            name='exam_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='exam_id', to='markethub.markethubmodel', verbose_name='فصل'),
        ),
        migrations.AlterField(
            model_name='markethubkarnamemodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='markethubmodel',
            name='cover_image',
            field=models.ImageField(null=True, upload_to='media/markethub_image_cover/', verbose_name='عکس کاور'),
        ),
        migrations.AlterField(
            model_name='markethubmodel',
            name='data_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد'),
        ),
        migrations.AlterField(
            model_name='markethubmodel',
            name='description',
            field=models.CharField(max_length=100, verbose_name='توضیحات فصل برای خرید'),
        ),
        migrations.AlterField(
            model_name='markethubmodel',
            name='myclass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='markethubs', to='markethub.myclass', verbose_name='کلاس مربوطه'),
        ),
        migrations.AlterField(
            model_name='markethubmodel',
            name='paid_users',
            field=models.ManyToManyField(blank=True, related_name='paid_market_hubs', to=settings.AUTH_USER_MODEL, verbose_name='دسترسی کاربران'),
        ),
        migrations.AlterField(
            model_name='markethubmodel',
            name='price',
            field=models.SmallIntegerField(verbose_name='قیمیت فصل'),
        ),
        migrations.AlterField(
            model_name='markethubmodel',
            name='title',
            field=models.CharField(max_length=100, verbose_name='عنوان فصل'),
        ),
        migrations.AlterField(
            model_name='markethubquestionmodel',
            name='answers_text',
            field=models.CharField(max_length=100, verbose_name='جواب را وارد کنید'),
        ),
        migrations.AlterField(
            model_name='markethubquestionmodel',
            name='markethub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='markethub.markethubmodel', verbose_name='فصل'),
        ),
        migrations.AlterField(
            model_name='markethubquestionmodel',
            name='question_text',
            field=models.CharField(max_length=150, verbose_name='سوال را وارد کنید'),
        ),
        migrations.AlterField(
            model_name='myclass',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده'),
        ),
        migrations.AlterField(
            model_name='myclass',
            name='cover_image',
            field=models.ImageField(null=True, upload_to='media/classes_image_cover/', verbose_name='کاور کلاس'),
        ),
        migrations.AlterField(
            model_name='myclass',
            name='study_field',
            field=models.CharField(max_length=100, verbose_name='رشته تحصیلی'),
        ),
        migrations.AlterField(
            model_name='myclass',
            name='title',
            field=models.CharField(max_length=100, verbose_name='عنوان کلاس'),
        ),
    ]

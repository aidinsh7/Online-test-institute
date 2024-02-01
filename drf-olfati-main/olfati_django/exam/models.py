from django.db import models
from accounts.models import UserModel

from utils.vlaidations import validate_image_size


class MyExamClass(models.Model):
    class Meta:
        verbose_name = 'کلاس'
        verbose_name_plural = 'کلاس ها'

    title = models.TextField(verbose_name='عنوان')
    study_field = models.CharField(max_length=100, verbose_name='فیلد مطالعه')
    cover_image = models.ImageField(upload_to='media/classes_image_cover/', null=True, validators=[validate_image_size], verbose_name='عکس کاور')
    author= models.ForeignKey(UserModel, on_delete=models.PROTECT, verbose_name='نویسنده')

    def __str__(self):
        return self.title



class ExamModel(models.Model):
    class Meta:
        verbose_name = 'فصل'
        verbose_name_plural = 'فصل ها'


    title = models.TextField(verbose_name='عنوان')
    cover_image = models.ImageField(upload_to='media/exam_image_cover/', validators=[validate_image_size], verbose_name='عکس کاور')
    data_created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    myclass = models.ForeignKey(MyExamClass, related_name='exams', on_delete=models.CASCADE, verbose_name='کلاس')

    def __str__(self):
        return self.title[:20]

    def have_karname(self, user):
        return KarNameModel.objects.filter(user=user).exists()


class QuestionModel(models.Model):
    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'

    exam = models.ForeignKey(ExamModel, on_delete=models.CASCADE, related_name='questions', verbose_name='امتحان')
    question_text = models.TextField(verbose_name='متن سوال')

    def __str__(self):
        return f"{self.question_text[:25]}"


class ChoiceModel(models.Model):
    class Meta:
        verbose_name = 'گزینه'
        verbose_name_plural = 'گزینه ها'

    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name='choices', verbose_name='سوال')
    choice_text = models.TextField(verbose_name='متن انتخاب')
    is_correct = models.BooleanField(default=False, verbose_name='صحیح بون')

    def __str__(self):
        return f"{self.question.question_text[:25]} | {self.choice_text[:20]}"


class KarNameModel(models.Model):
    class Meta:
        verbose_name = 'کارنامه'
        verbose_name_plural = 'کارنامه ها'

    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, verbose_name='کاربر')
    exam_id = models.ForeignKey(ExamModel, on_delete=models.PROTECT, related_name="exam_id", verbose_name='امتحان')


class KarNameDBModel(models.Model):
    question = models.ForeignKey(QuestionModel, on_delete=models.PROTECT, related_name="question_id", verbose_name='سوال')
    choice = models.ForeignKey(ChoiceModel, on_delete=models.PROTECT, related_name="choice_id", null=True, verbose_name='انتخاب')
    karname = models.ForeignKey(KarNameModel, on_delete=models.PROTECT, related_name="karname", verbose_name='کارنامه')

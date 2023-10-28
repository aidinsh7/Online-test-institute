from django.db import models
from accounts.models import UserModel


class ExamModel(models.Model):
    title = models.CharField(max_length=100)
    study_field = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='media/exam_image_cover/')
    author = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    data_created = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(auto_created=False,null=True,default=False)

    def __str__(self):
        return self.title[:20]


class QuestionModel(models.Model):
    exam = models.ForeignKey(ExamModel, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.question_text[:25]}"


class ChoiceModel(models.Model):
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False
                                     )

    def __str__(self):
        return f"{self.question.question_text[:25]} | {self.choice_text[:20]}"


class KarNameModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, )
    exam_id = models.ForeignKey(ExamModel, on_delete=models.PROTECT, related_name="exam_id")


class KarNameDBModel(models.Model):
    question = models.ForeignKey(QuestionModel, on_delete=models.PROTECT, related_name="question_id")
    choice = models.ForeignKey(ChoiceModel, on_delete=models.PROTECT, related_name="choice_id", null=True)
    karname = models.ForeignKey(KarNameModel, on_delete=models.PROTECT, related_name="karname")

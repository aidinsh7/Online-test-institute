from django.db import models
from accounts.models import UserModel


class LitnerModel(models.Model):
    title = models.CharField(max_length=100)
    study_field = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='media/litner_image_cover/', null=True)
    author = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    data_created = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(null=True,default=False)



class LitnerQuestionModel(models.Model):
    litner = models.ForeignKey(LitnerModel, on_delete=models.CASCADE, related_name='litner')
    question_text = models.CharField(max_length=150)
    answers_text = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.question_text} | {self.answers_text}"


class LitnerKarNameModel(models.Model):
    exam_id = models.OneToOneField(LitnerModel, on_delete=models.CASCADE, related_name='exam_id')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, )


class LitnerAnswer(models.Model):
    karname = models.ForeignKey(LitnerKarNameModel, on_delete=models.PROTECT, related_name="litner_azmon")
    question = models.ForeignKey(LitnerQuestionModel, on_delete=models.PROTECT, )
    is_correct = models.BooleanField(default=False)


class LitnerKarNameDBModel(models.Model):
    question = models.ForeignKey(LitnerQuestionModel, on_delete=models.PROTECT, related_name='question_id')
    is_correct = models.BooleanField(null=True)
    karname = models.ForeignKey(LitnerKarNameModel, on_delete=models.PROTECT, related_name="karname")

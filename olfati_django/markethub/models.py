from django.db import models
from accounts.models import UserModel




    

class MarketHubModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='media/litner_image_cover/', null=True)
    author= models.ForeignKey(UserModel, on_delete=models.PROTECT)
    price = models.SmallIntegerField()
    data_created = models.DateTimeField(auto_now_add=True)
    paid_users = models.ManyToManyField(UserModel, related_name='paid_market_hubs', blank=True)
    study_field = models.CharField(max_length=100,default="")
    is_open = models.BooleanField(null=True,default=False)
    has_access=models.BooleanField




    def is_paid_user(self, user):
        return self.paid_users.filter(id=user.id).exists()
    
    def hass_acess(self,user):
        return self.has_access.filter(id=user.id).exists()


class MarketHubQuestionModel(models.Model):
    markethub = models.ForeignKey(MarketHubModel, on_delete=models.CASCADE, related_name='markethub')
    question_text = models.CharField(max_length=150)
    answers_text = models.CharField(max_length=100)


class MarketHubKarNameModel(models.Model):
    exam_id = models.OneToOneField(MarketHubModel, on_delete=models.CASCADE, related_name='exam_id')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, )
    is_open = models.BooleanField(default=True)
    

class MarketHubAnswer(models.Model):
    karname = models.ForeignKey(MarketHubKarNameModel, on_delete=models.PROTECT, related_name="litner_azmon")
    question = models.ForeignKey(MarketHubQuestionModel, on_delete=models.PROTECT, )
    is_correct = models.BooleanField(default=False)


class MarketHubKarNameDBModel(models.Model):
    question = models.ForeignKey(MarketHubQuestionModel, on_delete=models.PROTECT, related_name='question_id')
    is_correct = models.BooleanField(null=True)
    karname = models.ForeignKey(MarketHubKarNameModel, on_delete=models.PROTECT, related_name="karname")








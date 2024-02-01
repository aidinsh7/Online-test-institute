from django.db import models
from accounts.models import UserModel



class Myclass(models.Model):
    class Meta:
        verbose_name = 'کلاس'
        verbose_name_plural = 'کلاس ها'

    title = models.CharField(max_length=100,verbose_name="عنوان کلاس")
    study_field = models.CharField(max_length=100, verbose_name="رشته تحصیلی")
    cover_image = models.ImageField(upload_to='media/classes_image_cover/', null=True,verbose_name="کاور کلاس")
    author= models.ForeignKey(UserModel, on_delete=models.PROTECT, verbose_name="نویسنده")
    

class MarketHubModel(models.Model):
    class Meta:
        verbose_name = 'فصل'
        verbose_name_plural = 'فصل ها'
    
    title = models.CharField(max_length=100,verbose_name='عنوان فصل')
    description = models.CharField(max_length=100,verbose_name='توضیحات فصل برای خرید')
    cover_image = models.ImageField(upload_to='media/markethub_image_cover/', null=True,verbose_name='عکس کاور')
    price = models.SmallIntegerField(verbose_name='قیمیت فصل')
    myclass = models.ForeignKey(Myclass, related_name='markethubs', on_delete=models.CASCADE,verbose_name='کلاس مربوطه')
    data_created = models.DateTimeField(auto_now_add=True,verbose_name='زمان ایجاد')
    paid_users = models.ManyToManyField(UserModel, related_name='paid_market_hubs', blank=True,verbose_name='دسترسی کاربران')

    @property
    def author (self):
        return self.myclass.author

    def is_paid_user(self, user):
        return self.paid_users.filter(id=user.id).exists()
    
    def is_author(self, user):
        return user.id == self.myclass.author.id
    
    #امتحان داده
    def have_karname(self, user):
        return MarketHubKarNameModel.objects.filter(user=user).exists()


class MarketHubQuestionModel(models.Model):
    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'
        
    markethub = models.ForeignKey(MarketHubModel, on_delete=models.CASCADE, related_name='questions',verbose_name="فصل")
    question_text = models.CharField(max_length=150,verbose_name="سوال را وارد کنید")
    answers_text = models.CharField(max_length=100,verbose_name="جواب را وارد کنید")


class MarketHubKarNameModel(models.Model):
    class Meta:
        verbose_name = 'کارنامه'
        verbose_name_plural = 'کارنامه ها'
    exam_id = models.OneToOneField(MarketHubModel, on_delete=models.CASCADE, related_name='exam_id', verbose_name="فصل")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="کاربر")
    

class MarketHubAnswer(models.Model):
    karname = models.ForeignKey(MarketHubKarNameModel, on_delete=models.PROTECT, related_name="litner_azmon", verbose_name="کارنامه")
    question = models.ForeignKey(MarketHubQuestionModel, on_delete=models.PROTECT, verbose_name="سوال" )
    is_correct = models.BooleanField(default=False, verbose_name="صحیح بودن")


class MarketHubKarNameDBModel(models.Model):
    question = models.ForeignKey(MarketHubQuestionModel, on_delete=models.PROTECT, related_name='question_id')
    is_correct = models.BooleanField(null=True)
    karname = models.ForeignKey(MarketHubKarNameModel, on_delete=models.PROTECT, related_name="karname")








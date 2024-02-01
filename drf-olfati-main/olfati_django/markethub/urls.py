from django.urls import path
from markethub.views import (
    MarketHubListView ,ListCreateMyClassView,
    MarketHubTakingExam, ListProfileMyClassView, 
    ListProfileMyClassCreatorView,
    MakeQuestionView,
    send_request, verify
)

urlpatterns = [

    path('zarrin-pall/request/', send_request, name='request'),
    path('zarrin-pall/verify/', verify , name='verify'),
    # {
    # "title": "",
    # "description": "",
    # "cover_image": null
    # }
    # ساختن، لیست تمام کلاس ها
    path('class-list/', ListCreateMyClassView.as_view({'get': 'list', 'post': 'create'})),

    # لیست تمام کلاس هایی که کاربر داخلشان مارکت هاب خریده شده دارد
    path('profile/class-list/', ListProfileMyClassView.as_view()),

    # لیست تمام کلاس هایی که کاربر ساخته تا بفروشد
    path('profile/my-class-list/', ListProfileMyClassCreatorView.as_view()),

    # حزئیات کلاس ها شامل فصل ها و ادیت یک کلاس و حذف آن
    path('class-list/<int:pk>/', ListCreateMyClassView.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),


    #  گرفتن فصول یک کلاس اونایی ک خریدی
    path('<int:pk>/markethub/list/', MarketHubListView.as_view({'get': 'list'})),

    
    # {
    # "title": "test",
    # "study_field": "test",
    # "cover_image": null,
    # "price": 10,
    # "description": "test",
    # "myclass": 1,
    # "questions": [{"question_text":"1", "answers_text":"2"}]
    # }
    # ساختن یک فصل
    path("markethub/", MarketHubListView.as_view({'post': 'create'})),
    # {
    # "title": "test",
    # "study_field": "test",
    # "cover_image": null,
    # "price": 10,
    # "description": "test",
    # "myclass": 1,
    # "questions": [{"question_text":"1", "answers_text":"2"}]
    # }
    # ویرایش، حذف یک فصل و  گرفتن جزئیات یک فصل شامل سوالات
    path("markethub/<int:pk>/", MarketHubListView.as_view({'get':'retrieve', 'put':'partial_update', 'delete': 'destroy'})),
    
    #ساخت سوال
    # [
    #   {
    #     question_text:"",
    #     answers_text:"",
    #     markethub: "" ایدی مارکت هاب
    #   }
    # ]
    path("make-question/", MakeQuestionView.as_view({'post':'create'})),
    #  ادیت سوال
    # {
    #     "question_text":"",
    #     "answers_text":"",
    #     "markethub": "" ایدی مارکت هاب
    # }
    path("make-question/<int:pk>/", MakeQuestionView.as_view({'put':'partial_update'})),



    # فقط سوالایی که جواب دارن در هر دو حالت برای امتحان یا اصلاج
            # [
            #     {
            #         "question": 1,
            #         "is_correct": true or false
            #     }
            # ]
    # امتحان دادن و اصلاح یک فصل
    path('list/<int:pk>/', MarketHubTakingExam.as_view()),
    path('list/', MarketHubTakingExam.as_view()),
    
]

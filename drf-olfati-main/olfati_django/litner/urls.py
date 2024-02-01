from django.urls import path

from litner.views import LitnerListView, LitnerView, ListCreateMyClassView,LitnerTakingExam,ListProfileMyClassView,ListProfileMyClassCreatorView

urlpatterns = [
   
# ساختن، لیست تمام کلاس ها
    path('class-list/', ListCreateMyClassView.as_view({'get': 'list', 'post': 'create'})),
   
    # حزئیات کلاس ها شامل فصل ها و ادیت یک کلاس و حذف آن
    path('class-list/<int:pk>/', ListCreateMyClassView.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),


    #  گرفتن فصول یک کلاس اونایی ک خریدی
    path('<int:pk>/litner/list/', LitnerListView.as_view({'get': 'list'})),
    
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
    path("litner/", LitnerListView.as_view({'post': 'create'})),
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
    path("litner/<int:pk>/", LitnerListView.as_view({'get':'retrieve', 'put':'partial_update', 'delete': 'destroy'})),
    
    # فقط سوالایی که جواب دارن در هر دو حالت برای امتحان یا اصلاج
            # [
            #     {
            #         "question": 1,
            #         "is_correct": true or false
            #     }
            # ]
    # امتحان دادن و اصلاح یک فصل
    path('list/<int:pk>/', LitnerTakingExam.as_view()),
    path('list/',LitnerTakingExam.as_view()),
    
]


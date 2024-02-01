from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import *
from django.shortcuts import redirect
from .permissions import  IsAuthenticated
from .serializer import  (
    MarketHubSerializer, 
    MarketHubTakeExamSerializer, 
    MarketHubDetailSerializer, MyClassSerializer,
    MarketHubQuestionSerializer
)
from django.conf import settings
import requests
import json
#part1 source ___________________________________________________________________________________________________________________

permission_error = Response({'اجازه این کار را ندارید.'}, status.HTTP_403_FORBIDDEN)


# ساخت کلاس 
# ورودی ها : 
# title 
# description
# cover image 
# price
class ListCreateMyClassView(ModelViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = MyClassSerializer
    queryset = Myclass.objects.all()

    def get_serializer_class(self):
        return MyClassSerializer
            
    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data":serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_author(request.user):
            return permission_error
        return super().destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_author(request.user):
            return permission_error
        return super().partial_update(request, *args, **kwargs)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data.get('markethubs', None)
        return Response({"data":data})

class MarketHubListView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MarketHubModel.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return MarketHubSerializer
        else:
            return MarketHubDetailSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = MarketHubModel.objects.filter(myclass_id = self.kwargs.get('pk', None))
        return queryset   

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data":serializer.data})

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_author(request.user):
            return permission_error
        return super().partial_update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not (instance.is_author(request.user) or instance.is_paid_user(request.user)):
            return permission_error
        serializer = self.get_serializer(instance)
        data = serializer.data.get('questions')
        return Response({'data':data})

class MarketHubTakingExam(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            try:
                markethub = MarketHubModel.objects.all()
                serializer = MarketHubSerializer(markethub, many=True)
                return Response({'data': serializer.data}, status.HTTP_200_OK)
            except Exception as ins:
                return Response({'message': str(ins)},status.HTTP_404_NOT_FOUND)
        else:
            try:
                markethub = MarketHubModel.objects.get(myclass_id=pk, paid_users=self.request.user)
                serializer = MarketHubDetailSerializer(markethub, context={'request': request, 'exam': pk})
                return Response({'data': serializer.data}, status.HTTP_200_OK)
            except Exception as ins:
                return Response({'message': 'Leitner notFound'}, status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):

        exam = get_object_or_404(MarketHubModel, pk=pk)
        try:
            karname = MarketHubKarNameModel.objects.get(user=request.user, exam_id=exam)
            answers = MarketHubKarNameDBModel.objects.filter(karname=karname)
            is_corrects = []
            is_false = []
            is_null = []
            for answer in answers:
                if not answer.is_correct is None:
                    if answer.is_correct == True:
                        is_corrects.append(
                            {
                                'question_id': answer.question.id,
                                'question_text': answer.question.question_text,
                                'answer_text': answer.question.answers_text
                            })
                    else:
                        if answer.is_correct == False:
                            is_false.append({
                                'question_id': answer.question.id,
                                'question_text': answer.question.question_text,
                                'answer_text': answer.question.answers_text
                            })
                else:
                    is_null.append({
                        'question_id': answer.question.id,
                        'question_text': answer.question.question_text,
                        'answer_text': answer.question.answers_text
                    })
            result = {
                'True answers': is_corrects,
                'False answers': is_false,
                'None answers': is_null
            }
            exam.save()
            return Response(result)

        except:
            data = {'user': request.user.id, "exam_id": pk}
            if request.data:
                data['karname'] = request.data
            else:
                data['karname'] = []
            serializer = MarketHubTakeExamSerializer(data=data, context={'request': request, 'exam': pk})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        # request.data example: you should send new questions and their choices 
        # [
        #     {
        #         "question":1,    #our questuin
        #         "choice":2      #client's answer
        #     },
        #     ...
        # ]
        data = {'user': request.user.id, "exam_id": pk}
        if request.data:
            data['karname'] = request.data
        else:
            data['karname'] = []
        exam = get_object_or_404(MarketHubModel, pk=pk)
        karname = get_object_or_404(MarketHubKarNameModel, user=request.user, exam_id=exam)
        serializer = MarketHubTakeExamSerializer(instance=karname, data=data, context={'request': request, 'exam': pk},
                                              partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception:
                return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)




class ListProfileMyClassView(generics.ListAPIView):
    serializer_class = MyClassSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        valid_objects = Myclass.objects.filter(markethubs__paid_users=self.request.user)
        return valid_objects
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data":serializer.data})


class ListProfileMyClassCreatorView(generics.ListAPIView):
    serializer_class = MyClassSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        valid_objects = Myclass.objects.filter(author=self.request.user)
        return valid_objects
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data":serializer.data})


class MakeQuestionView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MarketHubQuestionSerializer
    queryset = MarketHubQuestionModel.objects.all()
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.markethub.myclass.author:
            return permission_error
        return super().partial_update(request, *args, **kwargs)

ZP_API_REQUEST = "https://api.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = "https://api.zarinpal.com/pg/StartPay/"
# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


def send_request(request):
    amount = 1000  # Rial / Required
    description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
    phone = 'YOUR_PHONE_NUMBER'  # Optional
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Description": description,
        # "Phone": phone,
        "CallbackURL": settings.CALLBACKURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    try:
        response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return redirect(ZP_API_STARTPAY + str(response['Authority']))
                                 
            else:
                return JsonResponse({'status': False, 'code': str(response['Status'])})
        return JsonResponse(response)
    
    except requests.exceptions.Timeout:
        return JsonResponse({'status': False, 'code': 'timeout'})
    except requests.exceptions.ConnectionError:
        return JsonResponse({'status': False, 'code': 'connection error'})


def verify(authority):
    amount = 1000
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response
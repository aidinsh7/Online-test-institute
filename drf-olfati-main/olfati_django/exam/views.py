from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import ExamModel, KarNameModel, KarNameDBModel, MyExamClass
from .serializer import ExamDetailsSerializer, ExamSerializer, KarNameSerializer, TakeExamSerializer, MyExamClassSerializer

class ListCreateMyClassView(ModelViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = MyExamClassSerializer
    queryset = MyExamClass.objects.all()

    def get_serializer_class(self):
        return MyExamClassSerializer
            
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
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data.get('exams', None)
        return Response({"data":data})



class ExamListView(APIView):
    permission_classes = [IsAuthenticated]
    e404 = status.HTTP_400_BAD_REQUEST

    def get(self, request, pk=None):
        if pk is None:
            try:
                exams = ExamModel.objects.all()
                serializer = ExamSerializer(exams, many=True, context = {'request': request})
                return Response({'data': serializer.data}, status.HTTP_200_OK)
            except Exception as ins:
                return Response({'message': str(ins)}, status.HTTP_404_NOT_FOUND)
        else:
            try:
                exams = ExamModel.objects.get(pk=pk)
                serializer = ExamDetailsSerializer(exams, context = {'request': request})  
                data = serializer.data.get("questions")   
                return Response({'data': data}, status.HTTP_200_OK)
            except Exception as ins:
                return Response({'message': 'exam notFound'}, status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        exam = get_object_or_404(ExamModel, pk=pk)
        try:
            karname = KarNameModel.objects.get(user=request.user, exam_id=exam)
            answers = KarNameDBModel.objects.filter(karname=karname)
            is_corrects = []
            is_false = []
            is_null = []
            for answer in answers:
                if answer.choice:
                    if answer.choice.is_correct == True:
                        is_corrects.append({
                            'question_id': answer.question.id,
                            'question_text': answer.question.question_text,
                            'answer_text': answer.choice.choice_text
                        })
                    else:
                        is_false.append({
                            'question_id': answer.question.id,
                            'question_text': answer.question.question_text,
                            'answer_text': answer.choice.choice_text
                        })
                else:
                    is_null.append({
                        'question_id': answer.question.id,
                        'question_text': answer.question.question_text,
                        'answer_text': None
                    })
            result = {
                'True answers': is_corrects,
                'False answers': is_false,
                'None answers': is_null
            }
            exam.save()
            return Response(result)

        except:
            # request.data example: you should send question that are answered
            # [
            #     {
            #         "question":1, #our questuin
            #         "choice":2   #client's answer
            #     },
            #     ...
            # ]
            data = {'user': request.user.id, "exam_id": pk}
            if request.data:
                data['karname'] = request.data
            else:
                data['karname'] = []
            serializer = TakeExamSerializer(
                data=data, context={'request': request, 'exam': pk})
            try:
                serializer.is_valid()
            except Exception:
                return Response(serializer.errors, status=self.e404)
            serializer.save()
            return Response(serializer.data)

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
        exam = get_object_or_404(ExamModel, pk=pk)
        karname = get_object_or_404(
            KarNameModel, user=request.user, exam_id=exam)
        serializer = TakeExamSerializer(instance=karname, data=data, context={
            'request': request, 'exam': pk}, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception:
                return Response(serializer.errors, self.e404)
        else:
            return Response(serializer.errors, self.e404)
        return Response(serializer.data)


class ExamView(APIView):
    permission_classes = [IsAdminUser]
    e404 = status.HTTP_400_BAD_REQUEST

    def post(self, request):
        try:
            serializer = ExamDetailsSerializer(data=request.data, context = {'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {'data': serializer.data}, status.HTTP_201_CREATED)
            return Response({'data': serializer.errors}, self.e404)
        except Exception as e:
            return Response({'data': 'data Is no valid'}, self.e404)

    def put(self, request, pk):
        query = ExamModel.objects.get(pk=pk)
        serializer = ExamDetailsSerializer(
            instance=query, data=request.data, partial=True, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data}, status.HTTP_200_OK)
        return Response({'message': serializer.errors}, self.e404)

    def delete(self, request, pk):
        try:
            query = ExamModel.objects.get(pk=pk)
            query.delete()
            return Response({'message': 'exam remove successfully'}, status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'exam nof found for remove'}, status.HTTP_404_NOT_FOUND)


class ExamKarNameView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = KarNameModel.objects.all()
        srz_data = KarNameSerializer(query, many=True, context = {'request': request}).data
        return Response(srz_data, status.HTTP_200_OK)

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from litner.models import LitnerModel, LitnerKarNameModel, LitnerKarNameDBModel
from litner.serializer import LitnerSerializer, LitnerDetailSerializer, LitnerTakeExamSerializer


class LitnerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            try:
                leitners = LitnerModel.objects.all()
                serializer = LitnerSerializer(leitners, many=True)
                return Response({'data': serializer.data}, status.HTTP_200_OK)
            except Exception as ins:
                return Response({'message': str(ins)},status.HTTP_404_NOT_FOUND)
        else:
            try:
                leitners = LitnerModel.objects.get(pk=pk)
                serializer = LitnerDetailSerializer(leitners)
                serializer = LitnerDetailSerializer(leitners)
                return Response({'data': serializer.data}, status.HTTP_200_OK)
            except Exception as ins:
                return Response({'message': 'Leitner notFound'}, status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):

        exam = get_object_or_404(LitnerModel, pk=pk)
        try:
            exam.is_open = True
            karname = LitnerKarNameModel.objects.get(user=request.user, exam_id=exam)
            answers = LitnerKarNameDBModel.objects.filter(karname=karname)
            is_corrects = []
            is_false = []
            is_null = []
            print(answers)
            for answer in answers:
                if not answer.is_correct is None:
                    if answer.is_correct == True:
                        is_corrects.append(
                            {
                                'question_id': answer.question.id,
                                # 'question_text': answer.question.question_text,
                                # 'answer_text': answer.answerss
                            })
                    else:
                        if answer.is_correct == False:
                            is_false.append({
                                'question_id': answer.question.id,
                                # 'question_text': answer.question.question_text,
                                # 'answer_text': answer.answerss
                            })
                else:
                    is_null.append({
                        'question_id': answer.question.id,
                        # 'question_text': answer.question.question_text,
                        # 'answer_text': answer.answerss
                    })
            result = {
                'True answers': is_corrects,
                'False answers': is_false,
                'None answers': is_null
            }
            exam.save()
            return Response(result)

        except:
            # just questions that have answer
            # [
            #     {
            #         "question": 1,
            #         "is_correct": true or false
            #     }
            # ]
            data = {'user': request.user.id, "exam_id": pk}
            if request.data:
                data['karname'] = request.data
            else:
                data['karname'] = []
            serializer = LitnerTakeExamSerializer(data=data, context={'request': request, 'exam': pk})
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
        exam = get_object_or_404(LitnerModel, pk=pk)
        karname = get_object_or_404(LitnerKarNameModel, user=request.user, exam_id=exam)
        serializer = LitnerTakeExamSerializer(instance=karname, data=data, context={'request': request, 'exam': pk},
                                              partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception:
                return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)


class LitnerView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = LitnerDetailSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response(data.data)

    def delete(self, request, pk):
        try:
            instance = LitnerModel.objects.get(pk=pk)
            instance.delete()
            return Response({"massage": "leitner remove successfully"}, status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(
                {"massage": "leitner not found"}, status.HTTP_404_NOT_FOUND)

    def put(self, request):
        pass

# a = {
#     'exam': 1,
#     'user': 20,
#     'answer': [
#         {
#             "id_question": 5,
#             "choice": None  # null
#         }
#     ],
#     # 'true_answer': [
#     #     {
#     #         "question_text": "سوال اول آزمون ریاضی که بود؟",
#     #         "answers_text": "رضا"
#     #     },
#     #     {
#     #         "question_text": "سوال 2 آزمون مامایی که بود؟",
#     #         "answers_text": "احمد"
#     #     },
#     #     {
#     #         "question_text": "سوال اول آزمون عربی که بود؟",
#     #         "answers_text": "علی"
#     #     },
#     # ],
#     # 'no_answer': [
#     #     {
#     #         "question_text": "امیر نمره ریاضیش چند بود؟",
#     #         "answers_text": "10"
#     #     },
#     #     {
#     #         "question_text": "سوال 2 آزمون مامایی که بود؟",
#     #         "answers_text": "احمد"
#     #     },
#     #     {
#     #         "question_text": "سوال اول آزمون عربی که بود؟",
#     #         "answers_text": "علی"
#     #     },
#     # ],
#     # 'false_answer': [
#     #     {
#     #         "question_text": "سوال اول آزمون ریاضی که بود؟",
#     #         "answers_text": "رضا"
#     #     },
#     #     {
#     #         "question_text": "سوال 2 آزمون مامایی که بود؟",
#     #         "answers_text": "احمد"
#     #     },
#     #     {
#     #         "question_text": "سوال اول آزمون عربی که بود؟",
#     #         "answers_text": "علی"
#     #     },
#     # ],
# }

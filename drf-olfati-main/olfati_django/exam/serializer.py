from rest_framework import serializers

from .models import ExamModel, ChoiceModel, QuestionModel, KarNameModel, KarNameDBModel, MyExamClass
from accounts.serializer import UserSerializers
from django.shortcuts import get_object_or_404

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceModel
        fields = ('id','choice_text','is_correct')
                              
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionModel
        fields = ('question_text',)



class ExamQuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = QuestionModel
        fields = ('id', 'question_text', 'choices')


class ExamDetailsSerializer(serializers.ModelSerializer):
    questions = ExamQuestionSerializer(many=True)
    have_karname = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ExamModel
        fields = ('id', 'title', 'questions', 'data_created', 'have_karname')
   
    def get_have_karname(self, obj):
        request = self.context.get("request")
        return obj.have_karname(request.user)
    
    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        exam = ExamModel.objects.create(**validated_data)

        for question_data in questions_data:
            choices_data = question_data.pop('choices', [])
            question = QuestionModel.objects.create(exam=exam, **question_data)
            for choice_data in choices_data:
                choice = ChoiceModel.objects.create(question=question, **choice_data)

        return exam

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', [])
        # Update Exam fields
        instance.title = validated_data.get('title', instance.title)
        instance.study_field = validated_data.get('study_field', instance.study_field)
        instance.save()
        return instance


class ExamSerializer(serializers.ModelSerializer):
    have_karname = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ExamModel
        fields = "__all__"

    def get_have_karname(self, obj):
        request = self.context.get("request")
        return obj.have_karname(request.user)
    

class MyExamClassSerializer(serializers.ModelSerializer):
    exams = ExamSerializer(many=True, read_only=True)
    class Meta: 
        model = MyExamClass
        fields = '__all__'
        read_only_fields = ['author']

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if not request.parser_context.get("kwargs").get("pk"):
            rep.pop("exams", None)
        return rep

class KarNameDBMSerializer(serializers.ModelSerializer):
    # choice = ChoiceSerializer(many=True)
    # question = QuestionSerializer(many=True)
    class Meta:
        model = KarNameDBModel 
        fields = ('question', 'choice',)


#*******************************
class KarNameSerializer(serializers.ModelSerializer):
    user = UserSerializers()
    exam_id = ExamDetailsSerializer()
    class Meta:
        model = KarNameModel
        fields = '__all__'



class TakeExamSerializer(serializers.ModelSerializer):
    karname = KarNameDBMSerializer(KarNameDBModel.objects.all() ,many = True)
    class Meta:
        model = KarNameModel
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user 
        exam = ExamModel.objects.get(pk= self.context.get('exam'))
        questions = []
        karname = KarNameModel.objects.create(user= user, exam_id= exam)
        for question_and_choice in validated_data['karname']:
            question = question_and_choice['question']
            if question.exam != karname.exam_id:
                continue
            questions.append(question.id)
            choice = question_and_choice['choice']
            if choice.question != question:
                choice = None
            KarNameDBModel.objects.create(karname=karname, question=question, choice=choice)
        question_with_no_answer = exam.questions.exclude(id__in=questions)
        for question in question_with_no_answer:
            KarNameDBModel.objects.create(karname=karname, question=question, choice=None)
        return karname
    
    def update(self, instance, validated_data):
        karname = instance
        for question_and_choice in validated_data['karname']:
            question = question_and_choice['question']
            if question.exam != karname.exam_id:
                continue
            choice = question_and_choice['choice']
            if choice.question != question:
                choice = None
            answered = KarNameDBModel.objects.get(question=question, karname=karname)
            answered.choice = choice
            answered.save() 
        return karname    

       





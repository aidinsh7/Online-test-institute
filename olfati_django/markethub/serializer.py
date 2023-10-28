from .models import *
from rest_framework import serializers
from accounts.serializer import UserSerializers


# اگه پرداخت نکرده بود
class MarketHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketHubModel
        fields = ('title', 'description','study_field', 'cover_image', 'price', 'data_created','is_open')


class MarketHubQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketHubQuestionModel
        fields = "__all__"


# اگه پرداخت کرده بود


class MarketHubPaidSerializer(serializers.ModelSerializer):
    question = MarketHubQuestionSerializer(many=True, read_only=True)
    cover_image = serializers.ImageField(source="markethub.cover_image")
    title = serializers.CharField(source="markethub.title")
    description = serializers.CharField(source="markethub.description")
     
    class Meta:
        model = MarketHubQuestionModel
        fields = '__all__'


# ************************************************


class MarketHubAwnsereserilizer(serializers.ModelSerializer):
    class Meta:
        model = MarketHubAnswer
        fields = ('is_correct',)


class MarketHubQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketHubQuestionModel
        fields = ('id', 'question_text', 'answers_text',)


class MarketHubSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = MarketHubModel
        fields = "__all__"


class MarketHubSearchSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    class Meta:
        model = MarketHubModel
        fields ="__all__"




class MarketHubDetailSerializer(serializers.ModelSerializer):
   # markethub = MarketHubQuestionSerializer(many=True)
    class Meta:
        model = MarketHubModel
        fields = ("id", "title", "study_field", "cover_image", "data_created",'is_open','author','description')

    def create(self, validated_data):
        questions_data = validated_data.pop('litner', [])
        litner = MarketHubModel.objects.create(**validated_data)
        for question in questions_data:
            print(question)
            MarketHubQuestionModel.objects.create(litner=litner, **question)
        return litner


class MarketHubKarnameDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketHubKarNameDBModel
        fields = ('question', 'is_correct')


class LitnerKarNameSerializer(serializers.ModelSerializer):
    user = UserSerializers()
    exam_id = MarketHubDetailSerializer()

    class Meta:
        model = MarketHubKarNameModel
        fields = '__all__'


class MarketHubTakeExamSerializer(serializers.ModelSerializer):
    karname = MarketHubKarnameDBSerializer(MarketHubKarNameDBModel.objects.all(), many=True)

    class Meta:
        model = MarketHubKarNameModel
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        exam = MarketHubKarNameModel.objects.get(pk=self.context.get('exam'))
        questions = []

        karname = MarketHubKarNameModel.objects.create(user=user, exam_id=exam)
        for question_and_choice in validated_data['karname']:
            question = question_and_choice['question']
            if question.markethub != karname.exam_id:
                continue
            questions.append(question.id)
            is_correct = question_and_choice['is_correct']
            MarketHubKarNameDBModel.objects.create(karname=karname, question=question, is_correct=is_correct)
        question_with_no_answer = exam.markethub.exclude(id__in=questions)
        for question in question_with_no_answer:
            MarketHubKarNameDBModel.objects.create(karname=karname, question=question, is_correct=None)
        return karname

    def update(self, instance, validated_data):
        karname = instance
        for question_and_choice in validated_data['karname']:
            question = question_and_choice['question']
            if question.markethub != karname.exam_id:
                continue
            is_correct = question_and_choice['is_correct']
            answered = MarketHubKarNameDBModel.objects.get(question=question, karname=karname)
            answered.is_correct = is_correct
            answered.save()
        return karname

    


#*******************************************************************
class ClassSerializer(serializers.ModelSerializer):
    markethub = MarketHubSerializer(many=True)
    class Meta: 
        model =Classmodel
        fields = '__all__'

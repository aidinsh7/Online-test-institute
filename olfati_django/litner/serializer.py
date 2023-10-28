from rest_framework import serializers
from litner.models import LitnerModel, LitnerQuestionModel, LitnerKarNameModel, LitnerKarNameDBModel, LitnerModel, \
    LitnerAnswer
from accounts.serializer import UserSerializers


class LitnerAwnsereserilizer(serializers.ModelSerializer):
    class Meta:
        model = LitnerAnswer
        fields = ('is_correct',)


class LitnerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LitnerQuestionModel
        fields = ('id', 'question_text', 'answers_text',)


class LitnerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = LitnerModel
        fields = "__all__"


class LitnerDetailSerializer(serializers.ModelSerializer):
    litner = LitnerQuestionSerializer(many=True)

    class Meta:
        model = LitnerModel
        fields = ("id", "title", "study_field", "author", "cover_image", "data_created", "litner",'is_open')

    def create(self, validated_data):
        questions_data = validated_data.pop('litner', [])
        litner = LitnerModel.objects.create(**validated_data)
        for question in questions_data:
            print(question)
            LitnerQuestionModel.objects.create(litner=litner, **question)
        return litner


class LitnerKarnameDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = LitnerKarNameDBModel
        fields = ('question', 'is_correct')


class LitnerKarNameSerializer(serializers.ModelSerializer):
    user = UserSerializers()
    exam_id = LitnerDetailSerializer()

    class Meta:
        model = LitnerKarNameModel
        fields = '__all__'


class LitnerTakeExamSerializer(serializers.ModelSerializer):
    karname = LitnerKarnameDBSerializer(LitnerKarNameDBModel.objects.all(), many=True)

    class Meta:
        model = LitnerKarNameModel
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        exam = LitnerModel.objects.get(pk=self.context.get('exam'))
        questions = []

        karname = LitnerKarNameModel.objects.create(user=user, exam_id=exam)
        for question_and_choice in validated_data['karname']:
            question = question_and_choice['question']
            if question.litner != karname.exam_id:
                continue
            questions.append(question.id)
            is_correct = question_and_choice['is_correct']
            LitnerKarNameDBModel.objects.create(karname=karname, question=question, is_correct=is_correct)
        question_with_no_answer = exam.litner.exclude(id__in=questions)
        for question in question_with_no_answer:
            LitnerKarNameDBModel.objects.create(karname=karname, question=question, is_correct=None)
        return karname

    def update(self, instance, validated_data):
        karname = instance
        for question_and_choice in validated_data['karname']:
            question = question_and_choice['question']
            if question.litner != karname.exam_id:
                continue
            is_correct = question_and_choice['is_correct']
            answered = LitnerKarNameDBModel.objects.get(question=question, karname=karname)
            answered.is_correct = is_correct
            answered.save()
        return karname

    #

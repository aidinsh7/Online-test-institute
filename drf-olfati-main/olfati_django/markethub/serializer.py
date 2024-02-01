from .models import *
from rest_framework import serializers
from accounts.serializer import UserSerializers


class MarketHubQuestionSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    
    class Meta:
        model = MarketHubQuestionModel
        fields = ("id", "question_text", "answers_text", 'markethub')
        extra_kwargs = {'id': {'read_only': False, 'required': False}}

    def create(self, validated_data):
        validated_data.pop('id', None)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data.pop('id', None)
        return super().update(instance, validated_data)

class MarketHubSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    myclass = serializers.SlugRelatedField(slug_field="id", read_only=True)
    is_paid = serializers.SerializerMethodField(read_only=True)
    have_karname = serializers.SerializerMethodField(read_only=True)
    is_author = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = MarketHubModel
        fields = ('id', 'title', 'description', 'cover_image', 'price', 'data_created', 'author', 'myclass', 'is_paid', 'have_karname', 'is_author')
    def get_is_paid(self, obj):
        request = self.context.get("request")
        return obj.is_paid_user(request.user) or obj.is_author(request.user)
    def get_have_karname(self, obj):
        request = self.context.get("request")
        return obj.have_karname(request.user)
    def get_is_author(self, obj):
        request = self.context.get("request")
        return obj.is_author(request.user)

class MarketHubDetailSerializer(serializers.ModelSerializer):
    questions = MarketHubQuestionSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(slug_field="full_name", read_only=True)
    is_paid = serializers.SerializerMethodField(read_only=True)
    have_karname = serializers.SerializerMethodField(read_only=True)
    is_author = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = MarketHubModel
        fields = ("id", "title", "cover_image", "data_created",'author', 'price', 'description', 'myclass', 'questions', 'have_karname', 'is_paid', 'is_author')

    def get_is_paid(self, obj):
        request = self.context.get("request")
        return obj.is_paid_user(request.user) or obj.is_author(request.user)
    def get_have_karname(self, obj):
        request = self.context.get("request")
        return obj.have_karname(request.user)
    def get_is_author(self, obj):
        request = self.context.get("request")
        return obj.is_author(request.user)

    def create(self, validated_data):
        myclass = validated_data.get('myclass', None)
        request = self.context.get("request")
        if not myclass.author == request.user:
            return PermissionError("اجازه اینکار را ندارید")
        questions_data = validated_data.pop('questions', [])
        markethub = MarketHubModel.objects.create(**validated_data)
        for question in questions_data:
            question.pop('id', None)
            MarketHubQuestionModel.objects.create(**question, markethub=markethub)
        return markethub
    
    
    def update(self, instance, validated_data):
        request = self.context.get("request")
        myclass = validated_data.get('myclass', None)
        questions_data = validated_data.pop('questions', [])
        for question in questions_data:
            question_id = question.get('id', None)
            if question_id:
                try:
                    questionmodel = instance.questions.get(id=question_id)
                    for attr, value in question.items():
                        setattr(questionmodel, attr, value)
                    questionmodel.save()
                except:
                    pass
            else:
                MarketHubQuestionModel.objects.create(**question, markethub=instance)
        if myclass:
            if not myclass.author == request.user:
                return PermissionError
        return super().update(instance, validated_data)
    
class MyClassSerializer(serializers.ModelSerializer):
    markethubs = MarketHubSerializer(many=True, read_only=True)
    paid_users_count = serializers.SerializerMethodField(read_only=True)
    class Meta: 
        model = Myclass
        fields = '__all__'
        read_only_fields = ['author',]

    def get_paid_users_count(self, obj):
        return MarketHubModel.objects.filter(myclass=obj).values('paid_users').distinct().count()

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)

        if not request.parser_context.get("kwargs").get("pk"):
            rep.pop("markethubs", None)
        return rep

    def create(self, validated_data):
        # Associate the authenticated user with the created object
        user = self.context['request'].user
        validated_data['author'] = user
        return super().create(validated_data)
    
class MarketHubKarnameDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketHubKarNameDBModel
        fields = ('question', 'is_correct')

class MarketHubAwnsereserilizer(serializers.ModelSerializer):
    class Meta:
        model = MarketHubAnswer
        fields = ('is_correct',)

class MarketHubSearchSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        model = MarketHubModel
        fields ="__all__"

class MarketHubTakeExamSerializer(serializers.ModelSerializer):
    karname = MarketHubKarnameDBSerializer(MarketHubKarNameDBModel.objects.all(), many=True)

    class Meta:
        model = MarketHubKarNameModel
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        exam = MarketHubModel.objects.get(pk=self.context.get('exam'))
        questions = []

        karname = MarketHubKarNameModel.objects.create(user=user, exam_id=exam)
        for question_and_choice in validated_data['karname']:
            question = question_and_choice['question']
            if question.markethub != karname.exam_id:
                continue
            questions.append(question.id)
            is_correct = question_and_choice['is_correct']
            MarketHubKarNameDBModel.objects.create(karname=karname, question=question, is_correct=is_correct)
        question_with_no_answer = exam.questions.exclude(id__in=questions)
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

    




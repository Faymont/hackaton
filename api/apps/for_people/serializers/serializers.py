""" Сериалайзеры для Rest Api """
from rest_framework import serializers
from apps.for_people.models import Ticket, QuestionSubject, QuestionPolyclinic, \
    AnswerSubject, AnswerPolyclinic


class TicketSerializer(serializers.Serializer):
    """ Сериалайзер для Талонов """
    ticket = serializers.CharField(label='Номер талона')


class QuestionSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSubject
        fields = '__all__'


class QuestionPolyclinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionPolyclinic
        fields = '__all__'


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    answer = serializers.IntegerField()


class ItemsAnswerSerializer(serializers.Serializer):
    answers = serializers.ListField(child=AnswerSerializer())
    ticket = serializers.CharField()

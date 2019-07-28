from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.for_people.models import Ticket, QuestionPolyclinic,\
    QuestionSubject, AnswerPolyclinic, AnswerSubject
from apps.for_people.serializers.serializers import TicketSerializer, QuestionSubjectSerializer,\
    QuestionPolyclinicSerializer, ItemsAnswerSerializer


class TicketView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = TicketSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            ticket = Ticket.objects.get(name=serializer.validated_data['ticket'])
            if ticket.is_passed:
                return Response(_(f'Тест уже пройден'))

            request.session['ticket'] = ticket.name

            question_subject = QuestionSubject.objects.order_by('?')[:3]
            question_polyclinic = QuestionPolyclinic.objects.order_by('?')[:2]

            question_subject_serializer = QuestionSubjectSerializer(question_subject, many=True)
            question_polyclinic_serializer = QuestionPolyclinicSerializer(question_polyclinic, many=True)

            response = question_subject_serializer.data + question_polyclinic_serializer.data
            return Response(response)

        except ObjectDoesNotExist:
            return Response(_(f'Does not exist'))


class QuestionRedeem(APIView):

    def post(self, request, *args, **kwargs):

        serializer = ItemsAnswerSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        ticket = serializer.data['ticket']

        ticket_object = Ticket.objects.get(name=ticket)

        if ticket_object.is_passed:
            return Response(_(f'Тест уже пройден'))

        subject = ticket_object.subject
        polyclinic = subject.polyclinic

        l = list(serializer.data['answers'])

        answer_subject = l[:3]
        answer_polyclinic = l[3:]

        for item in answer_subject:
            id, ans = item.items()
            answer = AnswerSubject.objects.create(
                answer=ans[1],
                subject=subject,
                question_subject=QuestionSubject.objects.get(id=id[1])
            )
            answer.save()

        for item in answer_polyclinic:
            id, ans = item.items()
            answer = AnswerPolyclinic.objects.create(
                answer=ans[1],
                polyclinic=polyclinic,
                question_polyclinic=QuestionPolyclinic.objects.get(id=id[1])
            )
            answer.save()

        ticket_object.is_passed = True
        ticket_object.save()

        return Response(_(f'Ваш подарок!'))

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from .validators import JSONSchemaValidator, DIGIT_JSON_FIELD_SCHEMA


class Ticket(models.Model):
    name = models.IntegerField('Номер талона', unique=True)
    is_passed = models.BooleanField('Пройден',default=False)
    subject = models.OneToOneField(
        'Subject', verbose_name='Пользователь',
        related_name='ticket_subject',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} {self.subject}"

    class Meta:
        verbose_name = _('Номер талона')
        verbose_name_plural = _('Номера талонов')


class Subject(models.Model):
    name = models.CharField('ФИО', default="", max_length=40)
    position = models.CharField('Дожность', default='', max_length=40)

    polyclinic = models.ForeignKey(
        'Polyclinic', verbose_name='Поликлинника',
        related_name='subject_polyclinic',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} {self.position} {self.polyclinic}"

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователь')


class Polyclinic(models.Model):
    name = models.CharField('Поликлинника', default="", max_length=40)
    city = models.ForeignKey(
        'City', verbose_name='Город',
        related_name='polyclinic_city',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} {self.city}"

    class Meta:
        verbose_name = _('Поликлинника')
        verbose_name_plural = _('Поликлинники')


class City(models.Model):
    name = models.CharField('Город', default="", max_length=40)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')


class QuestionPolyclinic(models.Model):
    question = models.CharField('Вопрос', default="", max_length=1000)

    def __str__(self):
        return f"{self.question}"

    class Meta:
        verbose_name = _('Вопрос о поликлиннике')
        verbose_name_plural = _('Воспросы о поликлиннике')


class QuestionSubject(models.Model):
    question = models.CharField('Вопрос', default="", max_length=1000)

    def __str__(self):
        return f"{self.question}"

    class Meta:
        verbose_name = _('Вопрос по персоналу')
        verbose_name_plural = _('Воспросы по персоналу')


class AnswerPolyclinic(models.Model):
    answer = models.IntegerField(default=0)
    polyclinic = models.ForeignKey(
        'Polyclinic', verbose_name='Поликлинника',
        related_name='answer_polyclinic',
        on_delete=models.CASCADE
    )
    question_polyclinic = models.ForeignKey(
        'QuestionPolyclinic', verbose_name='Вопрос',
        related_name='answer_question_polyclinic',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.polyclinic.name} {self.question_polyclinic.question} {self.answer}"

    class Meta:
        verbose_name = _('Ответ о поликлиннике')
        verbose_name_plural = _('Ответы о поликлинниках')


class AnswerSubject(models.Model):
    answer = models.IntegerField(default=0)
    subject = models.ForeignKey(
        'Subject', verbose_name='Поликлинника',
        related_name='answer_subject',
        on_delete=models.CASCADE
    )
    question_subject = models.ForeignKey(
        'QuestionSubject', verbose_name='Вопрос',
        related_name='answer_question_subject',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.subject.name} {self.question_subject.question} {self.answer}"

    class Meta:
        verbose_name = _('Ответ по персоналу')
        verbose_name_plural = _('Ответы по персоналу')

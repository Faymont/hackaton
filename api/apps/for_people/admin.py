from django.contrib import admin

from .models import Subject, Ticket, City, Polyclinic, QuestionPolyclinic, \
    QuestionSubject, AnswerPolyclinic, AnswerSubject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Polyclinic)
class PolyclinicAdmin(admin.ModelAdmin):
    pass


@admin.register(QuestionPolyclinic)
class QuestionPolyclinicAdmin(admin.ModelAdmin):
    pass


@admin.register(QuestionSubject)
class QuestionSubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(AnswerPolyclinic)
class AnswerPolyclinicAdmin(admin.ModelAdmin):
    pass


@admin.register(AnswerSubject)
class AnswerSubjectAdmin(admin.ModelAdmin):
    pass

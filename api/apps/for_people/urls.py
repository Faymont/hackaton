from django.urls import path
from apps.for_people.views import views

app_name = 'for_people'

urlpatterns = [
    path('ticket/', views.TicketView.as_view(), name='ticket'),
    path('redeem/', views.QuestionRedeem.as_view(), name='redeem'),
]

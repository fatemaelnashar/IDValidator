from django.urls import path
from .views import validate_id,get_visits


urlpatterns = [
    path('validator', validate_id, name='validate_id'),
    path('visits/',get_visits,name='get_visit')
]
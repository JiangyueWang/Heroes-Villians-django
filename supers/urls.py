from django.urls import path
from supers import views
urlpatterns = [
    path('api/supers/', views.supers_list),

]

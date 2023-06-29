from django.urls import path
from graphics.views import index
                          

urlpatterns = [
    path('', index, name='home'),
]
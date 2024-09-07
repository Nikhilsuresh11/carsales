import statistics
from django.conf import settings
from django.urls import path
from .views import home, result, about, login_view, contact,upload,upload_result,signup,buy


urlpatterns = [
    path('', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('home/', home, name='home'),
    path('result/', result, name='result'),
    path('about/', about, name='about'),
    path('upload/', upload, name='upload'),
    path('buy/', buy, name='buy'),
    path('upload_result/', upload_result, name='upload_result'),
    path('contact/', contact, name='contact'),
    path('login/', login_view, name='login'),
]



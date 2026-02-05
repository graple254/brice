from django.urls import path
from . views import *

urlpatterns = [
      path('', index, name='index'),
      path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),
      path('dentist/dashboard/', dentist_dashboard, name='dentist_dashboard'),
      path('login/', login_view, name='login'),
      path('logout/', logout_view, name='logout'),

] 
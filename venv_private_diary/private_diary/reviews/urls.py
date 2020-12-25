from django.urls import path

from . import views
app_name = 'reviews'

urlpatterns = [
    path('', views.ReviewsList.as_view(), name='review_list'),
    path('review-detail', views.)
]
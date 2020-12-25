from django.urls import path

from . import views
app_name = 'reviews'

urlpatterns = [
    path('', views.ReviewsList.as_view(), name='review_list'),
    path('review-detail/<int:pk>', views.ReviewsDetail.as_view(), name="review_detail"),
    path('review-create', views.ReviewsCreate.as_view(), name="review_create"),
    path('review-update/<int:pk>', views.ReviewsUpdate.as_view(), name="review_update"),
    path('review-delete/<int:pk>', views.ReviewsDelete.as_view(), name="review_delete"),
]
from django.urls import path
from .views  import SubscriptionApiView,UserRegistrationApiView,UserLoginApiView,FeatureApiView,PlanFeatureAPiView,SubscriptionUpdateApiView,PlanFeatureUpdateAPiView

urlpatterns = [
    path('register/', UserRegistrationApiView.as_view()),
    path('login/', UserLoginApiView.as_view()),
    path('features/', FeatureApiView.as_view()),
    path('plans/', PlanFeatureAPiView.as_view()),
    path('plans/<int:id>/', PlanFeatureUpdateAPiView.as_view()),
    path('subscription/', SubscriptionApiView.as_view()),
    path('subscription/<int:id>/', SubscriptionUpdateApiView.as_view())

]

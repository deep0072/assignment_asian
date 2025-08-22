
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Subscription, Feature, Plan
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import (
    SubscriptionSerializer, UserInfoSerializer, UserLoginSerializer,
    FeatureSerializer, PlanSerializer, PlanSerializerData,
    SubscriptionSerializerData
)
from rest_framework import status
from django.db.models import F
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist


class AdminClass(APIView):

    def get_permissions(self):
        """Override to set permissions per method."""
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        elif self.request.method == 'GET':
           
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

class UserRegistrationApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        # raise_exception=True handles 400 automatically, but for completeness
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=request.data['username'], password=request.data['password'])
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({"error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeatureApiView(AdminClass):
    def post(self, request):
        serializer = FeatureSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Feature created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        features = Feature.objects.all()
        serializer = FeatureSerializer(features, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PlanFeatureAPiView(AdminClass):
    def post(self, request):
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Plan created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        plans = Plan.objects.prefetch_related('features').all()
        serializer = PlanSerializerData(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PlanFeatureUpdateAPiView(AdminClass):
    def put(self, request, id):
        try:
            plan = Plan.objects.get(id=id)
            serializer = PlanSerializer(plan,data=request.data,partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "Plan Updated successfully"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlanSerializer(plan, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Plan updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubscriptionApiView(APIView):
    def post(self, request):

        request.data['user']=request.user.id        
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Subscription created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        subscriptions = request.user.subscriptions.select_related('plan').prefetch_related('plan__features').all()
        serializer = SubscriptionSerializerData(subscriptions, many=True)
        if serializer.data:
             
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "no active subscription available"},status=status.HTTP_404_NOT_FOUND)

class SubscriptionUpdateApiView(APIView):
    """update subscription, user can deactivate and plan also can be changed"""
    def put(self, request, id):
        try:
            subscription = Subscription.objects.get(id=id,user=request.user,is_active=True)
        except ObjectDoesNotExist:
            return Response({"error": "Subscription not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubscriptionSerializer(subscription, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Subscription updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



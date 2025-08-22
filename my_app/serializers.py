from rest_framework import serializers
from django.contrib.auth.models import User
from .models import  Subscription, Plan, Feature
from django.utils import timezone

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    features = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Feature.objects.all()       # ← makes the field write-enabled
    )
    class Meta:
        model = Plan
        fields = '__all__'


    def create(self, validated_data):     
        feature_objects = validated_data.pop('features', [])       
        plan = Plan.objects.create(**validated_data)
        plan.features.set(feature_objects)
        return plan
        
class PlanSerializerData(serializers.ModelSerializer):
    features = FeatureSerializer(
        many=True,
          
    )
    class Meta:
        model = Plan
        fields = ('id','name', "features")




class SubscriptionSerializer(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(
      
        many=False,queryset=Plan.objects.filter()
    )   

    class Meta:
        model = Subscription
        fields = ('id', 'start_date', 'is_active', 'plan','user')
 


   



        

class SubscriptionSerializerData(serializers.ModelSerializer):
    plan = PlanSerializerData()

    class Meta:
        model = Subscription
        fields = ('id', 'start_date', 'is_active', 'plan','user')
    
   
 



class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model  = User
        fields = ('id','username', 'email','password')

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
   
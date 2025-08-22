from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Subscription, Plan, Feature  # Adjust import if needed

class SubscriptionTests(APITestCase):
    def setUp(self):
        # Create a test user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        
        # Create test data (feature and plan)
        self.feature = Feature.objects.create(name='Test Feature')
        self.plan = Plan.objects.create(name='Test Plan')
        self.plan.features.add(self.feature)

    def test_subscription_creation(self):
        url = '/api/subscription/'  # Your POST endpoint for creation
        data = {'plan': self.plan.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(Subscription.objects.first().plan, self.plan)

    def test_switch_plan(self):
        # Create an initial subscription
        subscription = Subscription.objects.create(user=self.user, plan=self.plan)
        
        # Create a new plan to switch to
        new_plan = Plan.objects.create(name='New Plan')
        
        url = f'/api/subscription/{subscription.id}/'  # Your PUT endpoint for update
        data = {'plan': new_plan.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh and verify the plan was switched
        subscription.refresh_from_db()
        self.assertEqual(subscription.plan, new_plan)

    def test_retrieve_list_with_nested(self):
        # Create a subscription to list
        Subscription.objects.create(user=self.user, plan=self.plan)
        
        url = '/api/subscription/'  # Your GET endpoint for listing
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Ensure data is returned
        self.assertIn('plan', response.data[0])  # Check nested plan
        print(response.data, "plan")
        self.assertNotIn('user', response.data)  # Check nested features

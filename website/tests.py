from django.test import TestCase
from django.test.client import Client
from .urls import reverse
import unittest
from .views import *
import random

class MainSiteTestCase(TestCase):
    """
    this tests the main functionalities of the site
    to make sure it works appropiately.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='tester',
                                        email='test_me@testing.com',
                                        password="GPC2021")
        self.user._password = "GPC2021"
        self.client = Client()


    def test_login_ok(self):
        """
        tests the login is loading ok
        :return: error if any
        """
        endpoint = 'website:login'
        response = self.client.get(reverse(endpoint))
        self.assertTrue(response.status_code == 200,"There's a problem with your request.")

    def test_post_login(self):
        """
        tries to log in
        :return:
        """
        endpoint = reverse("website:login")
        data = {
            'email': self.user.email,
            'password': self.user._password
        }
        response = self.client.post(path=endpoint,data=data)
        self.assertEqual(response.status_code,302, "The login has failed.")
        self.assertNotIn('Login', response.content.decode(), "You weren't capable of logging in")
        self.assertNotIn('error', response.content.decode(), "You weren't capable of logging in")

    @unittest.expectedFailure
    def test_post_login_fail(self):
        """
        tries to login without credentials
        :return:
        """
        endpoint = reverse("website:login")

        data = {
            'email': "",
            'password': self.user.password
        }
        response = self.client.post(path=endpoint, data=data)
        print(dir(response))
        self.assertIn('error', response.content.decode(), "You weren't capable of logging in")

    @unittest.expectedFailure
    def test_dashboard_access_denied(self):
        endpoint = 'website:dashboard'
        response = self.client.get(reverse(endpoint))
        self.assertTrue('dashboard' in response.url, "There's a problem with your request.")


    def test_objective_listing(self):
        """
        tests the response of the listing items
        :return: error if any
        """
        endpoint = reverse('website:list_objectives')
        token = Token.objects.get_or_create(user=self.user)[0]
        data = {
            'authtoken': token.key
        }
        response = self.client.get(path=endpoint,data=data)
        self.assertEqual(response.status_code,200,
                         f"Error: {response.json()['error'] if 'error' in response.json().keys() else response.json()}")
        self.assertIn('objective_list' , response.json().keys(),"The request was a success but it didn't render the list")



    def test_objective_creation(self):
        """
        tests how the objects are created
        :return: error if any
        """
        endpoint = reverse('website:handle_objective')
        token = Token.objects.get_or_create(user=self.user)[0]
        data = {
            'authtoken': token.key,
            'goals': json.dumps([1,2,3]),
            'goals_description':json.dumps(['simple goal','simple goal','simple goal']),
            'consecution_percentages':json.dumps([20,30,50]),
            'description':'adding new values for our clients',
            'metric': 'new increases for clients',
            'new_x': 2.0,
        }
        response = self.client.post(path=endpoint, data=data)
        self.assertEqual(response.status_code, 200,
                         f"Error: {response.json()['error'] if 'error' in response.json().keys() else response.json()}")


    @unittest.expectedFailure
    def test_objective_creation_fail(self):
        """
        tests how the objects are created
        :return: error if any
        """
        endpoint = reverse('website:handle_objective')
        token = Token.objects.get_or_create(user=self.user)[0]
        data = {
            'authtoken': token.key,
            'goals': json.dumps([1, 2, 3]),
            'goals_description': json.dumps(['simple goal', 'simple goal', 'simple goal']),
            'consecution_percentages': json.dumps([20, 30]),
            'description': 'adding new values for our clients',
            'metric': 'new increases for clients',
            'new_x': 10.0,

        }
        response = self.client.post(path=endpoint, data=data)
        self.assertEqual(response.status_code, 200,
                         f"Error: {response.json()['error'] if 'error' in response.json().keys() else response.json()}")

    @unittest.expectedFailure
    def test_objective_creation_fail_http_method_type(self):
        """
        tests how the objects are created
        :return: error if any
        """
        endpoint = reverse('website:handle_objective')
        token = Token.objects.get_or_create(user=self.user)[0]
        data = {
            'authtoken': token.key,
            'goals': json.dumps([1, 2, 3]),
            'goals_description': json.dumps(['simple goal', 'simple goal', 'simple goal']),
            'consecution_percentages': json.dumps([20, 30, 50]),
            'description': 'adding new values for our clients',
            'metric': 'new increases for clients',
            'new_x': 10.0,
        }
        response = self.client.get(path=endpoint, data=data)
        self.assertEqual(response.status_code, 200,
                        f"Error: {response.json()['error'] if 'error' in response.json().keys() else response.json()}")

    def test_objective_update(self):
        """
        tests how the objects are created
        :return: error if any
        """
        endpoint = reverse('website:handle_objective')
        token = Token.objects.get_or_create(user=self.user)[0]
        objective = Objective.objects.create(metric='new increases for clients',
                                             description='adding new values for our clients')
        goals = [
            {'goal':90.99,
             'consecution_percentage':20.00,
             'description':'test goal'
             },

            {'goal': 300.99,
             'consecution_percentage': 60.00,
             'description': 'test goal'
             },
        ]
        for goal in goals:
            ObjectiveGoal.objects.update_or_create(objective=objective,
                                        goal=goal['goal'],
                                        description=goal['description'],
                                        consecution_percentage=goal['consecution_percentage'])
        data = {
            'authtoken': token.key,
            'goals': json.dumps([g.goal for g in objective.objectivegoal_set.all()]),
            'goals_description': json.dumps([g.description for g in objective.objectivegoal_set.all()]),
            'consecution_percentages': json.dumps([g.consecution_percentage for g in objective.objectivegoal_set.all()]),
            'description': 'adding new values for ourselves',
            'objective_id': objective.id,
            'new_x': 91.0,
            'metric': objective.metric,
        }
        response = self.client.post(path=endpoint, data=data)
        self.assertEqual(response.status_code, 200,
                         f"Error: {response.json()['error'] if 'error' in response.json().keys() else response.json()}")


    @unittest.expectedFailure
    def test_objective_update_fail(self):
        """
        tests how the objects are created
        :return: error if any
        """
        endpoint = reverse('website:handle_objective')
        token = Token.objects.get_or_create(user=self.user)[0]
        objective = Objective.objects.create(metric='new increases for clients',
                                             description='adding new values for our clients')
        goals = [
            {'goal': 90.99,
             'consecution_percentage': 20.00,
             'description': 'test goal'
             },

            {'goal': 300.99,
             'consecution_percentage': 60.00,
             'description': 'test goal'
             },
        ]
        for goal in goals:
            ObjectiveGoal.objects.update_or_create(objective=objective,
                                                   goal=goal['goal'],
                                                   description=goal['description'],
                                                   consecution_percentage=goal['consecution_percentage'])
        data = {
            'authtoken': token.key,
            'goals': json.dumps([g['description'] for g in goals]),
            'goals_description': json.dumps([g['description'] for g in goals]),
            'consecution_percentages': json.dumps([1]),
            'description': 'adding new values for ourselves',
            'new_x':10.0,
            'metric': objective.metric,
        }
        response = self.client.post(path=endpoint, data=data)
        self.assertEqual(response.status_code, 200,
                         f"Error: {response.json()['error'] if 'error' in response.json().keys() else response.json()}")

    def test_objective_deletion(self):
        """
        tests if the object is removed
        :return: error if any
        """
        token = Token.objects.get_or_create(user=self.user)[0]
        objective = Objective.objects.create(metric='new increases for clients',
                                             description='adding new values for our clients')
        endpoint = reverse('website:delete_objective',kwargs={'objective_id':objective.id})
        data = {
            'authtoken': token.key,
        }
        response = self.client.post(endpoint,data=data)
        self.assertEqual(response.status_code,200,
                         f"Error: {response.json()['error'] if 'error' in response.json().keys() else response.json()}")


    @unittest.expectedFailure
    def test_objective_deletion_fail(self):
        """
        tests if the object is removed
        :return: error if any
        """
        token = Token.objects.get_or_create(user=self.user)[0]
        objective = Objective.objects.create(metric='new increases for clients',
                                             description='adding new values for our clients')
        endpoint = reverse('website:delete_objective', kwargs={'objective_id': random.randrange(249)})
        data = {
            'authtoken': token.key,
        }
        response = self.client.post(endpoint, data=data)
        self.assertEqual(response.status_code, 200,
                         f"Error: {response.json()['error'] if 'error' in response.json().keys() else response.json()}")


    def tearDown(self):
        del self.user
        super().tearDown()



class HelpersTestCase(TestCase):
    """
    tests all helpers used in order
    to manage the data, access and
    perform operations needed for information proces
    """

    def setUp(self):
        self.user = User.objects.create_user(username='tester',
                                        email='test_me@testing.com',
                                        password="GPC2021")
        self.goals = [x for x in range(1, 100, 10)]
        self.consecution_percentages = [x for x in range(100, 200, 10)]


    def test_linear_interpolation(self):
        """
        tests the lineal interpolation calculation
        :return: error if any
        """
        dif =calculate_lineal_interpolation(x_values=self.goals,
                                            x_new=random.randrange(self.goals[0],self.goals[-1]),
                                       y_values=self.consecution_percentages,
                                       order=random.choice(['asc','desc']))
        print("INTERPOLATION",dif,self.goals,self.consecution_percentages)
        self.assertIn('interpolation',dif.keys(),f'{dif["error"] if "error" in dif.keys() else "ERROR"}')
        self.assertIsInstance(dif['interpolation'],float,f'{dif["error"] if "error" in dif.keys() else "ERROR"}')


    @unittest.expectedFailure
    def test_linear_interpolation_fail(self):
        """
        tests the lineal interpolation calculation
        :return: error if any
        """
        dif = calculate_lineal_interpolation(x_values=self.goals,
                                             x_new=0.00,
                                             y_values=self.consecution_percentages,
                                             order=random.choice(['asc', 'desc']))
        self.assertIn('interpolation',dif.keys(),f'{dif["error"] if "error" in dif.keys() else "ERROR"}')
        self.assertIsInstance(dif['interpolation'],float,f'{dif["error"] if "error" in dif.keys() else "ERROR"}')


    def test_validate_goal_order(self):
        """
        tests the goal order evaluation
        :return: error if any
        """
        result = validate_goal_order(self.goals, self.consecution_percentages)
        self.assertTrue(result['status'],
                        f"Error: {result['error'] if 'error' in result.keys() else result}")


    @unittest.expectedFailure
    def test_validate_goal_order_fail(self):
        """
        tests the goal order evaluation
        :return: error if any
        """
        result = validate_goal_order(self.goals, self.consecution_percentages.reverse())
        self.assertTrue(result['status'], f"{result['error']}")

    def test_validate_token(self):
        """
        validates if the token has been validated
        :return: error if any
        """
        token = Token.objects.get_or_create(user=self.user)[0]
        validated = validate_token(token)
        self.assertTrue(validated,"ERROR: The token is not valid")


    @unittest.expectedFailure
    def test_validate_token_fail(self):
        """
        tries to validate if the value is actually working.
        :return: error if any
        """
        token = " "
        validated = validate_token(token)
        self.assertTrue(validated, "ERROR: The token is not valid")


    def tearDown(self):
        del self.user
        super().tearDown()
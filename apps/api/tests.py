from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserManager

User = get_user_model()

class UserManagerTestClass(TestCase):
    """
    Test class for UserModel
    """
    def test_create_user(self):
        """
        Test case for checking create_user method
        """
        self.new_user = User.objects.create_user(first_name='John', last_name='Doe', username='john_doe', email='johndoe@example.com', password='test_password')

        self.assertEqual(self.new_user.first_name, 'John')
        self.assertEqual(self.new_user.last_name, 'Doe')
        self.assertEqual(self.new_user.username, 'john_doe')
        self.assertEqual(self.new_user.email, 'johndoe@example.com')
        self.assertTrue(self.new_user.check_password('test_password'))

class UserTestClass(TestCase):
    """
    Class for testing User
    """
    def setUp(self):
        """
        Runs after each test case
        """
        self.new_user = User.objects.create_user(first_name='John', last_name='Doe', username='john_doe', email='johndoe@example.com', bio='I am new here.', password='test_password')

    def tearDown(self):
        """
        Runs after each test case
        """
        User.objects.all().delete()

    def test_user_instance(self):
        """
        Test case to check if self.new_user is instance of User model
        """
        self.assertIsInstance(self.new_user, User)

from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserManager
from cloudinary.uploader import destroy

User = get_user_model()


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

    def test_create_user(self):
        """
        Test case for create_user method
        """
        self.assertEqual(self.new_user.first_name, 'John')
        self.assertEqual(self.new_user.last_name, 'Doe')
        self.assertEqual(self.new_user.username, 'john_doe')
        self.assertEqual(self.new_user.email, 'johndoe@example.com')
        self.assertTrue(self.new_user.check_password('test_password'))
        self.assertFalse(self.new_user.is_staff)
        self.assertFalse(self.new_user.is_superuser)
        self.assertFalse(self.new_user.is_active)

        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name='', last_name='', username='', email='', bio='', password=''
            )

    def test_create_superuser(self):
        """
        Test case for checking create_superuser method
        """
        superuser = User.objects.create_superuser(
            first_name='Jane', last_name='Doe', username='jane_doe', email='janedoe@example.com', bio='I am new here.', password='test_password'
        )

        self.assertEqual(self.new_user.first_name, 'John')
        self.assertEqual(self.new_user.last_name, 'Doe')
        self.assertEqual(self.new_user.username, 'john_doe')
        self.assertEqual(self.new_user.email, 'johndoe@example.com')
        self.assertTrue(self.new_user.check_password('test_password'))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                first_name='', last_name='', username='', email='', bio='', password=''
            )
    def test_upload_profile_pic(self):
        """
        Test case for checking is method uploads picture
        """
        url = 'https://cdn.business2community.com/wp-content/uploads/2017/08/blank-profile-picture-973460_640.png'

        self.details = self.new_user.upload_profile_pic(url)

        self.test = self.assertEqual(self.new_user.profile_pic, details.get('url'))


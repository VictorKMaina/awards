from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserManager, Project
from cloudinary.uploader import destroy
from apps.api.models import Review

User = get_user_model()


class UserTestClass(TestCase):
    """
    Class for testing User
    """

    def setUp(self):
        """
        Runs after each test case
        """
        self.new_user = User.objects.create_user(first_name='John', last_name='Doe', username='john_doe', email='johndoe@example.com', bio='I am new here.', password='test_password', website='example.com', social_media={
            'facebook':'Facebook link',
            'Dribble': 'Dribble link',
        })

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
        
        # Test if is_staff is set to True
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                first_name='Jane', last_name='Doe', username='jane_doe', email='janedoe@example.com', bio='I am new here.', password='test_password', is_staff = False,
            )
        
    def test_upload_profile_pic(self):
        """
        Test case for checking is method uploads picture
        """
        url = 'https://cdn.business2community.com/wp-content/uploads/2017/08/blank-profile-picture-973460_640.png'

        details = self.new_user.upload_profile_pic(url)

        self.assertEqual(self.new_user.profile_pic, details.get('url'))
        destroy(details.get('public_id'))

        # Test if invalid image path is inserted
        with self.assertRaises(Exception):
            details = self.new_user.upload_profile_pic('Random path')
            self.assertEqual(self.new_user.profile_pic, details.get('url'))

class ProjectTest(TestCase):
    """
    Class for testing Project model
    """
    def setUp(self):
        self.new_user = User.objects.create_user(first_name='John', last_name='Doe', username='john_doe', email='johndoe@example.com', bio='I am new here.', password='test_password', website='example.com', social_media={
            'facebook': 'Facebook link',
            'Dribble': 'Dribble link',
        })

        self.new_project = Project.objects.create(title = "New Project", description = 'This is a new project.', site_url = "https://www.example.com", user = self.new_user)

    def tearDown(self):
        """
        Runs after each test case
        """
        User.objects.all().delete()
        Project.objects.all().delete()

    def test_instance(self):
        """
        Test case to check if self.new_project is instance of Project
        """
        self.assertIsInstance(self.new_project, Project)
    
    def test_project_database(self):
        """
        Test to check if Project is being saved to the database
        """
        self.new_project.save()
        projects = Project.objects.all()
        self.assertTrue(len(projects) > 0)

    def test_uploading_landing_page(self):
        """
        Test case to check is method uploads landing page image to CLoudinary
        """
        self.new_project.save()
        url = 'https://themes.getbootstrap.com/wp-content/uploads/2019/08/quick-website-ui-kit-1.1.0-cover.jpg'
        details = self.new_project.upload_landing_page(url)

        self.assertEqual(self.new_project.landing_page_image, details.get('url'))

        destroy(details.get('public_id'))

    def test_average_rating(self):
        """
        Test case to see if average rating property is set by number of reviews
        """
        self.new_project.save()

        review1 = Review.objects.create(project = self.new_project, user = self.new_user, design = 8, usability = 5, content = 9, comment = 'This is a nice website.')

        review2 = Review.objects.create(project = self.new_project, user = self.new_user, design = 6, usability = 5, content = 3, comment = 'This is a nice website.')

        self.assertEqual(self.new_project.average_rating, 6.0)


    def test_find_by_id(self):
        """
        Test case to check id class method project instance
        """
        self.new_project.save()
        project = Project.find_by_id(self.new_project.id)
        self.assertEqual(project, self.new_project)

    def test_find_by_user(self):
        """
        Test case to ckeck if class method returns queryset of projects by user
        """
        self.new_project.save()

        projects = Project.find_by_user(self.new_user)
        self.assertTrue(len(projects) > 0)

class ReviewTest(TestCase):
    """
    Class for testing Review model
    """
    def setUp(self):
        """
        Runs before each test case
        """
        self.new_user = User.objects.create_user(first_name='John', last_name='Doe', username='john_doe', email='johndoe@example.com', password='test_password')

        self.new_project = Project.objects.create(
            title="New Project", description='This is a new project.', site_url="https://www.example.com", user=self.new_user)

        self.new_review = Review.objects.create(project = self.new_project, user = self.new_user, design = 5, usability = 6, content = 7, comment="This is a nice website.")

    def tearDown(self):
        """
        Runs after each test case
        """
        User.objects.all().delete()
        Project.objects.all().delete()
        Review.objects.all().delete()

    def test_instance(self):
        """
        Test is self.new_review is instance of Review
        """
        self.assertIsInstance(self.new_review, Review)

    def test_database(self):
        """
        Test to check if object is being added to database with proper properties
        """
        review = Review(project=self.new_project, user=self.new_user, design=7, usability=6, content=5, comment="This is a nice website.")
        review.save()
        reviews = Review.objects.all()

        self.assertTrue(len(reviews) > 0)

    def test_find_by_project(self):
        """
        Test case to  see if class method returs queryset of reviews by project
        """
        reviews = Review.find_by_project(self.new_project)
        self.assertTrue(len(reviews) > 0)
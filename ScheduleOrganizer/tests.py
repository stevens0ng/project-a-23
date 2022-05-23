from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from ScheduleOrganizer.models import course, assignment

# Create your tests here.

#google authentication tests
class authTests(TestCase):

    #set up with dummy user
    def setUp(self):
        # User = get_user_model()
        # user = User.objects.create(username='testuser', email='cs3240testuser@gmail.com', password= 'Thisisjustatest123!')
        # user.save()

        self.user={
            'email': 'cs3240testuser@gmail.com',
            'username': 'testuser',
            'password': 'Thisisjustatest123!'
        }


    #testing page access
    def test_page_access(self):
        response=self.client.get('/accounts/login/')
        self.assertEqual(response.status_code,200)
        #self.assertTemplateUsed(response,'auth/login.html')
    #testing with gmail account
    def test_gmail_login(self):

        User = get_user_model()
        user = User.objects.create(username='testuser', email='cs3240testuser@gmail.com', password= 'Thisisjustatest123!')
    
        
        self.client.post('/accounts/social/signup/',self.user, format='text/html')
        user.save()
        response = self.client.post('/accounts/login/', self.user, format='text/html')
        self.assertEqual(response.status_code, 200)

    # def test_nongmail_login(self):
    #     c = Client()
    #     response = c.post('/accounts/login/', {'username': 'testuser', 'email': 'cs3240testuser@yahoo.com', 'password1': 'Thisisjustatest123!'}, secure = True)
    #     logged_in = self.client.login(username = 'testuser', password='Thisisjustatest123!')
    #     self.assertTrue(response.status_code >=400 and response.status_code <=499)

class funcTests(TestCase):
    def setUp(self):
        self.user = {
            'email': 'cs3240testuser@gmail.com',
            'username': 'testuser',
            'password': 'Thisisjustatest123!'
        }

        assignment.objects.create(title='Blank', due_date='Tomorrow',description='sprint check', complete=False)
        course.objects.create(name='2150', section='001')
        course.objects.create(name='1110', section='002')


    def testManyToManyAdd(self):
        User = get_user_model()
        user1 = User.objects.create(username='testuser', email='cs3240testuser@gmail.com', password='Thisisjustatest123!')
        course1=course.objects.get(name='1110')
        course1.users.add(user1)
        self.assertTrue(user1 in course1.users.all())
    def testManyToManyRemove(self):
        User = get_user_model()
        user1 = User.objects.create(username='testuser', email='cs3240testuser@gmail.com', password='Thisisjustatest123!')
        course1=course.objects.get(name='1110')
        course1.users.add(user1)
        course1.users.remove(user1)
        self.assertFalse(user1 in course1.users.all())

    def testAssignmentGenerate(self):
        assignment1 = assignment.objects.get(title='Blank')
        self.assertTrue(assignment1.due_date=='Tomorrow')



class DummyTestCase(TestCase):
    def setup(self):
        x=1
        y=2
    def test_dummy_test(self):
        self.assert_(1,1)


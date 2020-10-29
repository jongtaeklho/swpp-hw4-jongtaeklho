from django.test import TestCase, Client
import json
from .models import Article,Comment
from django.contrib.auth.models import User

class BlogTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='jongtaek',password='1234')
        User.objects.create_user(username='swpp',password='iluvswpp')
    def test_csrf(self):
        # By default, csrf checks are disabled in test client
        # To test csrf protection we enforce csrf checks here
   
        client = Client(enforce_csrf_checks=True)
        response = client.post('/api/signup', json.dumps({'username': 'chris', 'password': 'chris'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 403)  # Request without csrf token returns 403 response

        response = client.get('/api/token')
        csrftoken = response.cookies['csrftoken'].value  # Get csrf token from cookie

        response = client.post('/api/signup', json.dumps({'username': 'chris', 'password': 'chris'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 201)  # Pass csrf protection
        response = client.put('/api/signup', json.dumps({'username': 'chris', 'password': 'chris'}),
                               content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)  # Pass csrf protection
    def test_token(self):
        client=Client()
        response = client.post('/api/token')
        self.assertEqual(response.status_code,405)
    def test_signup(self):
        client=Client()
        response = client.get('/api/token')
        csrftoken = response.cookies['csrftoken'].value
        response=client.post('/api/signup',json.dumps({'username':'jongtak','passord':'1234'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,400)
    def test_signin(self):
        client=Client()
        response = client.get('/api/token')
        csrftoken = response.cookies['csrftoken'].value
        response=client.post('/api/signin',json.dumps({'username':'jongtak','password':'1234'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,401)
        response=client.post('/api/signin',json.dumps({'username':'jongtaek','password':'134'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,401)                                
        response=client.post('/api/signin',json.dumps({'username':'jongtaek','password':'1234'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,204)
        response=client.post('/api/signin',json.dumps({'usernam':'jongtak','password':'1234'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,400)
        response=client.get('/api/signin', 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,405)
    def test_signout(self):
        client=Client()
        response = client.get('/api/token')
        csrftoken = response.cookies['csrftoken'].value
        response=client.get('/api/signout',content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,401)
        response=client.post('/api/signin',json.dumps({'username':'jongtaek','password':'1234'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        response=client.get('/api/signout',content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,204)
        response=client.post('/api/signout',json.dumps({'username':'jongtaek','password':'1234'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,405)       

    def test_article(self):
        client=Client()
        response = client.get('/api/token')
        csrftoken = response.cookies['csrftoken'].value
        response=client.get('/api/article',content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,401)
        response=client.post('/api/signin',json.dumps({'username':'jongtaek','password':'1234'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        response=client.get('/api/article', 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,200)
        response=client.post('/api/article',json.dumps({'title':'jongtaek','content':'hi'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,201)
        response=client.post('/api/article',json.dumps({'tite':'jongtaek','content':'hi'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,400)
        response=client.put('/api/article',json.dumps({'username':'jongtaek','password':'1234'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,405)   
    def test_article_info(self):
        client=Client()
        response = client.get('/api/token')
        csrftoken = response.cookies['csrftoken'].value
        response=client.get('/api/article/2',content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,401)
        response=client.post('/api/signin',json.dumps({'username':'jongtaek','password':'1234'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        response=client.post('/api/article',json.dumps({'title':'jongtaek','content':'hi'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        response=client.post('/api/article',json.dumps({'title':'jongtaek','content':'hi'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        response=client.get('/api/article/1',content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,200)    
        response=client.put('/api/article/1',json.dumps({'title':'jongtaek','content':'hiii'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,200)
        response=client.put('/api/article/1',json.dumps({'tite':'jongtaek','content':'hiii'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,400)
        response=client.delete('/api/article/1', 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,200)
        response=client.get('/api/signout',content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        response = client.get('/api/token')
        csrftoken = response.cookies['csrftoken'].value
        response=client.post('/api/signin',json.dumps({'username':'swpp','password':'iluvswpp'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,204)
        response=client.put('/api/article/2',json.dumps({'title':'jongtaek','content':'hiii'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,401)
        response=client.delete('/api/article/2', 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,401)   
        response=client.post('/api/article/2',json.dumps({'title':'jongtaek','content':'hiii'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,405)


    def test_comment(self):
        client=Client()
        response = client.get('/api/token')
        csrftoken = response.cookies['csrftoken'].value
        response=client.get('/api/article/1/comment',content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,401)
        client.post('/api/signin',json.dumps({'username':'jongtaek','password':'1234'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        client.post('/api/article',json.dumps({'title':'jongtaek','content':'hi'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        response=client.post('/api/article/1/comment',json.dumps({'content':'hi'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,201)
        response=client.post('/api/article/1/comment',json.dumps({'cotent':'hi'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,400)
        response=client.get('/api/article/1/comment',content_type='application/json',
                                        HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,200)
        response=client.put('/api/article/1/comment',json.dumps({'content':'hi'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,405)
    
    def test_comment_info(self):
        client=Client()
        response = client.get('/api/token')
        csrftoken = response.cookies['csrftoken'].value
        response=client.get('/api/comment/1',content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,401)
        client.post('/api/signin',json.dumps({'username':'jongtaek','password':'1234'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        client.post('/api/article',json.dumps({'title':'jongtaek','content':'hi'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        response=client.post('/api/article/1/comment',json.dumps({'content':'hi'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        response=client.post('/api/article/1/comment',json.dumps({'content':'hii'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        response=client.put('/api/comment/1',json.dumps({'content':'hiii'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,200)
        response=client.put('/api/comment/1',json.dumps({'contnt':'hiii'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,400)
        response=client.delete('/api/comment/1',content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,200)
        response=client.get('/api/signout',content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        response = client.get('/api/token')
        csrftoken = response.cookies['csrftoken'].value
        response=client.post('/api/signin',json.dumps({'username':'swpp','password':'iluvswpp'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,204)
        response=client.put('/api/comment/2',json.dumps({'content':'hiii'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,401)
        response=client.delete('/api/comment/2',content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,401)
        response=client.get('/api/comment/2',content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,200)
        response=client.post('/api/comment/2',json.dumps({'content':'hiii'}), 
                                        content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code,405)

        
        

       


        
        


    
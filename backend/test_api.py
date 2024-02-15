import unittest
from main import create_app
from config import TestConfig
from exts import db

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app(TestConfig)
        self.client=self.app.test_client(self)
        

        with self.app.app_context():
      

            db.create_all()
    
    def test_hello_world(self):
        hello_world_response=self.client.get('/recipe/hello')

        json=hello_world_response.json

        self.assertEqual(json,{"message":"Hello World!"})
    
    def test_signup(self):
        signup_response=self.client.post('/auth/signup',
            json={
                "username":"testuser",
                "email":"testuser@gmail.com",
                "password":"password"
            }                                 
        )

        status_code=signup_response.status_code

        self.assertEqual(status_code, 201)
    
    def test_login(self):
        login_response=self.client.post('/auth/login',
        json={
                "username":"testuser",
                "password":"password"
             }
        )

        status_code = login_response.status_code
        self.assertEqual(status_code,200)
    
    def test_get_all_recipes(self):
        response=self.client.get('/recipe/recipes')
        status_code= response.status_code
        self.assertEqual(status_code,200)
    def test_get_one_recipe(self):
        id=1
        response=self.client.get(f'/recipe/recipe/{id}')
        status_code=response.status_code
        self.assertEqual(status_code, 404)
    def test_crud_recipe(self):
        signup_response=self.client.post('/auth/signup',
            json={
                "username":"testuser",
                "email":"testuser@gmail.com",
                "password":"password"
            }                                 
        )

        login_response=self.client.post('/auth/login',
        json={
                "username":"testuser",
                "password":"password"
             }
        )
        access_token=login_response.json['access_token']
        create_response=self.client.post('/recipe/recipes',
        json={
	            "title": "Test bar",
	            "description": "This is how to make the delicious test bar"
            },
        headers={
            "Authorization":f"Bearer {access_token}"
            }
        )

        create_response_status_code=create_response.status_code

        update_response=self.client.put('/recipe/recipe/1',
        json={
	            "id":"1",
                "title": "Test bar update",
	            "description": "This is how to make the delicious updated test bar"
            },
        headers={
            "Authorization":f"Bearer {access_token}"
            }
        )

        update_response_status_code=update_response.status_code

        delete_response=self.client.delete('/recipe/recipe/1',

        headers={
            "Authorization":f"Bearer {access_token}"
            }
        )

        delete_response_status_code=delete_response.status_code

        self.assertEqual(create_response_status_code,201)
        self.assertEqual(update_response_status_code,200)
        self.assertEqual(delete_response_status_code,200)



        
    def test_delete_recipe(self):
        pass
            

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__=="__main__":
    unittest.main()            
try:
    from company import app
    import unittest

except Exception as e:
    print("Some Modules are missing {}".format(e))
    

class FlaskTest(unittest.TestCase):
    
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode,200)
        
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.content_type,"text/html; charset=utf-8")
     
if __name__ == '__main__':
    unittest.main()
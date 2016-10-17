from locust import HttpLocust, TaskSet, task
from bs4 import BeautifulSoup

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()
    def login(self):
        response = self.client.post("/clogin", {"email":"kr.prithvi@gmail.com", "password":"ambigous"})
    @task
    def tutorial(self):
        for i in range(1,5):
            with self.client.get("/tutorial/%i" % i, name="/tutorial?i=[i]", catch_response=True) as response:
                title = BeautifulSoup(response.content).title.string
                print title
                if title != "Tutorial %i" % i:
                    response.failure("Got wrong response")
    @task
    def home(self):
        with self.client.get("/index", catch_response=True) as response:
            title = BeautifulSoup(response.content).title.string
            print title
            if title != "Home":
                response.failure("Got wrong response")
            
    @task
    def admin(self):
        with self.client.get("/admin", catch_response=True) as response:
            title = BeautifulSoup(response.content).title.string
            print title
            if title != "Admin":
                response.failure("Got wrong response")

    @task
    def quizzler(self):
        with self.client.get("/quizzler", catch_response=True) as response:
            title = BeautifulSoup(response.content).title.string
            print title
            if title != "Quizzler":
                response.failure("Got wrong response")
    @task
    def quiz(self):
        for i in range(1,4):
            with self.client.get("/quiz/%i" % i, name="/quiz?i=[i]", catch_response=True) as response:
                title = BeautifulSoup(response.content).title.string
                print title
                if title != "Quiz %i" % i:
                    response.failure("Got wrong response")

        

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=1000
    max_wait=2000

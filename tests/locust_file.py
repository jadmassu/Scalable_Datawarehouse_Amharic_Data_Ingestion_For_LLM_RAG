from locust import HttpUser, TaskSet, task, between

class DataLoadTest(TaskSet):
    @task
    def send_data(self):
        self.client.post("/data", json={"id": 1, "value": "sample data"})

class WebsiteUser(HttpUser):
    tasks = [DataLoadTest]
    wait_time = between(1, 5)

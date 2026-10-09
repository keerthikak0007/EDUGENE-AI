from locust import HttpUser, task, between


class EduGenieUser(HttpUser):
    host = "http://127.0.0.1:8000"
    wait_time = between(1, 3)

    @task
    def ask_question(self):
        self.client.get("/qa", params={"question": "What is Java?"})
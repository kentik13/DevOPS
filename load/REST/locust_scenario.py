from config import *
from locust import HttpUser, TaskSet, task, constant
import logging
import rest_gui_api

USER_CREDENTIALS = [(f"operator_{x}@visonic.ua", f"Operator{x}!") for x in [i for i in range(0, client_number)]]


class GUIRestApiLoad(TaskSet):
    def __init__(self, parent):
        super(GUIRestApiLoad, self).__init__(parent)
        self.PASS: str = ''
        self.LOGIN: str = ''
        self.LOGIN, self.PASS = USER_CREDENTIALS.pop()

        USER_CREDENTIAL = {
            'login': self.LOGIN,
            'password': self.PASS,
        }

        APP_DATA = {"user_rest_ver": USER_REST_VERSION,
                    "installer_rest_ver": INSTALLER_REST_VERSION,
                    }

        self.api = rest_gui_api.GUIApi(self.client, SERVER_HOST, APP_DATA, USER_CREDENTIAL)

    @task(25)
    def events(self):
        self.api.events()

    @task(20)
    def processes(self):
        self.api.processes()

    @task(5)
    def panel_vod(self):
        self.api.panel_vod()

    @task(50)
    def panels(self):
        self.api.panels()


    def on_start(self):
        if self.api.auth():
            pass
        else:
            logging.error("FATAL ERROR!!!\nFAIL ON START! NO NEED TO CONTINUE.\n ABORTING!!!")
            exit(-1)


class GUIRestLoad(HttpUser):
    tasks = [GUIRestApiLoad]
    HttpUser.wait_time = constant(task_period)
    insecure = True

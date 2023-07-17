from config import *
import logging
import time
import random

class GUIApi:
    def __init__(self, client, host, app_data, user_data):
        self.client = client
        self.host: str = host
        self.user_email: str = user_data['login']
        self.password: str = user_data['password']
        self.gui_api_url: str = f"https://{self.host}"
        self.rest_installer_url: str = f"https://{self.host}/rest_api/installer/{app_data['installer_rest_ver']}"
        self.rest_user_url: str = f"https://{self.host}/rest_api/{app_data['user_rest_ver']}"
        self.session_token: str = ""
        self.user_token: str = ""

    def request_post_api(self, api, rest, url_headers=None, json_data=None, expected_result=200, name_alias=None,
                         ssl_validate=True):
        if rest == 'installer':
            url = f"{self.rest_installer_url}{api}"
        elif rest == 'user':
            url = f"{self.rest_user_url}{api}"
        else:
            url = f"{self.gui_api_url}{api}"
        if name_alias is None:
            name_alias = api
        if url_headers is None:
            url_headers = {"Content-Type": "application/json"}
        if json_data is None:
            json_data = {}
        try:
            response = self.client.post(url, json=json_data, headers=url_headers, name=name_alias, verify=ssl_validate)
            if response.status_code != expected_result:
                logging.error(f"Requested data by GUI Operator '{self.user_email}':\n"
                              f"URL: {url}\n HEADER: {url_headers}\n JSON: {json_data}")
                logging.error(f"Response data for GUI Operator '{self.user_email}':\n Expect '{expected_result}', "
                              f"but got '{response.status_code}' with response data:\n {response.text}")
            else:
                logging.debug(f"Requested data by GUI Operator '{self.user_email}'\n"
                              f"URL: {url}\n HEADER: {url_headers}\n JSON: {json_data}")
                logging.debug(f"Response data for GUI Operator '{self.user_email}':\n {response.text}")
            return response
        except Exception as Err:
            logging.error(f"Requested data by GUI Operator '{self.user_email}':\n"
                          f"URL: {url}\n HEADER: {url_headers}\n JSON: {json_data}")
            logging.error(f"Exception data for GUI Operator '{self.user_email}': {Err}")
            return False

    def request_get_api(self, api, rest, url_headers=None, expected_result=200, name_alias=None,
                        ssl_validate=True):
        if rest == 'installer':
            url = f"{self.rest_installer_url}{api}"
        elif rest == 'user':
            url = f"{self.rest_user_url}{api}"
        else:
            url = f"{self.gui_api_url}{api}"
        if name_alias is None:
            name_alias = api
        if url_headers is None:
            url_headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            response = self.client.get(url, headers=url_headers, name=name_alias, verify=ssl_validate)
            if response.status_code != expected_result:
                logging.error(f"Requested data by GUI Operator '{self.user_email}'\n"
                              f"URL: {url}\n HEADER: {url_headers}")
                logging.error(f"Response data for GUI Operator '{self.user_email}':\n Expect '{expected_result}', "
                              f"but got '{response.status_code}' with response data:\n {response.text}")
                # Try Re-auth
                for c in range(0, 3):
                    if self.auth():
                        break
                    else:
                        time.sleep(60 * (c + 1))
            else:
                logging.debug(f"Requested data by GUI Operator '{self.user_email}' \n"
                              f"URL: {url}\n HEADER: {url_headers}")
                logging.debug(f"Response data for GUI Operator '{self.user_email}':\n {response.text}")
            return response
        except Exception as Err:
            logging.error(f"Requested data by GUI Operator '{self.user_email}'\n"
                          f"URL: {url}\n HEADER: {url_headers}")
            logging.error(f"Exception data for GUI Operator '{self.user_email}': {Err}")
            return False

    # API DEFINITION AREA
    def auth(self):
        logging.debug(f"Make AUTH by GUI email: {self.user_email}")
        return self.request_post_api(api="/api/login/sign", rest="GUI",
                                     url_headers={"Content-Type": "application/json"},
                                     json_data={"usr_email": str(self.user_email),
                                                "usr_password": str(self.password)
                                                },
                                     expected_result=200)

    def getallevents(self, units=None):
        if units is not None:
            self.request_get_api(api=f"/api/event/getallevents?count={units}&filter=&start=0",
                                 rest="GUI",
                                 url_headers={"Content-Type": "application/json"},
                                 name_alias=f"/api/event/getallevents?count={units}",
                                 expected_result=200)  # Main request
        else:
            self.request_get_api(api="/api/event/getallevents?count=1&filter=&start=0",
                                 rest="GUI",
                                 url_headers={"Content-Type": "application/json"},
                                 name_alias="/api/event/getallevents?count=1",
                                 expected_result=200)  # for updates

    def mine(self):
        self.request_get_api(api="/api/batch/mine",
                             rest="GUI",
                             url_headers={"Content-Type": "application/json"},
                             expected_result=200)

    def panels_page(self):
        self.request_get_api(api="/panels",
                             rest="GUI",
                             url_headers={"Content-Type": "application/json"},
                             expected_result=200)

    def servers_page(self):
        self.request_get_api(api="/api/settings/servers",
                             rest="GUI",
                             url_headers={"Content-Type": "application/json"},
                             expected_result=200)

    def getallunits(self, units):
        self.request_get_api(api=f"/api/units_all/getallunits?count={units}&filter=&query&start=0",
                             rest="GUI",
                             url_headers={"Content-Type": "application/json"},
                             name_alias=f"/api/units_all/getallunits?count={units}",
                             expected_result=200)

    def events_page(self):
        self.request_get_api(api="/events",
                             rest="GUI",
                             url_headers={"Content-Type": "application/json"},
                             expected_result=200)

    def getallprocesses(self, units):
        self.request_get_api(api=f"/api/process/getallprocesses?count={units}&filter=&query&sort&start=0",
                             rest="GUI",
                             url_headers={"Content-Type": "application/json"},
                             name_alias=f"/api/process/getallprocesses?count={units}",
                             expected_result=200)


    def process_page(self):
        self.request_get_api(api="/system/processes",
                             rest="GUI",
                             url_headers={"Content-Type": "application/json"},
                             expected_result=200)

    def myjobs_page(self, units):
        self.request_get_api(api=f"/api/batch/list?count={units}&filter=&query=&start=0",
                             rest="GUI",
                             url_headers={"Content-Type": "application/json"},
                             name_alias=f"/api/batch/list?count={units}",
                             expected_result=200)

    def one_panel(self,r_id):
        self.request_get_api(api=f"/panel/{r_id}",
                             rest="GUI",
                             url_headers={"Content-Type": "application/json"},
                             name_alias="/panel/random_id",
                             expected_result=200)

    # def unit_general(self,r_id):
    #     self.request_get_api(api=f"/api/unit_general/isonline?unt_id={r_id}",
    #                          rest="GUI",
    #                          url_headers={"Content-Type": "application/json"},
    #                          name_alias="/api/unit_general/isonline?unt_id=random_id",
    #                          expected_result=200)
    #
    # def unit_remarks(self,r_id):
    #     self.request_get_api(api=f"/api/unit_remarks/getall?unt_id={r_id}",
    #                          rest="GUI",
    #                          url_headers={"Content-Type": "application/json"},
    #                          name_alias="/api/unit_remarks/getall?unt_id=random_id",
    #                          expected_result=200)

    def post_vod(self,r_id):
        self.request_post_api(api=f"/api/unit_diagnostic/requestvideo?unt_id={r_id}&utz_id=1",
                              rest="GUI",
                              url_headers={"Content-Type": "application/json"},
                              name_alias="/api/unit_diagnostic/requestvideo",
                              expected_result=200)

    # TASK AREA
    def events(self):
        poll_time = 180
        logging.debug(f"CLIENT {self.user_email} select 'Events' page for {poll_time} seconds")
        self.events_page()

        while poll_time > 0:
            self.mine()
            time.sleep(1)

            self.getallevents(units_on_page)    # Main request
            self.getallevents()                 # for updates
            time.sleep(4)

            self.mine()
            time.sleep(2)

            self.getallevents(units_on_page)    # Main request
            self.getallevents()                 # for updates
            time.sleep(3)

            self.mine()
            time.sleep(3)

            self.getallevents(units_on_page)    # Main request
            self.getallevents()                 # for updates
            time.sleep(2)

            self.mine()
            time.sleep(4)

            self.getallevents(units_on_page)    # Main request
            self.getallevents()                 # for updates
            time.sleep(1)

            self.mine()
            time.sleep(5)

            self.getallevents(units_on_page)    # Main request
            self.getallevents()                 # for updates
            time.sleep(0)

            logging.debug(f"CLIENT {self.user_email}, GET: batch/mine")
            self.mine()
            time.sleep(5)

            poll_time -= 30

        self.stop(f"CLIENT {self.user_email} Go away or refresh 'Events' page")

    def panels(self):
        poll_time = 180
        logging.debug(f"CLIENT {self.user_email} select 'Panels' page for {poll_time} seconds")
        self.panels_page()
        self.servers_page()

        while poll_time > 0:
            self.mine()
            time.sleep(1)

            self.getallunits(units_on_page)
            time.sleep(4)

            self.mine()
            time.sleep(2)

            self.getallunits(units_on_page)
            time.sleep(3)

            self.mine()
            time.sleep(3)

            self.getallunits(units_on_page)
            time.sleep(2)

            self.mine()
            time.sleep(4)

            self.getallunits(units_on_page)
            time.sleep(1)

            self.mine()
            time.sleep(5)

            self.getallunits(units_on_page)
            time.sleep(0)

            self.mine()
            time.sleep(5)

            poll_time -= 30
        self.stop(f"CLIENT {self.user_email} Go away or refresh 'Panels' page")

    def processes(self):
        poll_time = 180
        logging.debug(f"CLIENT {self.user_email} select 'Processes' page for {poll_time} seconds")
        self.myjobs_page(units_on_page)
        self.process_page()

        while poll_time > 0:
            self.mine()
            time.sleep(3)

            self.getallprocesses(units_on_page)
            time.sleep(1)

            self.mine()
            time.sleep(3)

            self.getallprocesses(units_on_page)
            time.sleep(1)

            self.mine()
            time.sleep(3)

            self.getallprocesses(units_on_page)
            time.sleep(1)

            self.mine()
            time.sleep(3)

            self.getallprocesses(units_on_page)
            time.sleep(1)

            self.mine()
            time.sleep(3)

            self.getallprocesses(units_on_page)
            time.sleep(1)

            self.mine()
            time.sleep(3)

            poll_time -= 30
        self.stop(f"CLIENT {self.user_email} Go away or refresh 'Processes' page")

    def panel_vod(self):
        poll_time = 180
        r_id: str = str(random.randint(1, 1000))
        logging.debug(f"CLIENT {self.user_email} select 'Panel' page for {poll_time} seconds to VOD")

        while poll_time > 0:
            self.mine()
            time.sleep(3)

            self.one_panel(r_id)
            time.sleep(1)

            self.mine()
            time.sleep(3)

            # self.unit_general(r_id)
            # time.sleep(1)

            self.mine()
            time.sleep(3)

            # self.unit_remarks(r_id)
            # time.sleep(1)

            self.mine()
            time.sleep(3)

            poll_time -= 30
        self.post_vod(r_id)
        self.stop(f"CLIENT {self.user_email} Go away or refresh 'Panels' page")



    def stop(self, message):
        logging.debug(message)

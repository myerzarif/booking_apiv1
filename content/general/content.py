from common.requests import requests


class Content():

    def daily_update(self):
        print("daily_update")
        return "daily_update"

    def initial_update(self):
        response = requests.send_request(url=self.get_full_url(),
                                         method=self.config.method,
                                         params=self.config.params,
                                         data=self.config.data,
                                         json=self.config.json,
                                         headers=self.config.headers
                                         )

        print("response json: ", response.json())

    def get_full_url(self):
        return self.config.base_url + self.config.endpoint
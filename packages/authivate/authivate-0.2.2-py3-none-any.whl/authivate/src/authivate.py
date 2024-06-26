from pprint import pprint

import requests

from authivate.src.utils.authivate_config import AuthivateConfig
from authivate.src.utils.authivate_response import AuthivateResponse


class Authivate:
    def __init__(self, config: AuthivateConfig):
        self.config = config
        self._headers = {"Authorization": f"Bearer {config.api_key}"}
        self.client = requests.Session()

    def post_request(self, uri, body):
        try:
            response = self.client.post(uri, headers=self._headers, json=body)
            response.raise_for_status()
            return AuthivateResponse(response.status_code, response.json())
        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            json_data = (
                err.response.json()
                if "application/json" in err.response.headers.get("content-type", "")
                else None
            )
            return AuthivateResponse(status_code, json_data)
        except Exception as e:
            return AuthivateResponse(500, {"error": str(e)})

    def add_user_to_waitlist(self, **kwargs):
        url = f"api/v1/p/project/{self.config.project_id}/user_records/"
        body = {
            **kwargs,
        }
        uri = f"https://{self.config.host}/{url}"
        response = self.post_request(uri, body)
        return response

    def get_all_users(self, **kwargs):
        url = f"api/v1/p/project/{self.config.project_id}/user_records/"
        uri = f"https://{self.config.host}/{url}"
        response = self.client.get(uri, headers=self._headers, params=kwargs)
        return response.json()


# Example Usage
if __name__ == "__main__":

    # Initialize AuthivateConfig
    authivate_config = AuthivateConfig(
        api_key="edf8b00933fe400cec310c2d0ef491270e6e71b9", project_id="authivate"
    )

    # Create an instance of Authivate
    authivate_instance = Authivate(config=authivate_config)

    # Add user to waitlist
    """Response
    {'message': 'Yah!, you are now on the waitlist for {project name}. Please confirm your email to seal your spot'}
    """

    authivate_instance.add_user_to_waitlist(authivate_instance)

    # Get all users
    pprint(authivate_instance.get_all_users())

    """
    Response
    {'user_records': [
        {'country_code': 'NG',
                   'country_name': 'Nigeria',
                   'date_created': '2023-12-23T04: 47: 30.776501Z',
                   'fields': {
                       'email': 'email@mail.com',
                       'first_name': 'John',
                       'last_name': 'Doe'
                       },
                   'is_verified': False,
                   'status_in_project': 'WAITLISTED',
                   'user_unique_id': 'edg0aoyleai.0iael0ya'
        },
        {'country_code': 'NG',
                   'country_name': 'Nigeria',
                   'date_created': '2023-12-23T04: 54: 38.697351Z',
                   'fields':  {
                       'email': 'email2@mail.com',
                       'first_name': 'Peter',
                       'last_name': 'Akande'
                       },
                   'is_verified': False,
                   'status_in_project': 'WAITLISTED',
                   'user_unique_id': 'decwc.oyeyayaiioadeb'
        }
    ]
    }
    """

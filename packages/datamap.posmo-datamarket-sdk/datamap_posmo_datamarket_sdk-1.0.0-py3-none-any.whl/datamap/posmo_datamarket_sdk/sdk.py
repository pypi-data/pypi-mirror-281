import os
import requests
import webbrowser


class PosmoDataMarket:
    """Posmo DataMarket client

    Posmo DataMarket client can be used to execute queries in Posmo project database.
    """

    _login_url = 'https://id.datamap.io/api/user/login'
    _datamarket_url = 'https://gateway.datamap.io'

    def __init__(self, project_code: str, username: str = None, password: str = None) -> None:
        """Initializes the Posmo DataMarket client.

        Args:
            project_code: Posmo project code.
            username: Posmo account username.
            password: Posmo account password.
        """

        self.project_code = project_code
        self._username = username or os.environ.get('POSMO_USERNAME')
        self._password = password or os.environ.get('POSMO_PASSWORD')
        self._token = None

        if not project_code:
            raise ValueError('project_code argument cannot be empty.')
        if not self._username or not self._password:
            raise ValueError('Username and password must be provided in constructor or '
                             'POSMO_USERNAME and POSMO_PASSWORD environment variables.')

    def _login(self) -> None:
        response = requests.post(
            self._login_url,
            json={
                'login_input': self._username,
                'password': self._password,
            },
        )

        if (response.status_code == 200
            and (data := response.json().get('data'))
                and (jwt := data.get('jwt'))):
            self._token = jwt
        else:
            raise Exception('Posmo DataMarket login failed. '
                            'Please verify your credentials.')

    def _request(self, method: str, url: str, params: dict = None, body: dict = None) -> requests.Response:
        if not self._token:
            # Login if not yet logged in
            self._login()

        response = requests.request(
            method=method,
            url=url,
            headers={
                'Authorization': self._token,
            },
            params=params,
            json=body,
        )

        if response.status_code == 401:
            raise Exception('Posmo DataMarket request failed. Please '
                            'verify that you have sufficient permissions.')

        return response

    def query(self, query: str) -> dict:
        """Executes query in Posmo project database and returns the result dictionary.

        Args:
            query: SQL query to be executed in Posmo project database.
        """

        response = self._request(
            method='post',
            url=f'{self._datamarket_url}/api/query',
            body={
                'projectCode': self.project_code,
                'query': query,
            },
        )
        return response.json()

    def schema(self) -> None:
        """Opens DataMarket database schema in browser."""

        response = self._request(
            method='get',
            url=f'{self._datamarket_url}/api/meta',
            params={
                'projectCode': self.project_code,
            },
        )

        webbrowser.open_new_tab(response.json()['docs'])

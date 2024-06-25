from contextlib import contextmanager
import requests


class Orchest:
    def __init__(self, base_url: str, username: str, password: str):
        self.BASE_URL = base_url
        self.USERNAME = username
        self.PASSWORD = password

    @contextmanager
    def authenticated_session(
        self,
        *args,
        **kwargs
    ):
        '''Gets an authenticated session by persisting the login cookie.'''
        session = requests.Session(*args, **kwargs)
        data = {
            'username': self.USERNAME,
            'password': self.PASSWORD,
        }
        response = session.post(
            f'{self.BASE_URL}/login', timeout=4, data=data, allow_redirects=True
        )

        if not response.ok:
            return

        try:
            yield session
        finally:
            session.close()

    def request(self, method: str, url: str, payload: dict = {}, params: dict = {}):
        with self.authenticated_session() as session:
            if method == 'GET':
                response = session.get(url, params=params)
            elif method == 'POST':
                response = session.post(url, json=payload, params=params)
            elif method == 'PUT':
                response = session.put(url, json=payload, params=params)
            elif method == 'DELETE':
                response = session.delete(url, params=params)

            if not response.ok:
                raise Exception(response.text)

            response_json = response.json()

            return response_json

    def get_projects(self):
        url = f'{self.BASE_URL}/async/projects'

        response = self.request(method='GET', url=url)

        return response
    
    def get_pipeline_runs(self, page: int = 1, page_size: int = 10000, statusses: list = []):
        url = f'{self.BASE_URL}/catch/api-proxy/api/jobs/pipeline_runs'

        params = {
            'page': page,
            'page_size': page_size,
        }

        if statusses:
            params['status__in'] = ','.join(statusses)

        response = self.request(method='GET', url=url, params=params)

        return response
    
    def cancel_pipeline_run(self, job_id: str, pipeline_run_id: str):
        url = f'{self.BASE_URL}/catch/api-proxy/api/jobs/{job_id}/{pipeline_run_id}'
        
        response = self.request(method='DELETE', url=url)

        return response
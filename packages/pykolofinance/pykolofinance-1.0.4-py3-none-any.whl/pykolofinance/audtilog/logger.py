import json
import time

from django.conf import settings
from django.urls import resolve
from django.utils import timezone

from .tasks import send_logs_to_elk
from .contrib import get_headers, get_client_ip, mask_sensitive_data, decode_jwt_token


class APILoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Initialize settings from Django settings or use defaults
        self.API_LOGGER_PATH_TYPE = getattr(settings, 'API_LOGGER_PATH_TYPE', 'ABSOLUTE')
        if self.API_LOGGER_PATH_TYPE not in ['ABSOLUTE', 'RAW_URI', 'FULL_PATH']:
            self.API_LOGGER_PATH_TYPE = 'ABSOLUTE'

        self.API_LOGGER_SKIP_URL_NAME = getattr(settings, 'API_LOGGER_SKIP_URL_NAME', [''])
        if not isinstance(self.API_LOGGER_SKIP_URL_NAME, (tuple, list)):
            self.API_LOGGER_SKIP_URL_NAME = ['']

        self.API_LOGGER_SKIP_NAMESPACE = getattr(settings, 'API_LOGGER_SKIP_NAMESPACE', [])
        if not isinstance(self.API_LOGGER_SKIP_NAMESPACE, (tuple, list)):
            self.API_LOGGER_SKIP_NAMESPACE = []

        self.API_LOGGER_CONTENT_TYPES = [
            "application/json",
            "application/vnd.api+json",
            "application/gzip",
            "application/octet-stream",
        ]

    def __call__(self, request):
        if hasattr(settings, 'ELK_LOGGER_URL'):
            # Resolve URL name and namespace
            url_name = resolve(request.path_info).url_name
            namespace = resolve(request.path_info).namespace

            # Always skip logging for requests in 'admin' namespace
            if namespace == 'admin':
                return self.get_response(request)

            # Skip logging based on configured URL names
            if url_name in self.API_LOGGER_SKIP_URL_NAME:
                return self.get_response(request)

            # Skip logging based on configured namespaces
            if namespace in self.API_LOGGER_SKIP_NAMESPACE:
                return self.get_response(request)

            # Measure request execution time
            start_time = time.time()

            # Fetch request headers and method
            headers = get_headers(request=request)
            method = request.method

            # Parse request body as JSON if present
            request_data = json.loads(request.body) if request.body else ''

            email, user_id = decode_jwt_token(request)

            response = self.get_response(request)

            # Define content types to log
            self.API_LOGGER_CONTENT_TYPES = [
                "application/json",
                "application/vnd.api+json",
                "application/gzip",
                "application/octet-stream",
            ]

            # Determine response body based on content type
            if response.get("content-type") in self.API_LOGGER_CONTENT_TYPES:
                if response.get('content-type') == 'application/gzip':
                    response_body = '** GZIP Archive **'
                elif response.get('content-type') == 'application/octet-stream':
                    response_body = '** Binary File **'
                elif getattr(response, 'streaming', False):
                    response_body = '** Streaming **'
                else:
                    if isinstance(response.content, bytes):
                        response_body = json.loads(response.content.decode())
                    else:
                        response_body = json.loads(response.content)

                # Determine API path based on configuration
                if self.API_LOGGER_PATH_TYPE == 'ABSOLUTE':
                    api = request.build_absolute_uri()
                elif self.API_LOGGER_PATH_TYPE == 'FULL_PATH':
                    api = request.get_full_path()
                elif self.API_LOGGER_PATH_TYPE == 'RAW_URI':
                    api = request.get_raw_uri()
                else:
                    api = request.build_absolute_uri()

                # Mask sensitive data in the logged data
                data = dict(
                    api=mask_sensitive_data(api, mask_api_parameters=True),
                    headers=mask_sensitive_data(headers),
                    body=mask_sensitive_data(request_data),
                    method=method,
                    client_ip_address=get_client_ip(request),
                    response=mask_sensitive_data(response_body),
                    status_code=response.status_code,
                    execution_time=time.time() - start_time,
                    added_on=timezone.now(),
                    email=email,
                    user_id=user_id,
                    environment=settings.ENVIRONMENT_INSTANCE,

                )

                # Convert certain fields to JSON for logging purposes
                d = data.copy()
                print(d)
                d['headers'] = json.dumps(d['headers'], indent=4, ensure_ascii=False) if d.get('headers') else ''
                if request_data:
                    d['body'] = json.dumps(d['body'], indent=4, ensure_ascii=False) if d.get('body') else ''
                d['response'] = json.dumps(d['response'], indent=4, ensure_ascii=False) if d.get('response') else ''
                send_logs_to_elk.delay(d)

        else:
            response = self.get_response(request)

        return response
    
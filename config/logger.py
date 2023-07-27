"""
Decorator for log every request in project
logger name : project.request.{viewname}
"""

from json.decoder import JSONDecodeError
from typing import Dict

from django.http.response import FileResponse
from django.db import connection

import logging
import time
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from pythonjsonlogger import jsonlogger
from .exceptions import StreamingHttpResponseException


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_request_data(request):
    logger = logging.getLogger(f'project.request.data')
    if request.method in ["POST", "PATCH", "PUT", "DELETE"]:
        if request.content_type == "multipart/form-data":
            return {**request.POST}
        request_data_body = request.body
        if request_data_body:
            if len(request_data_body) >= 40000:
                return {}
            try:
                json_request_data = json.loads(request_data_body)
                request_data = json_request_data
            except JSONDecodeError as e:
                request_data = request_data_body.decode()
                logger.error("Json Decode Request Data Have Error", extra={
                    'error': str(e),
                }, exc_info=True)
            except Exception as e:
                request_data = {}
                logger.error("Request Body Data Have Error", extra={
                    'error': str(e),
                }, exc_info=True)
        else:
            request_data = {}
    elif request.method == "GET":
        request_data = {**request.GET}
    else:
        request_data = {}
    return request_data


def filter_sensitive_data(data: Dict):
    sensitive_fields = ["password", "old_password", "confirm_password"]
    semi_sensitive_fields = ["key", "token"]

    if not isinstance(data, Dict):
        return data
        
    new_data = data.copy()
    for key, value in data.items():
        if key in sensitive_fields:
            new_data[key] = "**********"
        elif key in semi_sensitive_fields and type(value) == str:
            new_data[key] = value[0:min(len(value), 8)] + "****"

    return new_data


class LoggerMixin:
    def dispatch(self, request, *args, **kwargs):
        logger = logging.getLogger(f'project.request.{self.get_view_name()}')
        start_time = time.time()
        headers = {}
        for (header, value) in request.META.items():
            if header.startswith("HTTP"):
                headers[header] = value
            if header.startswith("HTTP_AUTHORIZATION") and type(value) == str:
                headers[header] = value[0:min(len(value), 30)] + "***"
        request_data = get_request_data(request)
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            end_time = time.time()
            extra = {
                "absolute_url": request.get_full_path(),
                "headers": headers,
                "content_type": request.content_type,
                "ip": get_client_ip(request),
                "duration": end_time-start_time,
                "start_time": start_time,
                "end_time": end_time,
                "query_count": 0,
                "status_code": 500,
                "method": request.method,
                "type": "customize_request_response_mixin",
                "error_string": str(e),
                "request_data": filter_sensitive_data(request_data),
            }

            logger.error("Error on Get Response", extra=extra, exc_info=True)
            return JsonResponse(data={"message": "Internal Server Error!"}, status=500)
        end_time = time.time()

        # Log query if time bigger than 500ms
        list_query = {}
        list_query = {'count': 0, "queries": []}
        for query in connection.queries:
            list_query["queries"].append(query)
        list_query['count'] = len(connection.queries) + 1

        try:
            if type(response) == FileResponse:
                raise StreamingHttpResponseException
            data_json = json.dumps(response.data, cls=DjangoJSONEncoder)
            data_length = len(data_json)
            if data_length <= 40000:
                response_data = response.data
            else:
                response_data = {}

        except StreamingHttpResponseException:
            extra = {
                "absolute_url": request.get_full_path(),
                "headers": headers,
                "content_type": request.content_type,
                "ip": get_client_ip(request),
                "duration": end_time-start_time,
                "start_time": start_time,
                "end_time": end_time,
                "method": request.method,
                "type": "customize_request_response_mixin",
                "request_data": filter_sensitive_data(request_data),
            }
            logger.info("REQUEST_RESPONSE_FILE", extra=extra)
            return response
        except Exception as e:
            data_length = -1
            logger.warning("Error on jsonify response data in logger mixin", extra={
                "error_string": str(e)
            }, exc_info=True)
            return response

        extra = {
            "absolute_url": request.get_full_path(),
            "headers": headers,
            "content_type": request.content_type,
            "ip": get_client_ip(request),
            "response_data": response_data,
            "duration": end_time-start_time,
            "start_time": start_time,
            "end_time": end_time,
            "query_count": 0,
            "status_code": response.status_code,
            "method": request.method,
            "data_length": data_length,
            "type": "customize_request_response_mixin",
            "request_data": filter_sensitive_data(request_data),
        }
        if list_query:
            extra['list_query'] = list_query
        logger.info(
            msg="REQUEST_RESPONSE",
            extra=extra
        )
        return response


class LoggerBadRequestMixin:
    def dispatch(self, request, *args, **kwargs):
        logger = logging.getLogger(f'project.request.{self.get_view_name()}')
        start_time = time.time()
        headers = {}
        for (header, value) in request.META.items():
            if header.startswith("HTTP"):
                headers[header] = value
            if header.startswith("HTTP_AUTHORIZATION") and type(value) == str:
                headers[header] = value[0:min(len(value), 30)] + "***"
        request_data = get_request_data(request)
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            end_time = time.time()
            extra = {
                "absolute_url": request.get_full_path(),
                "headers": headers,
                "content_type": request.content_type,
                "ip": get_client_ip(request),
                "duration": end_time-start_time,
                "start_time": start_time,
                "end_time": end_time,
                "query_count": 0,
                "status_code": 500,
                "method": request.method,
                "type": "customize_request_response_mixin",
                "error_string": str(e),
                "request_data": filter_sensitive_data(request_data),
            }

            logger.error("Error on Get Response", extra=extra, exc_info=True)
            return JsonResponse(data={"message": "Internal Server Error!"}, status=500)
        end_time = time.time()

        # Log query if time bigger than 500ms
        list_query = {}
        list_query = {'count': 0, "queries": []}
        for query in connection.queries:
            list_query["queries"].append(query)
        list_query['count'] = len(connection.queries) + 1

        try:
            if type(response) == FileResponse:
                raise StreamingHttpResponseException
            data_json = json.dumps(response.data, cls=DjangoJSONEncoder)
            data_length = len(data_json)
            if data_length <= 40000:
                response_data = response.data
            else:
                response_data = {}

        except StreamingHttpResponseException:
            extra = {
                "absolute_url": request.get_full_path(),
                "headers": headers,
                "content_type": request.content_type,
                "ip": get_client_ip(request),
                "duration": end_time-start_time,
                "start_time": start_time,
                "end_time": end_time,
                "method": request.method,
                "type": "customize_request_response_mixin",
                "request_data": filter_sensitive_data(request_data),
            }
            logger.info("REQUEST_RESPONSE_FILE", extra=extra)
            return response
        except Exception as e:
            data_length = -1
            logger.warning("Error on jsonify response data in logger mixin", extra={
                "error_string": str(e)
            }, exc_info=True)
            return response

        extra = {
            "absolute_url": request.get_full_path(),
            "headers": headers,
            "content_type": request.content_type,
            "ip": get_client_ip(request),
            "response_data": response_data,
            "duration": end_time-start_time,
            "start_time": start_time,
            "end_time": end_time,
            "query_count": 0,
            "status_code": response.status_code,
            "method": request.method,
            "data_length": data_length,
            "type": "customize_request_response_mixin",
            "request_data": filter_sensitive_data(request_data),
        }
        if list_query:
            extra['list_query'] = list_query
        if extra.get("status_code", 200) >= 300:
            logger.info(
                msg="REQUEST_RESPONSE",
                extra=extra
            )
        return response


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict)
        # Add Log level
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
        # Process
        if not log_record.get('process'):
            log_record['process'] = record.process
        # Thread
        if not log_record.get('thread'):
            log_record['thread'] = record.thread
        # name
        if not log_record.get('name'):
            log_record['name'] = record.name
        # Created At
        if not log_record.get('created'):
            log_record['created'] = record.created

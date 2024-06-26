import json
import traceback
from http import HTTPStatus
from typing import Any

from .mini_logger import MiniLogger as logger
import warnings

HEADERS_KEY = 'headers'
AUTHORIZATION_KEY = 'authorization'
AUTHORIZATION_PREFIX = 'Bearer '


# TODO Align those methods with typescript-sdk https://github.com/circles-zone/typescript-sdk-remote-typescript-package/blob/dev/typescript-sdk/src/utils/index.ts
# TODO Shall we create also createInternalServerErrorHttpResponse(), createOkHttpResponse() like we have in TypeScript?

# TODO: add handler wrapper?

def get_payload_dict_from_event(event: dict) -> dict:
    warnings.warn("DELETE get_payload_dict_from_event",DeprecationWarning,stacklevel=2)
    """Extracts params sent with payload"""
    return json.loads(event.get('body') or '{}')


def get_path_parameters_dict_from_event(event: dict) -> dict:
    warnings.warn("DELETE get_path_parameters_dict_from_event",DeprecationWarning,stacklevel=2)
    """Extracts params sent implicitly: `url/param?test=5` -> param
    (when the path is defined with /{param})"""
    return event.get('pathParameters') or {}


def get_query_string_parameters_from_event(event: dict) -> dict:
    warnings.warn("DELETE get_query_string_parameters_from_event",DeprecationWarning,stacklevel=2)
    """Extracts params sent explicitly: `url/test?a=1&b=2` ->  {'a': '1', 'b': '2'}"""
    return event.get("queryStringParameters") or {}  # params sent with ?a=1&b=2


def create_authorization_http_headers(user_jwt: str) -> dict:
    warnings.warn("DELETE create_authorization_http_headers",DeprecationWarning,stacklevel=2)
    logger.start(object={"user_jwt": user_jwt})
    #TODO check the validity of user_jwt and it is not None and raise exception, please do the same in all other functions.
    authorization_http_headers = {
        'Content-Type': 'application/json',
        'Authorization': AUTHORIZATION_PREFIX + user_jwt,
    }
    logger.end(object={"authorization_http_headers": authorization_http_headers})
    return authorization_http_headers


def get_user_jwt_from_event(event: dict) -> str:
    warnings.warn("DELETE get_user_jwt_from_event",DeprecationWarning,stacklevel=2)
    logger.start(object={"event": event})
    auth_header = event.get(HEADERS_KEY, {}).get(AUTHORIZATION_KEY)
    if auth_header is None:
        auth_header = event.get(HEADERS_KEY, {}).get(AUTHORIZATION_KEY.capitalize())
    user_jwt = auth_header.split(AUTHORIZATION_PREFIX)[1]
    logger.end(object={"user_jwt": user_jwt})
    return user_jwt


def create_return_http_headers() -> dict:
    warnings.warn("DELETE create_return_http_headers",DeprecationWarning,stacklevel=2)
    logger.start()
    # Adding "Access-Control-Allow-Origin" : "*" to take care of CORS from localhost
    # TODO Do we need to add those? In which cases? try  adding crossDomain: true, to the request, 'Access-Control-Allow-Credentials': true to header
    return_http_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
    }
    logger.end(object={"return_http_headers": return_http_headers})
    return return_http_headers


def create_error_http_response(exception: Exception, status_code: HTTPStatus = HTTPStatus.BAD_REQUEST) -> dict:
    warnings.warn("DELETE create_error_http_response",DeprecationWarning,stacklevel=2)
    logger.start(object={"exception": exception})
    error_http_response = {
        "statusCode": status_code.value,
        "headers": create_return_http_headers(),
        "body": create_http_body({"error": str(exception)}),
        "traceback": traceback.format_exc()
    }
    logger.end(object={"error_http_response": error_http_response})
    return error_http_response


def create_ok_http_response(body: Any) -> dict:
    warnings.warn("DELETE create_ok_http_response",DeprecationWarning,stacklevel=2)
    logger.start(object={"body": body})
    ok_http_response = {
        "statusCode": HTTPStatus.OK.value,
        "headers": create_return_http_headers(),
        "body": create_http_body(body)
    }
    logger.end(object={"ok_http_response": ok_http_response})
    return ok_http_response


# https://google.github.io/styleguide/jsoncstyleguide.xml?showone=Property_Name_Format#Property_Name_Format
def create_http_body(body: Any) -> str:
    warnings.warn("DELETE create_http_body",DeprecationWarning,stacklevel=2)
    # TODO console.warning() if the body is not a valid camelCase JSON
    # https://stackoverflow.com/questions/17156078/converting-identifier-naming-between-camelcase-and-underscores-during-json-seria
    logger.start(object={"body": body})
    http_body = json.dumps(body)
    logger.end(object={"http_body": http_body})
    return http_body

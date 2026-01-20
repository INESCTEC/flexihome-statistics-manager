import requests, json

from statistics_manager_service import generalLogger, Config


def request_with_exception(url, error_msg, headers={}, query_parameters={}):
    response = requests.get(
        url, headers=headers, params=query_parameters, timeout=Config.REQUEST_TIMEOUT_SECONDS
    )

    # TODO: Can add a try catch to the "requests" method. Log connection problems, timeouts, etc.

    if 400 <= response.status_code < 600:
        generalLogger.error(f"Request failed with status code: {response.status_code}")
        generalLogger.error(error_msg)
        generalLogger.error(json.dumps(json.loads(response.content)))

        raise requests.exceptions.HTTPError(error_msg)
    
    return response


def decode_request_response(http_response, error_msg):
    try:
        decoded_response = json.loads(http_response.content)

    except json.decoder.JSONDecodeError as e:
        generalLogger.debug(http_response.text)
        generalLogger.error(repr(e))

        raise json.decoder.JSONDecodeError(error_msg)

    except Exception as e:
        generalLogger.debug(json.loads(http_response.content))
        generalLogger.error(repr(e))

        raise Exception("General exception. See stack trace.")
    
    return decoded_response
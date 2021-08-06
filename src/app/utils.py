import json


def generate_response(status_code, status, message, results):
    """
    Generates response for lambda return value in order to give details of the processing.

    Params:
        status_code(int): code designating the success or fail operation of the process
        status(int): code designating the success or fail operation of the process, may be more specific than statusCode
        message(str): Any relevant message regarding processing, such as specific error message or number of objects
         processed
        results(any): the object processed, such as the event lambda input or organised list of results

    Returns:
        response(dict): response of lambda giving status code based on processing and message with the details, as well
         as body with the processed object or results list.
    """
    response = {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(
            {"status": status, "message": message, "body": results})
    }
    return response
import logging

from src.app.utils import generate_response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    Lambda which receives customer housing details related to heating, and then calculates the expected heat loss for
    the property as well as the recommended heat pump and related details including cost.

    Params:
        event(list): provided list of json values for various customer houses with required parameters for heat
         calculations.
        context(Context): The AWS context object in which the function is called.

    Returns:
        response(dict): response of lambda giving status code based on processing and message with the details

    Examples:
        Example event Param:
            .. code-block:: json

                [
                    {
                        "submissionId": "4cb3820a-7bf6-47f9-8afc-3adcac8752cd",
                        "designRegion": "Severn Valley (Filton)",
                        "floorArea": 125,
                        "age": "1967 - 1975",
                        "heatingFactor": 101,
                        "insulationFactor": 1.3
                    },
                    {
                        "submissionId": "e21a3149-b88c-40e9-86fd-c94a6b93cb78",
                        "designRegion": "W Pennines (Ringway)",
                        "floorArea": 92,
                        "age": "1991 - 1995",
                        "heatingFactor": 88,
                        "insulationFactor": 1.1
                    }
                ]

        Example response Returned:
            .. code-block:: json
            
                {
                    "statusCode": 200,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": "{'status': 200, 'message': 'Successfully processed 6 customer house heat details', 
                    'body':
                        [
                            {
                                "submissionId": "4cb3820a-7bf6-47f9-8afc-3adcac8752cd",
                                "designRegion": "Severn Valley (Filton)",
                                "floorArea": 125,
                                "age": "1967 - 1975",
                                "heatingFactor": 101,
                                "insulationFactor": 1.3
                            },
                            {
                                "submissionId": "e21a3149-b88c-40e9-86fd-c94a6b93cb78",
                                "designRegion": "W Pennines (Ringway)",
                                "floorArea": 92,
                                "age": "1991 - 1995",
                                "heatingFactor": 88,
                                "insulationFactor": 1.1
                            }
                        ]
                    }"
                }
    """
    logger.info(f"input event: {event}")

    try:
        if event is None:
            raise Exception("No Event object found, required to provide house details")
        if type(event) is not list:
            raise Exception("Provided event object not a list, required to provide house details")

        records = event
        # TODO - Process records in methods outside this file
        success_records = []
        processed_message = f"Successfully processed {len(success_records)} house heat details"
        logger.info(processed_message)
        response = generate_response(200, 200, processed_message, event)
        return response

    except Exception as exception:
        logger.error("Application failed due to the following error")
        logger.error(exception)
        raise


if __name__ == '__main__':
    event_example = [
        {
            "submissionId": "4cb3820a-7bf6-47f9-8afc-3adcac8752cd",
            "designRegion": "Severn Valley (Filton)",
            "floorArea": 125,
            "age": "1967 - 1975",
            "heatingFactor": 101,
            "insulationFactor": 1.3
        },
        {
            "submissionId": "e21a3149-b88c-40e9-86fd-c94a6b93cb78",
            "designRegion": "W Pennines (Ringway)",
            "floorArea": 92,
            "age": "1991 - 1995",
            "heatingFactor": 88,
            "insulationFactor": 1.1
        },
        {
            "submissionId": "2191bf41-ce1e-427d-85c3-88d5a44680ae",
            "designRegion": "North-Eastern (Leeming)",
            "floorArea": 126,
            "age": "pre 1900",
            "heatingFactor": 131,
            "insulationFactor": 1.8
        },
        {
            "submissionId": "3d8f19b0-3886-452d-a335-f3a2e7d9f5a5",
            "designRegion": "Thames Valley (Heathrow)",
            "floorArea": 109,
            "age": "1930 - 1949",
            "heatingFactor": 90,
            "insulationFactor": 1.2
        },
        {
            "submissionId": "b0ec94b6-ca15-4fb2-9ec7-7017f43080f4",
            "designRegion": "W Scotland (Abbotsinch)",
            "floorArea": 163,
            "age": "1900 - 1929",
            "heatingFactor": 111,
            "insulationFactor": 1.7
        }
    ]
    lambda_handler(event_example, None)

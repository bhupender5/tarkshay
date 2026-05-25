import json
import logging
from typing import Dict

import httpx


# ---------------------------------------------------
# Logging Configuration
# ---------------------------------------------------

logging.basicConfig(
    filename="errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------------------------------
# Send Payload to Webhook
# ---------------------------------------------------

def send_to_webhook(
    payload: Dict,
    webhook_url: str,
    timeout: float = 10.0
):

    headers = {
        "Content-Type": "application/json"
    }

    try:

        response = httpx.post(
            webhook_url,
            content=json.dumps(payload),
            headers=headers,
            timeout=timeout
        )

        result = {
            "status": response.status_code,
            "body": response.text
        }

        print(
            f"Webhook sent successfully: {response.status_code}"
        )

        return result

    # ---------------------------------------------------
    # Timeout Handling
    # ---------------------------------------------------

    except httpx.TimeoutException as e:

        logging.error(
            f"Webhook timeout error: {str(e)}"
        )

        return {
            "error": "Webhook timeout",
            "details": str(e)
        }

    # ---------------------------------------------------
    # Request Error Handling
    # ---------------------------------------------------

    except httpx.RequestError as e:

        logging.error(
            f"Webhook request error: {str(e)}"
        )

        return {
            "error": "Webhook request failed",
            "details": str(e)
        }

    # ---------------------------------------------------
    # Generic Exception Handling
    # ---------------------------------------------------

    except Exception as e:

        logging.error(
            f"Unexpected webhook error: {str(e)}"
        )

        return {
            "error": "Unexpected webhook error",
            "details": str(e)
        }
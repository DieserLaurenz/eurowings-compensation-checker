import os
from dotenv import load_dotenv
import requests
import logging
from typing import Dict, Any

load_dotenv()

# Lese die Variablen aus der .env-Datei
FLIGHT_NUMBER = os.getenv('FLIGHT_NUMBER')
DEPARTURE_DATE = os.getenv('DEPARTURE_DATE')
AIRLINE_CODE = os.getenv('AIRLINE_CODE')
NAME = os.getenv('NAME')
SURNAME = os.getenv('SURNAME')
EMAIL = os.getenv('EMAIL')
BOOKING_CODE = os.getenv('BOOKING_CODE')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_and_validate_env():

    load_dotenv()
    env_vars = {}

    # Beispiel mit optionalen Variablen
    required_vars = [
        'FLIGHT_NUMBER',
        'DEPARTURE_DATE',
        'AIRLINE_CODE',
        'NAME',
        'SURNAME',
        'EMAIL',
        'BOOKING_CODE',
    ]

    # Erforderliche Variablen prüfen
    for var in required_vars:
        value = os.getenv(var)
        if value == "":
            raise ValueError(f"Environment variable '{var}' is not set in .env file.")
        env_vars[var] = value

    return env_vars

# Define Python user-defined exceptions
class NoEwCTFoundInRequestException(Exception):
    """Raised when there was no ew_ct cookie found in the request"""
    pass


def get_headers() -> Dict[str, str]:
    """Returns common headers for the requests."""
    return {
        'user-agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        ),
    }


def get_ew_ct_cookie(flight_number: str, departure_date: str, airline_code: str) -> str:
    """
    Sends a request to fetch the 'ew_ct' cookie.

    Args:
        flight_number (str): The flight number.
        departure_date (str): The departure date in YYYY-MM-DD format.
        airline_code (str): The airline code.

    Returns:
        str: The value of the 'ew_ct' cookie.

    Raises:
        NoEwCTFoundInRequestException: If the cookie is not found.
    """
    logging.info("Sending 'ew_ct' cookie request")
    headers = get_headers()

    json_data = {
        'flightNumber': flight_number,
        'departureDate': departure_date,
        'airlineCode': airline_code,
    }

    response = requests.post(
        'https://www.eurowings.com/at/4u/online-service-ausgleichsanspruch/_jcr_content/main/claimtool.submit.s2.html',
        headers=headers,
        json=json_data,
    )

    if 'ew_ct' in response.cookies:
        logging.info("'ew_ct' cookie successfully extracted")
        return response.cookies["ew_ct"]
    else:
        logging.error("Failed to extract 'ew_ct' cookie")
        raise NoEwCTFoundInRequestException("No 'ew_ct' cookie found in the response")


def get_decision_response(ew_ct: str, personal_data: Dict[str, Any]) -> str:
    """
    Sends a request to fetch the decision based on the 'ew_ct' cookie.

    Args:
        ew_ct (str): The 'ew_ct' cookie value.
        personal_data (Dict[str, Any]): Personal data required for the request.

    Returns:
        str: The decision message from the server.
    """
    logging.info("Sending request to fetch the decision")

    cookies = {'ew_ct': ew_ct}
    headers = get_headers()

    response = requests.post(
        'https://www.eurowings.com/at/4u/online-service-ausgleichsanspruch/_jcr_content/main/claimtool.submit.s3.html',
        cookies=cookies,
        headers=headers,
        json=personal_data,
    )

    if response.status_code == 200:
        try:
            response_json = response.json()
            return response_json.get("message", "No message in response")
        except ValueError:
            logging.error("Response is not valid JSON")
            raise ValueError("The response is not valid JSON")
    else:
        logging.error(f"Request failed with status code {response.status_code}")
        response.raise_for_status()


def main():
    try:
        env_vars = load_and_validate_env()
        logging.info("All environment variables loaded successfully!")
    except ValueError as e:
        logging.error(f"Error loading environment variables: {e}")
        return

    flight_data = {
        "flight_number": env_vars['FLIGHT_NUMBER'],
        "departure_date": env_vars['DEPARTURE_DATE'],
        "airline_code": env_vars['AIRLINE_CODE'],
    }

    personal_data = {
        'name': env_vars['NAME'],
        'surname': env_vars['SURNAME'],
        'email': env_vars['EMAIL'],
        'bookingCode': env_vars['BOOKING_CODE'],
        'personalDetailsCheckbox': 'checked',  # Standardwert
    }

    try:
        ew_ct = get_ew_ct_cookie(**flight_data)
        decision_message = get_decision_response(ew_ct, personal_data)
        logging.info(f"Decision message: {decision_message}")
    except NoEwCTFoundInRequestException as e:
        logging.error(f"Error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

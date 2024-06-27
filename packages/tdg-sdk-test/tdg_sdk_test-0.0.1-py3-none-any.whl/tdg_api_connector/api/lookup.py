import sys
import os
sys.path.insert(1, os.path.dirname(__file__))
from ..utilities.helpers import get_data

class LookupAPI:
    """
    LookupAPI is a library that interacts with the Phone Lookup API to fetch details related to 
    phone numbers and emails. To utilize this class, an API key is required for authentication.

    Attributes:
        - BASE_URL (str): The base URL for the Phone Lookup API.
        - headers (dict): Contains the API key in dictionary format.

    Methods:
        - get_details_by_contact_number(contact_number: int) -> dict:
            Retrieves details for a single contact number.

        - get_contact_number_details_in_bulk(contact_numbers_list: list) -> list:
            Retrieves details for multiple contact numbers in bulk.

        - get_details_by_email(email) -> dict:
            Retrieves details for a single email.

        - get_email_details_in_bulk(email_list) -> lis:
            Retrieves details for multiple emails.
    
    Example Usage:
        obj = LookupAPI('api_key')
        obj.get_details_by_contact_number(contact_number=5555555555)
    """

    def __init__(self, api_key: str) -> None:
        self.base_url = 'https://api.tdg1.io/v2/lookup/'
        self.headers = {
            "x-api-key": api_key
        }

    def get_phone(self, contact_number: int) -> dict:

        """
        A function that gets the details for a single contact number.
        
        Parameters:
            - contact_number: int, (REQUIRED)
                10-digit numeric phone number (without spaces, dashes, or parentheses).

        Returns:
            A dictionary containing the details of the contact number.

        Raises:
            ValueError: If contact_number is not a 10-digit number.
        """
        if len(str(contact_number)) != 10:
            len(str(contact_number))
            raise ValueError("Contact number must be a 10-digit numeric phone number.")


        return get_data(
            base_url=self.base_url,
            request_type='POST',
            endpoint='phone',
            payload={
                "phone": contact_number
            },
            headers=self.headers
        )
    

    def get_phone_details_in_bulk(self, contact_numbers_list: list) -> list:
        """
        A function that gets the details for multiple contact numbers in bulk.
        
        Parameters:
            - contact_numbers: list, (REQUIRED)
                List of 10-digit numeric phone numbers (without spaces, dashes, or parentheses).

        Returns:
            A list of dictionaries containing the details of the contact numbers.
        
        Raises:
            ValueError: If any contact number in the list is not a 10-digit number.
        """
        if len(contact_numbers_list) > 100:
            raise ValueError("Maximum range of allowed numbers are 100 .")

        for contact_number in contact_numbers_list:
            if len(str(contact_number)) != 10:
                raise ValueError(f"contact number: {contact_number} is not a 10 digit number, \
                All contact numbers in the list must be 10-digit numeric phone numbers.")

        output_data = [
                        get_data(
                            base_url=self.base_url,
                            headers=self.headers,
                            request_type='POST',
                            endpoint='phone',
                            payload={
                                "phone": contact
                            }
                        ) for contact in contact_numbers_list
                    ]

        return output_data

    def get_email(self, email: str) -> dict:
        """
        A function that gets the details by email.
        
        Parameters:
            - email: str, (REQUIRED)
                100 characters max.

        Returns:
            A dictionary containing the details of the email.

        Raises:
            ValueError: If email is not a 10-digit number.
        """

        if '@' not in email:
            raise ValueError("Invalid email address.")

        return get_data(
            base_url=self.base_url,
            request_type='POST',
            endpoint='email',
            payload={
                "Email": email
            },
            headers=self.headers
        )

    def get_email_details_in_bulk(self, email_list: list) -> list:
        """
        A function that gets the details for multiple contact numbers in bulk.
        
        Parameters:
            - contact_numbers: list, (REQUIRED)
                List of 10-digit numeric phone numbers (without spaces, dashes, or parentheses).

        Returns:
            A list of dictionaries containing the details of the contact numbers.
        
        Raises:
            ValueError: If any contact number in the list is not a 10-digit number.
        """
        if len(email_list) > 100:
            raise ValueError("Maximum range of allowed numebrs are 100 .")

        for email in email_list:
            if '@' not in email:
                raise ValueError(f"email: {email} is not a 10-digit number.")

        output_data = [
                        get_data(
                            base_url=self.base_url,
                            headers=self.headers,
                            request_type='POST',
                            endpoint='phone',
                            payload={
                                "phone": email
                            }
                        ) for email in email_list
                    ]

        return output_data

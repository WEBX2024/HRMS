"""
Custom exception handler for DRF.
Provides consistent error response format.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize the response data
        custom_response_data = {
            'success': False,
            'error': {
                'message': None,
                'details': None,
                'code': response.status_code
            }
        }
        
        # Handle different types of errors
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                custom_response_data['error']['message'] = response.data['detail']
            else:
                custom_response_data['error']['message'] = 'Validation error'
                custom_response_data['error']['details'] = response.data
        elif isinstance(response.data, list):
            custom_response_data['error']['message'] = 'Validation error'
            custom_response_data['error']['details'] = response.data
        else:
            custom_response_data['error']['message'] = str(response.data)
        
        response.data = custom_response_data
        
        # Log the error
        logger.error(
            f"API Error: {custom_response_data['error']['message']} | "
            f"Status: {response.status_code} | "
            f"Path: {context['request'].path}"
        )
    else:
        # Handle non-DRF exceptions
        logger.exception(f"Unhandled exception: {exc}")
        response = Response(
            {
                'success': False,
                'error': {
                    'message': 'An unexpected error occurred',
                    'details': str(exc) if context['request'].user.is_staff else None,
                    'code': status.HTTP_500_INTERNAL_SERVER_ERROR
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return response


def success_response(data=None, message=None, status_code=status.HTTP_200_OK):
    """
    Helper function to create consistent success responses.
    """
    response_data = {
        'success': True,
        'message': message,
        'data': data
    }
    return Response(response_data, status=status_code)

import logging
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import TransactionSerializer
from .cerbos_utils import check_permission

# Set up the logger for this module
logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_details(request):
    userid = request.headers.get('userid')
    logger.info(f"Received get_details request from user {userid}")

    if not check_permission(userid, 'get_details'):
        logger.warning(f"Permission denied for user {userid} to perform get_details")
        return Response(status=status.HTTP_403_FORBIDDEN)

    logger.info(f"Permission granted for user {userid} to perform get_details")
    return Response({"details": "Dummy details"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def save_details(request):
    userid = request.headers.get('userid')
    logger.info(f"Received save_details request from user {userid} with data: {request.data}")

    if not check_permission(userid, 'save_details'):
        logger.warning(f"Permission denied for user {userid} to perform save_details")
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        logger.info(f"Data from user {userid} is valid. Saving details.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    logger.error(f"Data from user {userid} is invalid: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

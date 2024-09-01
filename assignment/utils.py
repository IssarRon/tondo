import logging
from rest_framework.response import Response
from rest_framework import status
from .cerbos_utils import check_permission

logger = logging.getLogger(__name__)

def handle_transaction_request(request, serializer_class, action_name, userid):
    # Validate request data using the provided serializer
    serializer = serializer_class(data=request.data)
    
    if not serializer.is_valid():
        logger.error(f"Invalid data received: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    transaction_id = serializer.validated_data['transaction_id']
    
    # Log the request
    logger.info(f"Received {action_name} request from user {userid} for transaction {transaction_id}")

    # Check permissions
    if not check_permission(userid, action_name, transaction_id):
        logger.warning(f"Permission denied for user {userid} to perform {action_name} on transaction {transaction_id}")
        return Response(status=status.HTTP_403_FORBIDDEN)

    logger.info(f"Permission granted for user {userid} to perform {action_name} on transaction {transaction_id}")
    
    return Response(serializer.validated_data, status=status.HTTP_200_OK)

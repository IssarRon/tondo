import logging
from rest_framework.decorators import api_view
from .serializers import TransactionPostSerializer, TransactionGetSerializer
from .utils import handle_transaction_request

logger = logging.getLogger(__name__)

#create two endpoints for two separate actions
@api_view(['GET'])
def get_details(request):
    userid = request.headers.get('userid')
    return handle_transaction_request(request, TransactionGetSerializer, 'get_details', userid)

@api_view(['POST'])
def save_details(request):
    userid = request.headers.get('userid')
    return handle_transaction_request(request, TransactionPostSerializer, 'save_details', userid)

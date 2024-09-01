from rest_framework import serializers

class TransactionSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(max_length=255)
    amount = serializers.FloatField()
    # Add other fields as needed

from rest_framework import serializers

#serializers for different expected bodies
class TransactionPostSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField()
    amount = serializers.FloatField()

class TransactionGetSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField()

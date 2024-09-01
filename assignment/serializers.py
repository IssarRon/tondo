from rest_framework import serializers

class TransactionPostSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField()
    amount = serializers.FloatField()

class TransactionGetSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField()

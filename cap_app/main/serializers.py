from rest_framework import serializers
from .models import Query


class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = '__all__'  # Serialize all fields of the Query model

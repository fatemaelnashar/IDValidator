from rest_framework import serializers
from .models import NationalId, Visit

class NationalIdSerializer(serializers.Serializer):
   number = serializers.CharField(max_length=14, min_length=14)

class VisitSerializer(serializers.ModelSerializer):
   class Meta:
      model = Visit
      fields = '__all__'
from rest_framework.serializers import ModelSerializer
from .models import Breeds

class BreedsSerializer(ModelSerializer):
    class Meta:
        model = Breeds
        fields = ['breedsId', 'name']

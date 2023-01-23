from rest_framework import serializers
from ..models import CheckIn


class CheckInSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckIn
        fields = ['responses', 'user', 'created']
        read_only_fields = ['user', 'created']

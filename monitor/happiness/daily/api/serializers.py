from rest_framework import serializers
from ..models import CheckIn
from ...team.models import Team


class CheckInSerializer(serializers.ModelSerializer):
    # user = serializers.CurrentUserDefault()
    # responses = serializers.JSONField(default=list)

    class Meta:
        model = CheckIn
        fields = ['responses']

    # def create(self, validated_data):
    #     created = CheckIn.objects.create(responses=validated_data['responses'], user)
    #     return validated_data

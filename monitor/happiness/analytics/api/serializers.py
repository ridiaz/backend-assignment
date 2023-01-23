from rest_framework import serializers


class TeamStatsSerializer(serializers.Serializer):
    number_of_people = serializers.IntegerField()
    average_happiness = serializers.DecimalField(6, 2, required=False)
    level_happiness = serializers.CharField(max_length=200)


class TeamSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    average_happiness = serializers.DecimalField(6, 2, required=False)
    team_statistics = TeamStatsSerializer(required=False, many=True)

from django.db import models
from django.db.models import Count, Avg

from ..analytics.api.serializers import TeamStatsSerializer, TeamSerializer

LEVELS = ['Extremely happy',
          'Happy',
          'Slightly Happy',
          'Neutral',
          'Slightly Happy',
          'Unhappy',
          'Extremely unhappy']


class DimensionDate(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()


class DimensionTeam(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)


class DimensionHappinessLevel(models.Model):
    id = models.CharField(max_length=250, primary_key=True)
    level = models.CharField(max_length=150, unique=True)


class FactResponse(models.Model):
    score = models.IntegerField()
    dim_date = models.ForeignKey(DimensionDate, on_delete=models.DO_NOTHING)
    dim_team = models.ForeignKey(DimensionTeam, on_delete=models.DO_NOTHING)
    dim_happiness = models.ForeignKey(DimensionHappinessLevel, on_delete=models.DO_NOTHING)


def select_stats_from_authenticated_user(team_names=None, date_start=None, date_end=None):
    teams = []
    for team in team_names:
        qs = DimensionHappinessLevel.objects.filter(level__in=LEVELS,
                                                    factresponse__dim_date__year=2023,
                                                    factresponse__dim_team__id=team.id).annotate(
            number_of_people=Count('factresponse__id'),
            average_happiness=Avg('factresponse__score'))
        team = {
            'name': team.name
        }
        team_statistics = []
        for entry in qs:
            stat = {
                'number_of_people': entry.number_of_people,
                'average_happiness': entry.average_happiness,
                'level_happiness': entry.level
            }
            team_statistics.append(stat)
            team['team_statistics'] = team_statistics

            serializer = TeamSerializer(team)
            print(serializer.data)

        teams.append(team)

    for team in teams:
        qs = DimensionTeam.objects.filter(name=team['name'], factresponse__dim_date__year=2023).annotate(
            average_happiness=Avg('factresponse__score'))
        team['average_happiness'] = qs[0].average_happiness
    print(teams)
    return teams




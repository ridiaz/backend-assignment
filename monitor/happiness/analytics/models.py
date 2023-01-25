from django.db import models
from django.db.models import Count, Avg
from django.utils.timezone import now

from ..team.models import Team

LEVELS_OF_HAPPINESS = ['Extremely happy',
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



def get_statistics_anonymous(date_start=now(), date_end=now()):
    team_statistics_list = [{
        'name': 'all teams'
    }]
    for team_statistics_item in team_statistics_list:
        queryset = DimensionTeam.objects.filter(factresponse__dim_date__year=date_start.year).annotate(
            average_happiness=Avg('factresponse__score'))
        team_statistics_item['average_happiness'] = queryset[0].average_happiness

    return team_statistics_list


def get_statistics(user, date_start=now(), date_end=now()):
    teams = [team for team in Team.objects.filter(users__pk=user.id)]

    team_statistics_list = build_team_statistics_list(teams)

    for team_statistics_item in team_statistics_list:
        queryset = DimensionTeam.objects.filter(name=team_statistics_item['name'],
                                                factresponse__dim_date__year=date_start.year).annotate(
            average_happiness=Avg('factresponse__score'))
        team_statistics_item['average_happiness'] = queryset[0].average_happiness

    return team_statistics_list


def build_team_statistics_list(teams, date_start=now()):
    team_statistics_list = []
    for team in teams:
        queryset = DimensionHappinessLevel.objects.filter(level__in=LEVELS_OF_HAPPINESS,
                                                          factresponse__dim_date__year=date_start.year,
                                                          factresponse__dim_team__id=team.id).annotate(
            number_of_people=Count('factresponse__id'),
            average_happiness=Avg('factresponse__score'))
        team_statistics = []
        team_statistics_item = {
            'name': team.name
        }
        for entry in queryset:
            stat = {
                'number_of_people': entry.number_of_people,
                'average_happiness': entry.average_happiness,
                'level_happiness': entry.level
            }
            team_statistics.append(stat)
            team_statistics_item['team_statistics'] = team_statistics

        team_statistics_list.append(team_statistics_item)
    return team_statistics_list

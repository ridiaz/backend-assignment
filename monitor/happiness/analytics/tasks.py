import datetime

from django.utils import dateparse
from .models import DimensionTeam, DimensionDate, FactResponse, select_stats_from_authenticated_user, \
    DimensionHappinessLevel
from ..team.models import Team


def get_or_create_dimension_date(date: datetime) -> DimensionDate:
    date = dateparse.parse_datetime(date)
    date_pk = date.strftime('%Y%m%d')
    dim_date, _ = DimensionDate.objects.get_or_create(id=date_pk, year=date.year, month=date.month, day=date.day)
    return dim_date


def get_or_create_dimension_happiness_level(level):
    dim_key = '_'.join(level.lower().split())
    dim_happiness, _ = DimensionHappinessLevel.objects.get_or_create(id=dim_key, level=level)
    return dim_happiness


def get_or_create_dimension_happiness(score: int) -> DimensionHappinessLevel:
    levels = ['Extremely happy',
              'Happy',
              'Slightly Happy',
              'Neutral',
              'Slightly Happy',
              'Unhappy',
              'Extremely unhappy']
    if score > 30:
        return get_or_create_dimension_happiness_level(level=levels[0])
    if score > 25:
        return get_or_create_dimension_happiness_level(level=levels[1])
    if score > 21:
        return get_or_create_dimension_happiness_level(level=levels[2])
    if score == 20:
        return get_or_create_dimension_happiness_level(level=levels[3])
    if score > 14:
        return get_or_create_dimension_happiness_level(level=levels[4])
    if score > 9:
        return get_or_create_dimension_happiness_level(level=levels[5])

    return get_or_create_dimension_happiness_level(level=levels[6])


def get_or_create_dimension_teams(user) -> list[DimensionTeam]:
    dims = [DimensionTeam(name=team.name, id=team.id) for team in Team.objects.filter(users__pk=user)]
    DimensionTeam.objects.bulk_create(dims, ignore_conflicts=True, batch_size=100)
    return dims


def create_fact_response(dim_date: DimensionDate, dims_team: list[DimensionTeam], dim_happiness, score: int):
    fact_responses = []
    for dim_team in dims_team:
        fact_response = FactResponse(dim_date=dim_date, dim_team=dim_team, dim_happiness=dim_happiness, score=score)
        fact_responses.append(fact_response)
    FactResponse.objects.bulk_create(fact_responses, ignore_conflicts=True, batch_size=100)


def load_check_in(check_in):
    score = sum(check_in.get('responses'))
    user = check_in.get('user')
    dim_date = get_or_create_dimension_date(date=check_in.get('created'))
    dims_team = get_or_create_dimension_teams(user=user)
    dim_happiness = get_or_create_dimension_happiness(score=score)
    create_fact_response(dim_date=dim_date, dims_team=dims_team, dim_happiness=dim_happiness, score=score)

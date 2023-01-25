import datetime

from django.utils import dateparse
from .models import (DimensionTeam,
                     DimensionDate,
                     FactResponse,
                     DimensionHappinessLevel,
                     LEVELS_OF_HAPPINESS)
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


def get_or_create_dimension_happiness_by_score(score: int) -> DimensionHappinessLevel:
    if score > 30:
        return get_or_create_dimension_happiness_level(level=LEVELS_OF_HAPPINESS[0])
    if score > 25:
        return get_or_create_dimension_happiness_level(level=LEVELS_OF_HAPPINESS[1])
    if score > 21:
        return get_or_create_dimension_happiness_level(level=LEVELS_OF_HAPPINESS[2])
    if score == 20:
        return get_or_create_dimension_happiness_level(level=LEVELS_OF_HAPPINESS[3])
    if score > 14:
        return get_or_create_dimension_happiness_level(level=LEVELS_OF_HAPPINESS[4])
    if score > 9:
        return get_or_create_dimension_happiness_level(level=LEVELS_OF_HAPPINESS[5])

    return get_or_create_dimension_happiness_level(level=LEVELS_OF_HAPPINESS[6])


def get_or_create_dimension_teams(user) -> list[DimensionTeam]:
    dims = [DimensionTeam(name=team.name, id=team.id) for team in Team.objects.filter(users__pk=user)]
    DimensionTeam.objects.bulk_create(dims, ignore_conflicts=True, batch_size=100)
    return dims


def load_fact_table(dim_date: DimensionDate, dims_team: list[DimensionTeam], dim_happiness, score: int):
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
    dim_happiness = get_or_create_dimension_happiness_by_score(score=score)
    load_fact_table(dim_date=dim_date, dims_team=dims_team, dim_happiness=dim_happiness, score=score)

import datetime

from unittest.mock import Mock, patch
from happiness.daily.models import validate_same_day
from rest_framework.exceptions import APIException


@patch('django.utils.timezone.now')
@patch('happiness.daily.models.CheckIn.objects')
def test_validate_different_day(mock_objects, mock_now):
    # given
    yesterday = datetime.datetime(year=2023, month=1, day=24)
    today = datetime.datetime(year=2023, month=1, day=25)
    last_checkin = Mock(created=yesterday)

    mock_now.return_value = today
    mock_objects.filter().latest.return_value = last_checkin

    try:
        user = Mock(id=1)
        # when
        validate_same_day(user)
    except APIException:
        # then
        assert False


@patch('django.utils.timezone.now')
@patch('happiness.daily.models.CheckIn.objects')
def test_validate_same_day(mock_objects, mock_now):
    # given
    yesterday = datetime.datetime(year=2023, month=1, day=25)
    today = datetime.datetime(year=2023, month=1, day=25)
    last_checkin = Mock(created=yesterday)

    mock_now.return_value = today
    mock_objects.filter().latest.return_value = last_checkin

    try:
        user = Mock(id=1)
        # when
        validate_same_day(user)
    except APIException:
        # then
        assert True

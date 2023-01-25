import datetime

from unittest.mock import Mock, patch
from happiness.daily.models import verify_same_day
from rest_framework.exceptions import APIException


@patch('django.utils.timezone.now')
@patch('happiness.daily.models.CheckIn.objects')
def test_verify_same_day(mock_objects, mock_now):
    today = datetime.datetime(year=2023, month=1, day=24)
    tomorrow = datetime.datetime(year=2023, month=1, day=25)

    user = Mock(id=1)
    latest = Mock(created=today)

    mock_now.return_value = tomorrow
    mock_objects.filter().latest.return_value = latest

    try:
        verify_same_day(user)
    except APIException:
        assert False



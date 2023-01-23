from .api.serializers import CheckInSerializer
from .models import CheckIn


def serialize_check_in(check_in: CheckIn):
    return CheckInSerializer(check_in).data

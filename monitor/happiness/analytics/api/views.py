from rest_framework.views import APIView

from rest_framework.response import Response
from .serializers import TeamSerializer
from ..models import get_statistics, get_statistics_anonymous


class TeamListAPIView(APIView):
    serializer_class = TeamSerializer

    def get(self, request, version):
        if request.user.id is None:
            return Response(get_statistics_anonymous())

        return Response(get_statistics(user=request.user))

from rest_framework.views import APIView

from rest_framework.response import Response
from .serializers import TeamSerializer
from ..models import get_statistics, get_statistics_anonymous


class TeamListAPIView(APIView):
    serializer_class = TeamSerializer

    def get(self, request, version):
        """
        Return a list.
        """
        if request.user.id is None:
            print('Anonymous request')
            return Response(get_statistics_anonymous())

        return Response(get_statistics(user=request.user))

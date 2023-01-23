from rest_framework.views import APIView


from rest_framework.response import Response
from .serializers import TeamSerializer
from ..models import select_stats_from_authenticated_user
from ...team.models import Team


class TeamListAPIView(APIView):
    serializer_class = TeamSerializer

    def get(self, request, version, format=None):
        """
        Return a list.
        """
        print(request.user)
        if str(request.user) == 'AnonymousUser':
            print('Anonymous request')
        teams = [team for team in Team.objects.filter(users__pk=request.user.id)]
        select_stats_from_authenticated_user(teams)
        return Response(select_stats_from_authenticated_user(teams))

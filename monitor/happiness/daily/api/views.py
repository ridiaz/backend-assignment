from rest_framework.generics import CreateAPIView

from rest_framework.permissions import IsAuthenticated
from ..api.serializers import CheckInSerializer


class CheckInCreateAPIView(CreateAPIView):
    serializer_class = CheckInSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


from rest_framework import viewsets

from . import serializers
from . import models


class FederativeUnitViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FederativeUnitSerializer
    queryset = models.FederativeUnit.objects.all()

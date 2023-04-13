from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAdminOrReadOnly


class CreateDestroyListViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet
):
    pass


class AdminPermissionsMixin:
    def get_permissions(self):
        if self.action in ('create', 'partial_update', 'destroy'):
            return (IsAdminOrReadOnly(),)
        return super().get_permissions()

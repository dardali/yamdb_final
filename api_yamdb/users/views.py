from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .permissions import AdminPermission
from .serializers import (RegistrationSerializer, UserSerializer,
                          VerificationSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (AdminPermission, )
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    @action(
        detail=False,
        methods=['GET', 'PATCH', 'PUT'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = self.get_serializer(request.user, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get('role'):
            if request.user.role != (User.ROLE_ADMIN or not
                                     request.user.is_superuser):
                serializer.validated_data['role'] = request.user.role

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('role'):
            if not (request.user.role == User.ROLE_ADMIN
                    or request.user.is_superuser):
                serializer.validated_data['role'] = instance.role
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user, created = User.objects.get_or_create(
        username=username, email=email)
    if created:
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            "YaMDb: код для подтверждения регистрации",
            f"Ваш код для получения токена: {confirmation_code}",
            {DEFAULT_FROM_EMAIL},
            [email],
            fail_silently=False,
        )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verification_view(request):
    serializer = VerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, confirmation_code):
        raise serializers.ValidationError(
            {'error': 'Invalidconfirmation code'})
    token = AccessToken.for_user(user)
    return Response(data={'token': str(token)}, status=status.HTTP_200_OK)

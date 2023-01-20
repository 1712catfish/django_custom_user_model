from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from djoser.conf import settings
from djoser.permissions import CurrentUserOrAdmin
from djoser.serializers import UserSerializer, UserCreateSerializer, UserDeleteSerializer
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .serializers import CustomAdminSerializer, CustomAdminListSerializer, CustomUserSerializer, \
    CustomUserDeleteSerializer

User = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    permission_classes = [CurrentUserOrAdmin, ]
    token_generator = default_token_generator

    def get_instance(self):
        return self.request.user

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny, ]
        elif self.action == "list":
            self.permission_classes = [IsAdminUser, ]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.request.user.is_staff:
            if self.request.method == 'GET' and self.kwargs.get('pk') is None:
                return CustomAdminListSerializer
            return CustomAdminSerializer
        elif self.action == 'me':
            if self.request.method == 'DELETE':
                return CustomUserDeleteSerializer
        return self.serializer_class

    # def retrieve(self, request, *args, **kwargs):
    #     self.pk = kwargs.get('pk')
    #     super().retrieve(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if self.kwargs.get('pk') == 1:
            return Response({'details': 'Cannot delete root admin'}, status=status.HTTP_401_UNAUTHORIZED, )

        if instance == request.user:
            utils.logout_user(self.request)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)

            utils.logout_user(self.request)
            instance.is_active = False
            instance.save(update_fields=["is_active"])
            return Response(status=status.HTTP_204_NO_CONTENT)

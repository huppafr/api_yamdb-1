from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .generate_code import generate_confirmation_code, send_mail_to_user
from .models import User
from .permissions import IsAdmin, IsSuperuser
from .serializers import UserSerializer


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer = UserSerializer

    def post(self, request):
        validate = self.serializer(data=request.data)
        validate.is_valid(raise_exception=True)
        email = validate.validated_data('email')
        user = User.objects.order_by('email').first()
        if user > 0:
            confirmation_code = user[0].confirmation_code
        else:
            confirmation_code = generate_confirmation_code()
            base_username = email.split('@')[0]
            data = {
                'email': email,
                'confirmation_code': confirmation_code,
                'username': f'{base_username}'
            }
            serializer = self.serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        send_mail_to_user(email, confirmation_code)
        return Response({'email': email})


class TokenView(APIView):
    permission_classes = (AllowAny,)
    serializer = UserSerializer

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def post(self, request):
        validate = self.serializer(data=request.data)
        validate.is_valid(raise_exception=True)
        email = validate.validated_data('email')
        user = get_object_or_404(User, email=email)
        code = validate.validated_data('confirmation_code')
        if user.confirmation_code != code:
            response = {'confirmation_code': 'Неверный код'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = {'token': self.get_token(user)}
        return Response(response, status=status.HTTP_200_OK)


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsSuperuser | IsAdmin,)

    @action(detail=False, permission_classes=(IsAuthenticated,),
            methods=['get', 'patch'], url_path='me')
    def get_or_update_self(self, request):
        if request.method != 'GET':
            serializer = self.get_serializer(
                instance=request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data)

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Persona
from .serializers.personaSerializer import PersonaSerializer
from .serializers.userSerializer import UserSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets


# Create your views here.
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
        }
    ),
    responses={200: 'OK', 400: 'Invalid Password'}
)
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({
            "error": "Invalid Password"
        },
            status=status.HTTP_400_BAD_REQUEST
        )

    token, created = Token.objects.get_or_create(user=user)

    serializer = UserSerializer(instance=user)

    return Response({
        "token": token.key,
        "user": serializer.data
    },
        status=status.HTTP_200_OK
    )


@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    responses={201: 'Created', 400: 'Bad Request'}
)
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user=user)

        return Response({
            'token': token.key,
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token", type=openapi.TYPE_STRING)
    ],
    responses={200: 'OK'}
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({
        f'You are logged with @{request.user.username}'
    },
        status=status.HTTP_200_OK
    )


class PersonaApiView(viewsets.ModelViewSet):
    serializer_class = PersonaSerializer
    queryset = Persona.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

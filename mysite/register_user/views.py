from rest_framework import status,generics
from .serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LogoutSerializer



class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer


    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'detail':f'{e} тура эмес маалымат келди'}, status.HTTP_400_BAD_REQUEST)
        except NameError:
            return Response({'detail':'ошибка в коде бек '},status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            return Response({'detail': 'ошибка в коде бек '},status.HTTP_500_INTERNAL_SERVER_ERROR)




class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data.get("refresh_token")

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Вы успешно вышли"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Невалидный или уже аннулированный токен"}, status=status.HTTP_400_BAD_REQUEST)


class NetworkCreateAPIView(generics.CreateAPIView):
    serializer_class = NetworkPostSerializer

class UserProfileRetrieveAPIView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileAllListSerializer


class UserProfileUpdatedAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileAllPutSerializer
    queryset = UserProfile.objects.all()


class UserProfileListAPIView(generics.ListAPIView):
    serializer_class = UserProfileListSerializer
    queryset = UserProfile.objects.all()

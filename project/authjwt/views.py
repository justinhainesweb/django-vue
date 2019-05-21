from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken
from .utils import EmailVerifier


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def get_current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def lookup_email(request):
    """
    Lookup the entered email
    """
    email = request.data.get('email', None)
    result = EmailVerifier.lookup(email)

    return Response({'result': result})


class UserList(APIView):

    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        """
        Create a new user
        :param request:
        :param format:
        :return:
        """
        serializer = UserSerializerWithToken(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

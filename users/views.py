from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer
from .authentication import generate_access_token, JWTAuthentication

@api_view(['POST'])
def register(request):
	data = request.data

	if data['password'] != data['password_confirm']:
		raise exceptions.APIException('Password do not match dumdum')

	serializer = UserSerializer(data=data)
	serializer.is_valid(raise_exception=True)
	serializer.save()
	return Response(serializer.data)

@api_view(['POST'])
def login(request):
	email = request.data.get('email')
	password = request.data.get('password')

	user = User.objects.filter(email=email).first()
	
	# validation here
	if user is None:
		raise exceptions.AuthenticationFailed('User not found SUKAH!')

	# check if passwords match
	if not user.check_password(password):
		raise exceptions.AuthenticationFailed('Inkorreckt pass, jerk!')

	response = Response()
	
	token = generate_access_token(user)
	response.set_cookie(key='jwt', value=token, httponly=True)

	response.data = {
		'jwt': token
	}

	return response

@api_view(['POST'])
def logout(_):
	# need to delete cookie on logout
	response = Response()
	response.delete_cookie(key='jwt')
	response.data = {
		'message': 'success, you logged out ddoood'
	}
	print (response)

	return response

class AuthenticatedUser(APIView):
	# this middleware checks if user is auth, and throws error if not
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		serializer = UserSerializer(request.user)

		return Response({
			'data': serializer.data
		})


@api_view(['GET'])
def users(request):
	serializer = UserSerializer(User.objects.all(), many=True)
	return Response(serializer.data)
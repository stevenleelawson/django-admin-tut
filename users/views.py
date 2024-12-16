from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

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

	return Response('success')


@api_view(['GET'])
def users(request):
	serializer = UserSerializer(User.objects.all(), many=True)
	return Response(serializer.data)
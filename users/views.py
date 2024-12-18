from rest_framework import exceptions, viewsets, status, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reborn_django_admin.pagination import CustomPagination
from .models import User, Permission, Role
from .serializers import UserSerializer, PermissionsSerializer, RoleSerializer
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

class PermissionAPIView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		serializer = PermissionsSerializer(Permission.objects.all(), many=True)

		return Response({
			'data': serializer.data
		})
	
class RoleViewSet(viewsets.ViewSet):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	def list(self, request):
		serializer = RoleSerializer(Role.objects.all(), many=True)

		return Response({
			'data': serializer.data
		})

	def create(self, request):
		serializer = RoleSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({
			'data': serializer.data
		}, status=status.HTTP_201_CREATED)

	def retrieve(self, request, pk=None):
		role = Role.objects.get(id=pk)
		serializer = RoleSerializer(role)

		return Response({
			'data': serializer.data
		})

	def update(self, request, pk=None):
		role = Role.objects.get(id=pk)
		serializer = RoleSerializer(instance=role, data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response({
			'data': serializer.data
		}, status=status.HTTP_202_ACCEPTED)

	def destroy(self, request, pk=None):
		role = Role.objects.get(id=pk)
		role.delete()

		return Response(status=status.HTTP_204_NO_CONTENT)

class UserGenericAPIView(
	generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
	# for auth
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	queryset = User.objects.all()
	serializer_class = UserSerializer
	pagination_class = CustomPagination
	#primary key by default is None
	def get(self, request, pk=None):
		#if pk is not None
		if pk:
			return Response({
				'data': self.retrieve(request, pk).data
			})
		# easiest way to add 'data' for the FE is to just use Response
		# commented this out coz it was adding an extra 'data' layer
		# return Response({
		# 	'data': self.list(request).data
		# })
		return self.list(request)
	
	def post(self, request):
		return Response({
			'data': self.create(request).data
		})

	def put(self, request, pk=None):
		return Response({
			'data': self.update(request).data
		})

	def delete(self, request, pk=None):
		return self.destroy(request, pk=None)
		# dont neeed to return data here, hence commented out
		# return Response({
		# 	'data': self.destroy(request).data
		# })
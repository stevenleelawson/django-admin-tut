from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from reborn_django_admin.pagination import CustomPagination
from products.serializers import ProductSerializer
from users.authentication import JWTAuthentication


class ProductGenericAPIView(
	generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
	# for auth
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	queryset = Product.objects.all()
	serializer_class = ProductSerializer
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
			'data': self.partial_update(request).data
		})

	def delete(self, request, pk=None):
		return self.destroy(request, pk=None)

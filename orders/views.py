from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from users.authentication import JWTAuthentication
from orders.models import Order
from reborn_django_admin.pagination import CustomPagination
from orders.serializers import OrderSerializer


class OrderGenericAPIView(
	generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
	# for auth
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	queryset = Order.objects.all()
	serializer_class = OrderSerializer
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
	

import csv
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from rest_framework import generics, mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from users.authentication import JWTAuthentication
from orders.models import Order
from orders.models import OrderItem
from reborn_django_admin.pagination import CustomPagination
from orders.serializers import OrderSerializer
from rest_framework.views import APIView


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
	
class ExportAPIView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=orders.csv'

		orders = Order.objects.all()
		writer = csv.writer(response)

		writer.writerow(['ID', 'Name', 'Email', 'Product Title', 'Price', 'Quantity'])

		for order in orders:
			writer.writerow([order.id, order.name, order.email, '', '', ''])
			orderItems = OrderItem.objects.all().filter(order_id=order.id)

			for item in orderItems:
				writer.writerow([ '', '', '', item.product_title, item.price, item.quantity])

		return response


class ChartAPIView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, _):
		# need to display for each date, the orders for that date; so need a RAW SQL QUERY
		# a JOIN for orders and orderitems
		with connection.cursor() as cursor:
			cursor.execute("""
			SELECT DATE_FORMAT(o.created_at, '%Y-%m-%d') as date, sum(i.quantity * i.price) as sum
			FROM orders_order as o
			JOIN orders_orderitem as i ON o.id = i.order_id
			GROUP BY date
			""")
			row = cursor.fetchall()

			#this var effectivly LABELS our response, ie changes to more readable key/val
			data = [{
				'date': result[0],
				'sum': result[1]
			} for result in row]

			return Response({
				'data': data
			})

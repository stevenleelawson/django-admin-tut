import jwt
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

def generate_access_token(user):
	payload = {
		'user_id': user.id,
		'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
		'iat': datetime.datetime.utcnow()
	}

	# NO NEED TO DECODE, SHIZ IS DEPRECATED
	return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

class JWTAuthentication(BaseAuthentication):

	def authenticate(self, request):
		token = request.COOKIES.get('jwt')

		if not token:
			return None

		try:
			payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
		except jwt.ExpiredSignatureError:
			# if we don't get payload throw error aka raise exception
			raise exceptions.AuthenticationFailed('unauthenticated, you chode')

		user = get_user_model().objects.filter(id=payload['user_id']).first()

		if user is None:
			raise exceptions.AuthenticationFailed('Yoooser not found, looser!')
		
		return (user, None)
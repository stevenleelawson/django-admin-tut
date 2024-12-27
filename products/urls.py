from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductGenericAPIView, FileUploadView

urlpatterns = [
	path('products', ProductGenericAPIView.as_view()),
	path('products/<str:pk>', ProductGenericAPIView.as_view()),
	path('upload', FileUploadView.as_view())
	# the below concatenation allowed us to GET an image at say http://localhost:8000/api/media/LawsonResume.pdf
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
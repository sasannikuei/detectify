from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedImage
from .serializers import UploadedImageSerializer
import requests


class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UploadedImageSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            image_path = instance.image.path

            # ارسال به Colab API
            files = {"file": open(image_path, "rb")}
            response = requests.post("https://colab.research.google.com/drive/12rIjbYf0kxmjciS2b8TmeRD0lc-Zw1tc#scrollTo=XnplQ_zg8PcO", files=files)


            return Response({
                "image_url": request.build_absolute_uri(instance.image.url),
                "detections": response.json().get("detections", [])
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

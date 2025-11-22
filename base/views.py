from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UploadedImageSerializer
from ultralytics import YOLO


# Loading YOLO model.
model = YOLO("models/yolov8n.pt")



class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UploadedImageSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            image_path = instance.image.path

            # Running YOLO on photo
            results = model(image_path)

            detections = []
            for r in results:
                for box in r.boxes:
                    detections.append({
                        "class": int(box.cls[0]),
                        "confidence": float(box.conf[0]),
                        "xyxy": box.xyxy[0].tolist()
                    })

            return Response({
                "image_url": request.build_absolute_uri(instance.image.url),
                "detections": detections
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

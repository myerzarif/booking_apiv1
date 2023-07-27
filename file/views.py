from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from config.logger import LoggerMixin
from file.serializers import UploadFileSerializer


class UploadFileView(LoggerMixin, GenericAPIView):
    serializer_class = UploadFileSerializer
    permission_classes = [IsAuthenticated]
    name = "file_upload"

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        return Response(data=self.serializer.data, status=201)
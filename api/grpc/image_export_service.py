# api/grpc/image_export_service.py
import export_pb2
import export_pb2_grpc
from service.image_service import ImageService
from concurrent import futures

class ImageExportService(export_pb2_grpc.ImageExportServiceServicer):
    def __init__(self):
        self.service = ImageService()

    def ExportImages(self, request, context):
        images = self.service.list_images(request.author or None, request.tag or None)
        for img in images:
            yield export_pb2.ImageExportResponse(
                id=img.id,
                title=img.title,
                image=img.image,
                author=img.author,
                tags=img.tags,
                created_at=str(img.created_at)
            )

from fastapi import FastAPI
from api.rest.image_router import router as image_router
import grpc
from export_pb2_grpc import add_ImageExportServiceServicer_to_server
from api.grpc.image_export_service import ImageExportService
from concurrent import futures
import threading

app = FastAPI(title="Image CMS")
app.include_router(image_router, prefix="/images", tags=["Images"])

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ImageExportServiceServicer_to_server(ImageExportService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":

    threading.Thread(target=serve_grpc).start()

    import uvicorn
    uvicorn.run("main:app", reload=True)  # runs at localhost:8000

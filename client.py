import requests
import grpc
import export_pb2
import export_pb2_grpc
import time

REST_BASE_URL = "http://localhost:8000/images"

def test_rest_api():

    payload = {
        "image": "https://example.com/cat.jpg",
        "title": "Cute Cat",
        "author": "DRAKE ANDREW",
        "tags": ["animal", "cute"]
    }
    res = requests.post(REST_BASE_URL + "/", json=payload)
    print("Create Image Response:", res.status_code, res.json())
    created_image = res.json()
    image_id = created_image['id']

    res = requests.get(REST_BASE_URL + "/")
    print("List Images Response:", res.status_code, res.json())

    res = requests.get(f"{REST_BASE_URL}/{image_id}")
    print("Get Image Response:", res.status_code, res.json())

    update_payload = {"title": "Adorable Cat"}
    res = requests.put(f"{REST_BASE_URL}/{image_id}", json=update_payload)
    print("Update Image Response:", res.status_code, res.json())

    res = requests.delete(f"{REST_BASE_URL}/{image_id}")
    print("Delete Image Response:", res.status_code, res.json())

    res = requests.post(REST_BASE_URL + "/", json=payload)
    print("Creating Image Response for grpc streaming", res.status_code, res.json())

GRPC_SERVER_ADDRESS = "localhost:50051"

def test_grpc_api():
    channel = grpc.insecure_channel(GRPC_SERVER_ADDRESS)
    stub = export_pb2_grpc.ImageExportServiceStub(channel)

    request = export_pb2.ExportImagesRequest(author="", tag="")
    responses = stub.ExportImages(request)
    print("Exported Images:")
    try:
        for response in responses:
            print(f"- ID: {response.id}, Title: {response.title}, Author: {response.author}, Tags: {list(response.tags)}, Created At: {response.created_at}")
    except grpc.RpcError as e:
        print("gRPC error:", e)



if __name__ == "__main__":
    print("Waiting a few seconds for servers to start...")
    time.sleep(3)

    test_rest_api()
    test_grpc_api()

Setup Instructions
    Install all listed dependencies.

    pip install fastapi
    pip install sqlalchemy
    pip install grpcio
    pip install grpcio-tools
    pip install uvicorn

Run the application:

    Checkout the SWA2 branch locally.

    Run the main file:
    python main.py

Access the application:

    REST API is available at http://127.0.0.1:8000

    gRPC server is available at localhost:50051

REST API Endpoints

List all images
    GET http://127.0.0.1:8000/images
    Retrieves all images stored in the database.
    You can optionally filter results using query parameters author and tag.
    Example: GET /images?author=Yash&tag=nature

Create a new image
    POST http://127.0.0.1:8000/images
    Provide the following body to create a new image entry:

    { "image": "https://example.com/test.jpg", "title": "Test Title", "author": "Yash Tapadiya", "tags": ["fun", "nature"] }

Get details of a specific image
    GET http://127.0.0.1:8000/images/{id}
    Fetch details of a specific image by its id.

Update an image
    PUT http://127.0.0.1:8000/images/{id}
    Provide the updated title in the body:

    { "title": "Updated Title" }

Delete an image
    DELETE http://127.0.0.1:8000/images/{id}
    Delete an image record by its id.

gRPC Export API

    The export.proto file is located at: proto/export.proto

    To use the Export API:

    Open a gRPC tool like Postman (gRPC mode).

    Connect to localhost:50051.

    Choose the ExportImages function and make a request.

    Example request to filter by tag or author:

    { "tag": "fun", "author": "Yash" }

    If no filters are provided, the server will stream all images.
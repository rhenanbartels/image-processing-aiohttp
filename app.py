from io import BytesIO

import requests
from aiohttp import web

import face_recognition
from aiohttp_cache import cache, setup_cache


API_VERSION = "v0.1"


def detect_faces(img_content):
    img = face_recognition.load_image_file(BytesIO(img_content))
    return len(face_recognition.face_locations(img)) > 0


def request_image(img_url):
    resp = requests.get(img_url)
    return  resp.content


@cache()
async def faces_view(request):
    img_url = request.rel_url.query.get("img_url")
    if img_url:
        try:
            img = request_image(img_url)
        except Exception as e:
            response = {
                "error": "not able to retrieve image from {img_url}"
            }
            status = 503
        try:
            response = {"faces": detect_faces(img)}
            status = 200
        except Exception as e:
            response = {
                "error": f"error during face detection in image from {img_url}"
            }
            status = 503
    else:
        response = {"error": "img url not provided"}
        status = 400

    return web.json_response(response, status=status)


app = web.Application()
setup_cache(app)
app.router.add_get(f"/{API_VERSION}/faces", faces_view)

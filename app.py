from io import BytesIO

import requests
from aiohttp import web

import face_recognition
from aiohttp_cache import cache, setup_cache


def detect_faces(img_url):
    resp = requests.get(img_url)
    img = face_recognition.load_image_file(BytesIO(resp.content))
    return len(face_recognition.face_locations(img)) > 0


@cache()
async def has_faces_view(request):
    img_url = request.rel_url.query.get("img_url")
    if img_url:
        response = {"has_face": detect_faces(img_url)}
        status = 200
    else:
        response = {"error": "img url not provided"}
        status = 400

    return web.json_response(response, status=status)


app = web.Application()
setup_cache(app)
app.router.add_get("/has-faces", has_faces_view)

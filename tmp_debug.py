import io
from PIL import Image
from app import app

app.config['TESTING'] = True
with app.test_client() as client:
    image = Image.new('RGB', (224, 224), color=(20, 160, 50))
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    payload = buffer.getvalue()
    res = client.post(
        '/api/diagnose-disease',
        data={'leaf_photo': (io.BytesIO(payload), 'septoria_leaf_spot.jpg'), 'crop': 'tomato', 'lang': 'en'},
        content_type='multipart/form-data'
    )
    print('status', res.status_code)
    print(res.get_data(as_text=True))

import io
from PIL import Image
from disease_service import diagnose_plant_photo

image = Image.new('RGB', (224, 224), color=(20, 160, 50))
buffer = io.BytesIO(); image.save(buffer, format='PNG'); payload = buffer.getvalue()
print(diagnose_plant_photo(filename='green_leaf.png', file_bytes=payload, crop_id='tomato', lang='en'))

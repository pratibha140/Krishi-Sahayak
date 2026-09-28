import io
from PIL import Image
import torch
from disease_service import _load_plant_disease_model

image = Image.new('RGB', (224, 224), color=(20, 160, 50))
# emulate preprocess
width, height = image.size
short_edge = min(width, height)
scale = 256 / float(short_edge)
new_width = max(1, int(round(width * scale)))
new_height = max(1, int(round(height * scale)))
image = image.resize((new_width, new_height), Image.BILINEAR)
left = max(0, (new_width - 224) // 2)
top = max(0, (new_height - 224) // 2)
image = image.crop((left, top, left + 224, top + 224))
print('size', image.size)
tensor = torch.tensor(image.tobytes(), dtype=torch.float32).view(224, 224, 3)
print('tensor shape', tensor.shape, tensor.min().item(), tensor.max().item())
tensor = tensor.permute(2, 0, 1) / 255.0
mean = torch.tensor([0.5, 0.5, 0.5], dtype=torch.float32).view(3, 1, 1)
std = torch.tensor([0.5, 0.5, 0.5], dtype=torch.float32).view(3, 1, 1)
tensor = (tensor - mean) / std
pixel_values = tensor.unsqueeze(0)
print('pixel_values shape', pixel_values.shape)
model = _load_plant_disease_model()
print('model loaded', model is not None)
try:
    with torch.no_grad():
        logits = model(pixel_values=pixel_values).logits
    print('logits', logits.shape)
    probs = torch.softmax(logits, dim=-1)
    print('probs top', probs.argmax(dim=-1).item(), float(probs[0, probs.argmax(dim=-1).item()]) * 100)
except Exception as exc:
    print('ERROR', type(exc).__name__, exc)
    raise

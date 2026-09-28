import io
from PIL import Image
import torch
from disease_service import _load_plant_disease_model

path = r'D:\septoria-spot-tomato-plant-ea2ab44d-e6f21d609dd04b2f96d96a33e98aab07.jpg'
img = Image.open(path).convert('RGB')
width, height = img.size
short_edge = min(width, height)
scale = 256 / float(short_edge)
new_width = max(1, int(round(width * scale)))
new_height = max(1, int(round(height * scale)))
img = img.resize((new_width, new_height), Image.BILINEAR)
left = max(0, (new_width - 224) // 2)
top = max(0, (new_height - 224) // 2)
img = img.crop((left, top, left + 224, top + 224))
tensor = torch.tensor(list(img.getdata()), dtype=torch.float32).view(224,224,3)
tensor = tensor.permute(2,0,1) / 255.0
mean = torch.tensor([0.5, 0.5, 0.5], dtype=torch.float32).view(3,1,1)
std = torch.tensor([0.5, 0.5, 0.5], dtype=torch.float32).view(3,1,1)
tensor = (tensor - mean) / std
pixel_values = tensor.unsqueeze(0)
model = _load_plant_disease_model()
with torch.no_grad():
    logits = model(pixel_values=pixel_values).logits
probs = torch.softmax(logits, dim=-1)
top_index = int(probs.argmax(dim=-1).item())
print('top_index', top_index)
print('label', model.config.id2label[top_index])
print('confidence', float(probs[0,top_index]) * 100)
for i in range(5):
    p = float(probs[0,i]) * 100
    print(i, model.config.id2label[i], round(p, 2))

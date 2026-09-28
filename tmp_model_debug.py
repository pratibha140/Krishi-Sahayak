from transformers import AutoImageProcessor, AutoModelForImageClassification

model_name = 'linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification'
try:
    processor = AutoImageProcessor.from_pretrained(model_name)
    print('processor ok', processor)
except Exception as exc:
    print('processor failed', type(exc).__name__, exc)

try:
    model = AutoModelForImageClassification.from_pretrained(model_name)
    print('model ok', model.__class__.__name__)
except Exception as exc:
    print('model failed', type(exc).__name__, exc)

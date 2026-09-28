# Task: Fix Disease Diagnosis Using Actual Image Model

## Goal
Replace the current filename/crop-based disease prediction with real image inference using the already verified Hugging Face model:

linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification

The model has already been tested successfully outside the Flask app.

Test result:
- Input image: D:\septoria-spot-tomato-plant-ea2ab44d-e6f21d609dd04b2f96d96a33e98aab07.jpg
- Top prediction: Tomato with Septoria Leaf Spot
- Confidence: 53.24%

## Important constraints
- Do NOT redesign any UI.
- Do NOT change disease.html layout/styling unless absolutely required for model integration.
- Do NOT remove existing recovery/treatment/advisory information.
- Do NOT remove upload or camera functionality.
- Do NOT disable CSRF protection.
- Do NOT use the uploaded filename to determine the disease.
- Do NOT use crop_id or filename keywords as the prediction mechanism.
- Do NOT replace the specified Hugging Face model.
- Do NOT add an API key or paid external service.
- Keep the existing Flask route structure as much as possible.
- Make the smallest clean change required.

## Model details already verified
Model:
linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification

Architecture:
MobileNetV2ForImageClassification

38 labels.

Required image preprocessing:
1. Convert image to RGB.
2. Resize shortest edge to 256.
3. Center crop to 224x224.
4. Convert to tensor.
5. Rescale pixels by 1/255.
6. Normalize using mean [0.5, 0.5, 0.5].
7. Normalize using std [0.5, 0.5, 0.5].

## Existing project
Inspect:
- app.py
- disease_service.py
- disease.html
- existing disease-related static JS
- requirements.txt

Find the existing disease upload route and the existing diagnose_plant_photo() flow.

## Required implementation
1. Load the Hugging Face model safely.
2. Load it once rather than downloading/loading it for every request.
3. Use the actual uploaded image bytes/file.
4. Apply the verified preprocessing above.
5. Run inference with torch.no_grad().
6. Apply softmax to obtain probabilities.
7. Return the predicted label and confidence to the existing disease flow.
8. Preserve the existing disease information/recovery/treatment/advisory lookup.
9. Handle invalid/corrupt images safely with an appropriate existing-style error response.
10. Do not crash the Flask application if model loading or inference fails.

## Important
The current disease_service.py has a diagnose_plant_photo() implementation that can determine diseases from crop_id/filename information.

That behavior must no longer determine the disease prediction when an uploaded image is available.

The actual uploaded image must be passed through the MobileNetV2 model.

## Dependencies
If required dependencies are missing, update requirements.txt with compatible versions already installed/tested in this Python 3.11 environment.

Do not unnecessarily downgrade Transformers.

## Verification
After implementation:

1. Run Python syntax/compile checks.
2. Verify the Flask app starts.
3. Test the disease diagnosis flow.
4. Use an actual image file for inference.
5. Confirm that changing the filename alone cannot change the prediction.
6. Confirm that image bytes are actually passed into the model.
7. Confirm existing recovery/treatment information still appears.
8. Confirm CSRF protection remains enabled.
9. Check git diff and ensure only disease-diagnosis-related files changed.

## Final report
Report:
- files changed
- exact model integration approach
- preprocessing used
- test image prediction
- confidence
- verification results
- any remaining issue

Do not modify unrelated files.
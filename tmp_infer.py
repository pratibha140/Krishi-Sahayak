from disease_service import diagnose_plant_photo

path = r'D:\septoria-spot-tomato-plant-ea2ab44d-e6f21d609dd04b2f96d96a33e98aab07.jpg'
with open(path, 'rb') as f:
    data = f.read()
print(diagnose_plant_photo(filename='septoria_leaf_spot.jpg', file_bytes=data, crop_id='tomato', lang='en'))

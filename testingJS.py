# pip install jigsawstack requests
from jigsawstack import JigsawStack
import requests

# Step 1: Initialize API
jigsaw = JigsawStack(api_key="sk_6098d858be8d9d58480a835b3d64978ee8b3ef47317fc96179c820b6028bb1728cd561569f9cff333fce5a40446c7a2cbb0708963d97be3c992cd003c1c6143c0246Q039dNAgM9qMuf4x2")

# Step 2: Call the API
response = jigsaw.image_generation({
    "prompt": "Make a long queue with real people. One of them is holding onto the product image flat on their palm (do some image distortion to achieve this) and eating a mint from it. At the side it says 'Refresh and Take a Mint' in modern font.",
    "url": "https://i.postimg.cc/kgkrhY64/p1.jpg"
})

# Step 3: Print the full response
#print(response)

# Save the image bytes directly to a file
with open("output_image2.png", "wb") as f:
    f.write(response)

print("Image saved as output_image.png")

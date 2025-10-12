# Colab Prototype: Project Parampara (Color/Creative Variations)
!pip install opencv-python-headless pillow qrcode matplotlib

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt
import qrcode
from google.colab import files
import random

# -------------------------------
# 1. AI Design Co-Pilot (Color & Creative Variations)
# -------------------------------
def generate_design_variations_color(input_image_path, num_variations=3):
    img = Image.open(input_image_path).convert("RGB")
    variations = []

    for i in range(num_variations):
        new_img = img.copy()
        img_np = np.array(new_img).astype(np.float32)

        # Random color shift
        r_shift = random.randint(-50, 50)
        g_shift = random.randint(-50, 50)
        b_shift = random.randint(-50, 50)
        img_np[:,:,0] = np.clip(img_np[:,:,0] + r_shift, 0, 255)  # R channel
        img_np[:,:,1] = np.clip(img_np[:,:,1] + g_shift, 0, 255)  # G channel
        img_np[:,:,2] = np.clip(img_np[:,:,2] + b_shift, 0, 255)  # B channel

        new_img = Image.fromarray(img_np.astype('uint8'))

        # Random brightness
        enhancer = ImageEnhance.Brightness(new_img)
        factor = random.uniform(0.7, 1.3)
        new_img = enhancer.enhance(factor)

        # Random contrast
        enhancer = ImageEnhance.Contrast(new_img)
        factor = random.uniform(0.7, 1.3)
        new_img = enhancer.enhance(factor)

        # Optional: add a simple artistic effect - slight blur
        if random.random() > 0.5:
            new_img = new_img.filter(ImageFilter.SMOOTH)

        save_path = f"design_variation_{i+1}.png"
        new_img.save(save_path)
        variations.append(save_path)

    return variations

# -------------------------------
# 2. Digital Fingerprint + QR Code
# -------------------------------
def generate_fingerprint_and_qr(input_image_path, artisan_name="Vishnu"):
    img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    # ORB keypoints
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(img, None)

    if descriptors is None:
        descriptors = np.zeros((1,32), dtype=np.uint8)

    fingerprint_hash = str(np.sum(descriptors))

    # QR Code
    verification_data = f"Artisan: {artisan_name}\nProduct Hash: {fingerprint_hash}"
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(verification_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color='black', back_color='white')
    qr_path = "product_qr.png"
    qr_img.save(qr_path)

    return fingerprint_hash, qr_path

# -------------------------------
# 3. Upload Image
# -------------------------------
print("Upload your sample pattern image (e.g., Kanchipuram motif):")
uploaded = files.upload()
input_image_path = list(uploaded.keys())[0]

# -------------------------------
# 4. Generate Designs
# -------------------------------
designs = generate_design_variations_color(input_image_path, num_variations=3)
print("Generated design variations:", designs)

# -------------------------------
# 5. Generate Fingerprint + QR
# -------------------------------
hash_value, qr_path = generate_fingerprint_and_qr(input_image_path)
print("Fingerprint Hash:", hash_value)
print("QR Code saved at:", qr_path)

# -------------------------------
# 6. Display Results
# -------------------------------
fig, axs = plt.subplots(1, len(designs), figsize=(12,4))
for i, d in enumerate(designs):
    img = Image.open(d)
    axs[i].imshow(img)
    axs[i].axis("off")
    axs[i].set_title(f"Variation {i+1}")
plt.show()

# Display QR code
qr_img = Image.open(qr_path)
plt.imshow(qr_img)
plt.axis("off")
plt.title("QR Code for Product Verification")
plt.show()

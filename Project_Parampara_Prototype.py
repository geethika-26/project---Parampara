import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt
import qrcode
import random
import os

# -------------------------------
# Utility: Create output folders
# -------------------------------
def setup_output_folders():
    os.makedirs("outputs/designs", exist_ok=True)
    os.makedirs("outputs/qr", exist_ok=True)

# -------------------------------
# 1. Design Variation Generator
# -------------------------------
def generate_design_variations(input_image_path, num_variations=3):
    try:
        img = Image.open(input_image_path).convert("RGB")
    except Exception:
        raise ValueError("❌ Error: Unable to open image. Check file path.")

    variations = []

    for i in range(num_variations):
        img_np = np.array(img).astype(np.float32)

        # Random color shifts
        shifts = np.random.randint(-40, 40, size=3)
        for c in range(3):
            img_np[:, :, c] = np.clip(img_np[:, :, c] + shifts[c], 0, 255)

        new_img = Image.fromarray(img_np.astype('uint8'))

        # Brightness
        brightness_factor = random.uniform(0.8, 1.2)
        new_img = ImageEnhance.Brightness(new_img).enhance(brightness_factor)

        # Contrast
        contrast_factor = random.uniform(0.8, 1.2)
        new_img = ImageEnhance.Contrast(new_img).enhance(contrast_factor)

        # Optional smoothing
        if random.random() > 0.6:
            new_img = new_img.filter(ImageFilter.SMOOTH)

        save_path = f"outputs/designs/design_{i+1}.png"
        new_img.save(save_path)
        variations.append(save_path)

    return variations

# -------------------------------
# 2. Fingerprint + QR Generator
# -------------------------------
def generate_fingerprint_and_qr(input_image_path, artisan_name):
    img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("❌ Error: Invalid image path.")

    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(img, None)

    if descriptors is None:
        descriptors = np.zeros((1, 32), dtype=np.uint8)

    fingerprint_hash = str(np.sum(descriptors))

    # QR data
    qr_data = f"Artisan: {artisan_name}\nHash: {fingerprint_hash}"

    qr = qrcode.make(qr_data)
    qr_path = "outputs/qr/product_qr.png"
    qr.save(qr_path)

    return fingerprint_hash, qr_path

# -------------------------------
# 3. Display Results
# -------------------------------
def display_results(designs, qr_path):
    fig, axs = plt.subplots(1, len(designs), figsize=(12, 4))

    for i, path in enumerate(designs):
        img = Image.open(path)
        axs[i].imshow(img)
        axs[i].axis("off")
        axs[i].set_title(f"Design {i+1}")

    plt.tight_layout()
    plt.show()

    # Show QR
    qr_img = Image.open(qr_path)
    plt.imshow(qr_img)
    plt.axis("off")
    plt.title("QR Code (Product Verification)")
    plt.show()

# -------------------------------
# 4. Main Program
# -------------------------------
def main():
    print("\n=== Project Parampara ===")
    print("AI-based Design Variation + Product Authentication\n")

    input_image = input("Enter image file path: ").strip()
    artisan_name = input("Enter artisan name: ").strip()

    if not os.path.exists(input_image):
        print("❌ File does not exist.")
        return

    setup_output_folders()

    try:
        designs = generate_design_variations(input_image, 3)
        print("\n✅ Design variations created.")

        hash_value, qr_path = generate_fingerprint_and_qr(input_image, artisan_name)
        print("✅ Fingerprint generated.")
        print("Hash:", hash_value)

        display_results(designs, qr_path)

        print("\n📁 Outputs saved in 'outputs/' folder")

    except Exception as e:
        print("❌ Error:", str(e))

# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    main()

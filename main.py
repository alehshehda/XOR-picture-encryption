#SZYFROWANIE OBRAZKU ZA POMOCA XOR

from PIL import Image
import random
import secrets
from skimage.metrics import structural_similarity as ssim
import numpy as np


def calculate_ssim(original_path, decrypted_path):
    original_image = np.array(Image.open(original_path).convert('L'))  # Convert to grayscale
    decrypted_image = np.array(Image.open(decrypted_path).convert('L'))

    ssim_index, _ = ssim(original_image, decrypted_image, full=True)

    return ssim_index


def generate_secure_seed():
    secure_seed = secrets.randbelow(10)  # Ograniczamy zakres do 0-9
    return secure_seed


def generate_key(seed, length):
    random.seed(seed)
    return [random.randint(0, 255) for _ in range(length)]


def encrypt_image(input_path, output_path, seed):
    image = Image.open(input_path)
    width, height = image.size
    key = generate_key(seed, width * height)

    encrypted_image = Image.new(image.mode, (width, height))

    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            encrypted_pixel = tuple(p ^ key[y * width + x] for p in pixel)
            encrypted_image.putpixel((x, y), encrypted_pixel)

    encrypted_image.save(output_path)
    print(f"Image encrypted successfully with seed: {seed}")


def decrypt_image(input_path, output_path, seed):
    encrypted_image = Image.open(input_path)
    width, height = encrypted_image.size
    key = generate_key(seed, width * height)

    decrypted_image = Image.new('RGB', (width, height))

    for y in range(height):
        for x in range(width):
            pixel = encrypted_image.getpixel((x, y))
            decrypted_pixel = tuple(p ^ key[y * width + x] for p in pixel)
            decrypted_image.putpixel((x, y), decrypted_pixel)

    decrypted_image.save(output_path)
    print(f"Image decrypted successfully with seed: {seed}")


def brute_force_decrypt(input_path, output_path, target_seed):
    encrypted_image = Image.open(input_path)
    width, height = encrypted_image.size

    for seed in range(10000):  # Assume a maximum of 10000 seeds
        key = generate_key(seed, width * height)

        decrypted_image = Image.new(encrypted_image.mode, (width, height))

        for y in range(height):
            for x in range(width):
                pixel = encrypted_image.getpixel((x, y))
                decrypted_pixel = tuple(p ^ key[y * width + x] for p in pixel)
                decrypted_image.putpixel((x, y), decrypted_pixel)

        try:
            decrypted_image.verify()
            print(f"Image decrypted successfully with seed: {seed}")
            if seed == target_seed:
                decrypted_image.save(output_path)
                print(f"Image saved with the correct seed: {seed}")
                return
        except Exception as e:
            continue

    print(f"Failed to find the correct seed for decryption.")


if __name__ == "__main__":
    input_image_path = "C:/Users/alehs/Pictures/pythonRes/original.png"
    encrypted_image_path = "C:/Users/alehs/Pictures/pythonRes/encrypted.png"
    decrypted_image_path = "C:/Users/alehs/Pictures/pythonRes/decrypted.png"

    seed = generate_secure_seed()
    print("Wygenerowany bezpieczny seed:", seed)

    # Encrypt image with iterative key
    encrypt_image(input_image_path, encrypted_image_path, seed)

    # Brute-force decrypt image with iterative key
    brute_force_decrypt(encrypted_image_path, decrypted_image_path, seed)

    # Calculate SSIM between original and decrypted images
    ssim_index = calculate_ssim(input_image_path, decrypted_image_path)

    # Set a threshold for SSIM to consider the decrypted image as correct
    ssim_threshold = 0.99

    if ssim_index >= ssim_threshold:
        print("Decrypted image is a correct file.")
    else:
        print("Decrypted image is not a correct file.")
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import numpy as np
import random


# generowanie kluczu
def generate_key(seed, length):
    random.seed(seed)
    return [random.randint(0, 255) for _ in range(length)]


# liczenie SSIM dla porownania dwoch obrazkow na identycznosc
def calculateSSIM(original_path, decrypted_path):
    original_image = np.array(Image.open(original_path).convert('L'))
    decrypted_image = np.array(Image.open(decrypted_path).convert('L'))

    ssim_index, _ = ssim(original_image, decrypted_image, full=True)

    return ssim_index


# proba znaliezenia klucza za pomoca metody brute-force
def bruteForceDecrypt(input_path, output_path, target_seed):
    encrypted_image = Image.open(input_path)
    width, height = encrypted_image.size

    for seed in range(10000):
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


# deszyfrowanie obrazka za pomoca klucza z brute force
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
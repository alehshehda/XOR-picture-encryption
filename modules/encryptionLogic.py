from PIL import Image
import random
import secrets


# generowanie seedu
def generateSecureSeed():
    secure_seed = secrets.randbelow(10)  # Ograniczamy zakres do 0-9
    return secure_seed


# generowanie klucza
def generate_key(seed, length):
    random.seed(seed)
    return [random.randint(0, 255) for _ in range(length)]


# szyfrowanie obrazku za pomoca XOR
def encryptImage(input_path, output_path, seed):
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

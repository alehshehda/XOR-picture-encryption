# SZYFROWANIE OBRAZKA ZA POMOCA XOR

from modules.decryptionLogic import bruteForceDecrypt, calculateSSIM
from modules.encryptionLogic import generateSecureSeed, encryptImage


if __name__ == "__main__":

    inputImage = "C:/Users/alehs/Pictures/pythonRes/original.png"
    encryptedImage = "C:/Users/alehs/Pictures/pythonRes/encrypted.png"
    decryptedImage = "C:/Users/alehs/Pictures/pythonRes/decrypted.png"

    # generowanie seedu oraz wyswietlanie go
    seed = generateSecureSeed()
    print("Wygenerowany bezpieczny seed:", seed)

    # szyfrowanie obrazku
    encryptImage(inputImage, encryptedImage, seed)

    # deszyfracja obrazku za pomoca metody brute force
    bruteForceDecrypt(encryptedImage, decryptedImage, seed)

    # liczenie SSIM index dla porownania identycznosci dwoch obrazkow
    ssimIndex = calculateSSIM(inputImage, decryptedImage)

    # minimalni stopien identycznosci dwoch obrazkow - 99%
    ssimThreshold = 0.99

    if ssimIndex >= ssimThreshold:
        print("Decrypted image is a correct file.")
    else:
        print("Decrypted image is not a correct file.")

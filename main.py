from PIL import Image
import base64
import hashlib
#from Crypto.Cipher import AES
#from Crypto.Random import get_random_bytes

#pip install pillow
#pycryptodome required to use AES.

def encrypt(image, key):
    myimg = image

    for x in range(myimg.width):
        for y in range(myimg.height):
            pixel = myimg.getpixel((x, y))

            coord = (x, y)

            coprime_pixel = ((c+1 if c % 2 == 0 else c) for c in pixel)

            myimg.putpixel(coord, tuple(int(c**43 % 256)
                                        for c in coprime_pixel))

    return myimg

def decrypt(image, key):
    myimg = image

    for x in range(myimg.width):
        for y in range(myimg.height):
            pixel = myimg.getpixel((x, y))
            coord = (x, y)

            myimg.putpixel(coord, tuple(int(c**3 % 256) for c in pixel))

    return myimg

def main():
    print("Pengamanan PNG versi 1.0")

    im = Image.open("sample.png")

    lim = encrypt(im, 100)
    lim.save("encrypted.png")

    print("File encrypted! Now lets decrypt it again.")

    im = Image.open("encrypted.png")

    lim = decrypt(im, 100)
    lim.save("decrypted.png")

    print("File decrypted!")

if __name__ == "__main__":
    main()

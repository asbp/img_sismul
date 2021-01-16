from PIL import Image
import math, random
import numpy as np
import PySimpleGUI as sg

def getperm(l):
    seed = sum(sum(a) for a in l)
    random.seed(seed)
    perm = list(range(len(l)))
    random.shuffle(perm)
    random.seed() # optional, in order to not impact other code based on random
    return perm

def shuffle(l):
    perm = getperm(l)
    return [l[j] for j in perm]

def unshuffle(l):
    perm = getperm(l)
    res = [None] * len(l)
    for i, j in enumerate(perm):
        res[j] = l[i]
    return res

def xor(pixels, key):
    pix_out     = list()
    percent     = 0
    pixels_done = 0
    pix_total   = len(pixels)

    for data in pixels:
        #pixels_done += 1
        #percent = round((pixels_done/pix_total) * 100)
        
        da = tuple((p ^ key) for p in data)
        pix_out.append(da)

        #print("Processing image... "+ str(percent) + "%", end='\r')

    print("\nDone!\n")

    return pix_out

def encrypt(pixels, key):
    pixels = shuffle(pixels)
    pixels = xor(pixels, key)

    return pixels

def decrypt(pixels, key):
    pixels = xor(pixels, key)
    pixels = unshuffle(pixels)

    return pixels

def generate_img(img_mode, w, h, contents, filename):
    print("Creating image in " +img_mode+" mode...")
    img = Image.new(img_mode, (w, h))

    print("Appending image contents...")
    img.putdata(contents)

    print("Saving image...")
    img.save(filename)

    print("Output filename: "+ filename)

    sg.popup("File has been processed.")

def demo():
    key = 253 #max 254

    print("Opening image...")

    im              = Image.open("sample2.png")
    img_mode        = im.mode #Image mode (RGB/RGBA)
    width, height   = im.size
    pixels          = list(im.getdata())
    filetype        = im.format.lower()
    filename_out    = "enc" + "." + filetype

    encrypted_data  = encrypt(pixels, key)

    generate_img(img_mode, width, height, encrypted_data, filename_out)

    #-----

    im              = Image.open(filename_out)
    img_mode        = im.mode #Image mode (RGB/RGBA)
    width, height   = im.size
    pixels          = list(im.getdata())
    filetype        = im.format.lower()
    filename_out    = "dec" + "." + filetype
    
    decrypted_data  = decrypt(pixels, key)

    generate_img(img_mode, width, height, decrypted_data, filename_out)

def chooser_dialog():
    layout = [
          [sg.Radio('Encrypt image', "RADIO1", default=True, key="mode")],
          [sg.Radio('Decrypt image', "RADIO1", default=False)],
          [sg.Button('Select')]
    ]

    window = sg.Window('Please select mode', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event=="Exit":
            break
        else:
            mode = ""

            if(values['mode'] == True):
                mode = "encrypt"
            else:
                mode = "decrypt"

            window.close()
            return mode
    
    window.close()

def browse_file():
    filename = ""

    filename = sg.popup_get_file("Masukkan gambar yang ingin diproses.", 
    file_types = (
        ('PNG File', '*.png'),
        ('JPG File', '*.jpg'),
    ),)

    return filename

def enter_key():
    value = 0
    
    layout = [[sg.Text('Enter number for password (1-255): '), sg.Input(enable_events=True,  key='_INPUT_')],
          [sg.OK()] ]

    window = sg.Window('Enter password', layout)

    while True:
        event, values = window.Read()

        if event in (None, 'Exit'):
            break
        elif event in ("OK"):
            if value not in range(1, 254):
                sg.popup_ok("Please enter number 1-254")
            else:
                break

        if len(values['_INPUT_']) and values['_INPUT_'][-1] not in ('0123456789'):  # if last char entered not a digit
            window.Element('_INPUT_').Update(values['_INPUT_'][:-1])                # delete last char from input
        else:
            value = int(values['_INPUT_'] or "0")

    window.Close()
    return value

def do_encrypt(filename, key):
    sg.popup("Click 'OK' to encrypt image. Please wait until next dialog are shown.")

    im              = Image.open(filename)
    img_mode        = im.mode #Image mode (RGB/RGBA)
    width, height   = im.size
    pixels          = list(im.getdata())
    filetype        = im.format.lower()
    filename_out    = filename + "_enc" + "." + filetype

    encrypted_data  = encrypt(pixels, key)

    generate_img(img_mode, width, height, encrypted_data, filename_out)

def do_decrypt(filename, key):
    sg.popup("Click 'OK' to decrypt image. Please wait until next dialog are shown.")

    im              = Image.open(filename)
    img_mode        = im.mode #Image mode (RGB/RGBA)
    width, height   = im.size
    pixels          = list(im.getdata())
    filetype        = im.format.lower()
    filename_out    = filename + "_dec" + "." + filetype

    data            = decrypt(pixels, key)

    generate_img(img_mode, width, height, data, filename_out)

def main():
    mode = chooser_dialog()
    print(mode + " selected!")

    filename = browse_file()

    if not filename:
        value = sg.popup_yes_no("Filename is empty.\nWish to back to mode dialog?")

        if(value==
        "Yes"):
            main()
        else:
            return

    print("Filename: "+filename)

    xorkey = enter_key()

    if(mode=="encrypt"):
        do_encrypt(filename, xorkey)
    elif(mode=="decrypt"):
        do_decrypt(filename, xorkey)

if __name__ == "__main__":
    main()
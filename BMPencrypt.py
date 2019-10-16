from PIL import Image
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
 

 
def expand_data(data):
    return data + b"\x00"*(16-len(data)%16) 
 

def convert_to_RGB(data):
    pixels = []
    counter = 2

    for i in range(len(data)-1):
        if counter == 2:
            r = int(data[i])
            g = int(data[i+1])
            b = int(data[i+2])

            pixels.append((r,g,b))
            counter = 0
        else:
            counter += 1
    return pixels


def encrypt(input_filename,mode,key):
 
    img_in = Image.open(input_filename)
    data = img_in.convert("RGB").tobytes() 
 
    data_expanded = expand_data(data)

    if mode == "CBC":
        iv = get_random_bytes(16)
        aes = AES.new(key, AES.MODE_CBC, iv)
    elif mode == "ECB":
        aes = AES.new(key, AES.MODE_ECB)
       
    encrypted_data = convert_to_RGB(aes.encrypt(data_expanded)[:len(data)])
    
    img_out = Image.new(img_in.mode, img_in.size)
    img_out.putdata(encrypted_data)
    
    name = ''.join(input_filename.split('.')[:-1])
    img_format = str(input_filename.split('.')[-1])

    output_filename = name + '_' + mode + '_encrypted.' + img_format

    img_out.save(output_filename, img_format)
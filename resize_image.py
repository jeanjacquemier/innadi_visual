from PIL import Image
import os, sys

path = "./images/"
dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            print(im)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((200,200), Image.Resampling.LANCZOS)
            imResize.save(f + ' resized.jpg', 'JPEG', quality=90)
        else:
            print("not found: " + path+item)

if __name__ == '__main__':
    resize()
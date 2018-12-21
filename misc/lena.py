from PIL import Image

def lena():
    old_im = Image.open('misc/rsz_1lena.png').convert('L')
    tuplelist = list(old_im.getdata())
    #arrayresult = [x[0] for x in tuplelist]
    #print(arrayresult)
    return tuplelist

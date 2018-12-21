from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def lena():
    old_im = Image.open('rsz_1lena.png').convert('L')
    tuplelist = list(old_im.getdata())
    #arrayresult = [x[0] for x in tuplelist]
    #print(arrayresult)
    print(tuplelist[:100])
    test = np.reshape(tuplelist, (128,128))
    test = test * -1
    plt.imshow(test, cmap='gray')
    plt.show()

lena()

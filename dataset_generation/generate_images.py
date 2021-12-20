#coding=utf-8
import PIL, cv2, os, random, sys
from PIL import ImageFont, Image, ImageDraw, ImageOps
import numpy as np

random.seed(10)
cwd = os.getcwd() 
def plate_outline(w, h, t = 11, r = 11, inv_border_color = (255,255,255)): 
    #https://stackoverflow.com/questions/60382952/how-to-add-a-round-border-around-an-image/60392932#60392932
    border = cv2.copyMakeBorder(np.full_like(np.zeros((h,w,3),dtype='uint8'), 
    inv_border_color), t, t, t, t, borderType = cv2.BORDER_CONSTANT, value = (0,0,0))
    blur = cv2.GaussianBlur(border, (0,0), r, r)
    thresh1 = cv2.threshold(blur, 128, 255, cv2.THRESH_BINARY)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*t,2*t))
    thresh2 = cv2.morphologyEx(thresh1, cv2.MORPH_ERODE, kernel, iterations=1)
    mask = thresh1 - thresh2
    mask = mask[t:h+t, t:w+t]
    inverted_image = ImageOps.invert(Image.fromarray(mask))
    return inverted_image

def rounded_border(w, h, t = 11, r = 11):
    return plate_outline(w,h,t,r)

def sharp_border(w, h, t):
    return plate_outline(w, h, t, 0.01)

def no_border(w, h):
    return plate_outline(w, h, 1, 0.01)


def col_add(l1, l2):
    c1 = l1.flatten(); c2 = l2.flatten()
    z = list(zip(list(c1), list(c2)))
    retval = []
    for i in range(len(z)):
        x, y = z[i]
        if x == 0 or y == 0:
            retval.append(0)
        elif x == 255 or y == 255:
            retval.append(255)
        else:
            retval.append(0.5*(x+y))
    retval = np.asfarray(retval)
    a, b, c = l1.shape
    retval = retval.reshape(a,b,c)
    return retval.astype('uint8')


def combine_outline(w, h, t = 11, r = 11, plate_color = (255,255,255), type = 'rounded_border'):
    im1 = Image.new(mode = "RGB", size = (w, h), color = plate_color)
    if type == 'rounded_border':
        im2 = rounded_border(w, h, t, r)
    elif type == 'sharp_border':
        im2 = sharp_border(w, h, t)
    elif type == 'no_border':
        im2 = no_border(w, h)
    im1 = np.asfarray(im1) 
    im2 = np.asfarray(im2)
    return Image.fromarray(col_add(im1,im2))

def gen_plate(font_file, text, t = 11, r = 11, font_size = 150, plate_color = (255,255,255), type = 'rounded_border'):
    try :
        font = ImageFont.truetype(font_file, font_size)
    except IOError:
        font = ImageFont.truetype(cwd + '/dataset_generation/fonts/LICENSE_PLATE_USA.ttf', font_size)
    x = font.getsize(text)
    img = combine_outline(x[0] + 50,x[1] + 30, t, r, plate_color, type)
    draw = ImageDraw.Draw(img)
    draw.text((25,15), text, (0,0,0), font = font)
    return img
    

if __name__ == "__main__":
    iter = 0
    sep_list = ['-', '.', ' ', '']
    numString = str(sys.argv[1])
    border_type = ['rounded_border','sharp_border','no_border']
    plate_colors = [(255,255,255), (255,255,0)]
    path = cwd + '/data/PIL-' + numString + '/'
    ITER_LIM = int(sys.argv[1])
    f = open(cwd + "/data/ground_truth_" + numString + ".txt", "w")
    if not os.path.exists(path):
        os.mkdir(path)
    for e in open(cwd + '/dataset_generation/ILP/ILP-' + numString).read().splitlines() :
        if iter >= ITER_LIM:
            break
        iter += 1
        font_file = random.choice(os.listdir(cwd + "/dataset_generation/fonts/"))
        text = e.replace(' ', random.choice(sep_list))
        label = e.replace(' ', '')
        f.write('image_' + str(iter) + '.png' + '\t' + label + '\n')
        plate_color = random.choice(plate_colors)
        type = random.choice(border_type)
        g = gen_plate(font_file = font_file, text = text, plate_color = plate_color, type = type)
        g.save(path + 'image_' + str(iter) + '.png')

    f.close()
	

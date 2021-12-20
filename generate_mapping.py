import PIL, os, random
from PIL import Image
import dataset_generation.generate_images


cwd = os.getcwd()


def expand2square(pil_img):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), (0,0,0))
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), (0,0,0))
        result.paste(pil_img, ((height - width) // 2, 0))
        return result

def gen_plate_with_label(filename, label):
    border_type = ['rounded_border','sharp_border','no_border']
    font_file = random.choice(os.listdir(cwd + "/dataset_generation/fonts/"))
    plate_color = (255,255,255)
    type = random.choice(border_type)
    g = dataset_generation.generate_images.gen_plate(font_file = font_file, text = label, plate_color = plate_color, type = type)
    width, height = g.size
    g = expand2square(g.resize((256, int(256*height/width))))
    return g
    

if __name__ == '__main__':
    
    if not os.path.isdir('ilp_mapped'):
        os.mkdir('ilp_mapped')

    for filename in os.listdir(cwd + '/ilp_base'):
        if filename.endswith('.png'):
            label = filename.split('_')[0]
            g = gen_plate_with_label(filename, label)
            path = cwd + '/ilp_mapped/'
            g.save(path + filename)


from generate_mapping import expand2square, gen_plate_with_label
import PIL, os
from PIL import Image
import numpy as np

cwd = os.getcwd()

def create_pairing_dataset():
    artif_img = []
    orig_img = []
    for filename in os.listdir(cwd + '/ilp_base'):
        if filename.endswith('.png'):
            orig = Image.open(cwd + '/ilp_base/' + filename)
            width, height = orig.size
            orig = expand2square(orig.resize((256, int(256*height/width))))
            artif = gen_plate_with_label(filename, filename.split('_')[0])
            orig_img.append(np.asarray(orig))
            artif_img.append(np.asarray(artif))
         
    return [np.asarray(artif_img), np.asarray(orig_img)]

def create_np_dataset():
    artif, orig = create_pairing_dataset()
    print('Loaded: ', artif.shape, orig.shape)
    filename = 'LP_256.npz'
    np.savez_compressed(cwd + '/np_dataset/' + filename, artif, orig)
    print('Saved dataset: ', filename)


if __name__ == '__main__':
    if not os.path.isdir('np_dataset'):
        os.mkdir('np_dataset')
    create_np_dataset()

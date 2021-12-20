import random, os 
random.seed(10)
cwd = os.getcwd()
if __name__ == "__main__":
    iter = 0
    numString = str(sys.argv[1])
    path = cwd + '/data/PIL-' + numString + '/'
    ITER_LIM = int(sys.argv[1])
    for e in open(cwd + '/dataset_generation/ILP/ILP-' + numString).read().splitlines() :
        if iter >= ITER_LIM:
            break
        iter += 1
        f.write('image_' + str(iter) + '.png' + '\t' + label + '\n')
    f.close()



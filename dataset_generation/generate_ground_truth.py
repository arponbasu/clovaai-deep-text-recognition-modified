import random, os, sys 
random.seed(10)
cwd = os.getcwd()
if __name__ == "__main__":
    iter = 0
    numString = str(sys.argv[1])
    path = cwd + '/data/PIL-' + numString + '/'
    ITER_LIM = int(sys.argv[1])
    f = open(cwd + "/data/ground_truth_" + numString + ".txt", "w")
    for e in open(cwd + '/dataset_generation/ILP/ILP-' + numString).read().splitlines() :
        if iter >= ITER_LIM:
            break
        iter += 1
        label = e.replace(' ', '')
        f.write('image_' + str(iter) + '.png' + '\t' + label + '\n')
    f.close()



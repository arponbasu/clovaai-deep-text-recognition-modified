from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import random, os, sys


random.seed(10)

def readFile(fileName):
  fileObj = open(fileName, "r") 
  words = fileObj.read().splitlines() 
  fileObj.close()
  return words

def random_shuffle(arr):
  return random.sample(arr, len(arr))

def random_choice(arr):
  return random.choice(arr)
cwd = os.getcwd()
arr_1  = random_shuffle(readFile(cwd + "/dataset_generation/ILP/ILP-1"))
arr_21 = random_shuffle(readFile(cwd + "/dataset_generation/ILP/ILP-2.1"))
arr_22 = random_shuffle(readFile(cwd + "/dataset_generation/ILP/ILP-2.2"))
arr_31 = random_shuffle(readFile(cwd + "/dataset_generation/ILP/ILP-3.1"))
arr_32 = random_shuffle(readFile(cwd + "/dataset_generation/ILP/ILP-3.2"))
arr_33 = random_shuffle(readFile(cwd + "/dataset_generation/ILP/ILP-3.3"))
arr_41 = random_shuffle(readFile(cwd + "/dataset_generation/ILP/ILP-4.1"))
arr_42 = random_shuffle(readFile(cwd + "/dataset_generation/ILP/ILP-4.2"))
arr_43 = random_shuffle(readFile(cwd + "/dataset_generation/ILP/ILP-4.3"))
arr_44 = random_shuffle(readFile(cwd + "/dataset_generation/ILP/ILP-4.4"))

def generate_license_plate():
  retval = ""
  retval += random_choice(arr_1) + ' '

  if random.randint(1,2) == 1:
    retval += random_choice(arr_21) + ' '
  else:
    retval += random_choice(arr_22) + ' '
  rnd_3 = random.randint(1,3)
  if rnd_3 == 1:
    retval += random_choice(arr_31) + ' '
  elif rnd_3 == 2:
    retval += random_choice(arr_32) + ' '
  else:
    retval += random_choice(arr_33) + ' '
  rnd_4 = random.randint(1,4)
  if rnd_4 == 1:
    retval += random_choice(arr_41) 
  elif rnd_4 == 2:
    retval += random_choice(arr_42) 
  elif rnd_4 == 3:
    retval += random_choice(arr_43) 
  else:
    retval += random_choice(arr_44) 

  
  return retval
#print(generate_license_plate())

if __name__ == "__main__":
  if len(sys.argv) != 2:
    rng = 25000
  else:
    rng = int(sys.argv[1])
  f = open(cwd + "/dataset_generation/ILP/ILP-" + str(rng), "w")
  content = ""
  for i in range(rng):
    content += generate_license_plate() + '\n'
  f.write(content)
  f.close()





  

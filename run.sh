#!/bin/bash
echo "Installing packages ..."
pip3 install -r requirements.txt
echo "Package installment complete"
echo "Installing fonts; Requires sudo privileges ..."
sudo cp -u dataset_generation/fonts/ /usr/local/share/fonts/
echo "Font installation complete"
read -p "Enter the number of images in your dataset: " numImages
ILPFILE="dataset_generation/ILP/ILP-${numImages}"
echo "Searching for ILP file ..."
if [ -f "$ILPFILE" ]; then
    echo "ILP-${numImages} already exists..."
else 
    echo "Generating $ILPFILE ..."
	python3 dataset_generation/generate_dataset.py "$numImages"
	echo "ILP file generated ..."
fi
mkdir -p data
GTFILE="data/ground_truth_${numImages}.txt"
if [ ! -f "$GTFILE" ]; then
	touch "$GTFILE"
fi
PILDIR="data/PIL-${numImages}"
if [ ! -d "$PILDIR" ];
then 
	echo "Generating images ... This may take quite some time"
	python3 dataset_generation/generate_images.py "$numImages" 
	echo "Image generation is complete"
else
	echo "Your image directory already exists"
fi
echo "creating lmdb dataset, ensure that the data directory contains exactly one text file"
INPUTDIR="data/PIL-${numImages}"
python3 create_lmdb_dataset.py --inputPath "$INPUTDIR" --gtFile data/*.txt --outputPath result/
echo "lmdb dataset created"
read -p "Enter the number of iterations for training (default is 4000): " num_iter
echo "Your GPU details ..."
nvidia-smi
echo "Beginning training ..."
python3 train.py \
--train_data result/ --valid_data result/ \
--select_data '/' --batch_ratio 1.0 --num_iter "$num_iter" \
--Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn \
--character '0123456789ABCDEFGHIJKLMNOPQRSTVWXYZ'  \
--sensitive --saved_model 'default_model/TPS-ResNet-BiLSTM-Attn.pth' 
echo "Testing models against real life images"









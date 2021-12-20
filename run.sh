#!/bin/bash
echo "Installing packages ..."
pip install -r requirements.txt
echo "Package installment complete"
echo "Installing fonts; Requires sudo privileges ..."
sudo cp -u dataset_generation/fonts/ /usr/local/share/fonts/
echo "Font installation complete"
read -t 10 -p "Enter the number of images in your dataset (it will be set to 5000 automatically after 10 seconds): " numImages    
: ${numImages:=5000}        
echo "The number of images has been set to $numImages"
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
	python3 dataset_generation/generate_ground_truth.py "$numImages"
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
echo "creating lmdb dataset ..."
python3 create_lmdb_dataset.py --inputPath "$PILDIR" --gtFile "$GTFILE" --outputPath result/
echo "lmdb dataset created"
echo "Your GPU details ..."
nvidia-smi -L
read -t 10 -p "Enter the number of iterations for training (it will be set to 4000 automatically after 10 seconds): " num_iter 
: ${num_iter:=4000}
echo "The number of iterations has been set to $num_iter"        
read -t 10 -p "Enter the path of your starting model (it will be set to default_model/TPS-ResNet-BiLSTM-Attn.pth automatically after 10 seconds): " DEFAULT_MODEL 
: ${DEFAULT_MODEL:=default_model/TPS-ResNet-BiLSTM-Attn.pth}
echo "Beginning training ..."
python3 train.py \
--train_data result/ --valid_data result/ \
--select_data '/' --batch_ratio 1.0 --num_iter "$num_iter" \
--Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn \
--character '0123456789ABCDEFGHIJKLMNOPQRSTVWXYZ'  \
--sensitive --saved_model "$DEFAULT_MODEL" 
echo "Testing models against real life images"
for filename in saved_models/TPS-ResNet-BiLSTM-Attn-Seed1111/*.pth; do
    python3 demo.py \
	--Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn \
	--image_folder test_images/ \
	--saved_model "$file_name"
done








import os
from raindrop.dropgenerator import generateDrops
from raindrop.config import cfg

from PIL import Image
import numpy as np
import cv2

def main():
	# Updated paths for the new project structure
	image_folder_path = "./datasets"
	outputimg_folder_path = "./Output_image"
	outputlabel_folder_path = "./Output_label"
	
	# Create output directories if they don't exist
	os.makedirs(outputimg_folder_path, exist_ok=True)
	os.makedirs(outputlabel_folder_path, exist_ok=True)
	
	# using predefined label
	# input_label = Image.open("test.png")
	
	# Check if datasets directory exists
	if not os.path.exists(image_folder_path):
		print(f"Warning: {image_folder_path} not found. Please add images to the datasets directory.")
		return
	
	for file_name in os.listdir(image_folder_path):
		# Skip non-image files
		if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
			continue
			
		image_path = os.path.join(image_folder_path, file_name)
		print(f"Processing: {file_name}")
		
		try:
			# Enable label output
			cfg["return_label"] = True
			
			# Generate both image and label
			output_image, output_label = generateDrops(image_path, cfg)
			
			# Save processed image
			save_path = os.path.join(outputimg_folder_path, file_name)
			output_image.save(save_path)
			print(f"Saved image: {save_path}")
			
			# Save label map
			label_save_path = os.path.join(outputlabel_folder_path, file_name)
			# Convert label to proper format for saving
			output_label_array = np.array(output_label)
			# Multiply by 255 to make labels visible (0 -> 0, 1 -> 255)
			cv2.imwrite(label_save_path, output_label_array * 255)
			print(f"Saved label: {label_save_path}")
			
		except Exception as e:
			print(f"Error processing {file_name}: {str(e)}")

if __name__ == "__main__":
	main()
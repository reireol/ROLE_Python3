"""
MMPose custom transform for raindrop augmentation
"""
import random
import numpy as np
import tempfile
import os
from PIL import Image
from mmcv.transforms import BaseTransform
from mmpose.registry import TRANSFORMS

# Import ROLE raindrop generation from project
import sys
import os.path as osp
# Add the parent directory to Python path to enable relative import
current_dir = osp.dirname(osp.abspath(__file__))
parent_dir = osp.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from raindrop.dropgenerator import generateDrops


@TRANSFORMS.register_module()
class RaindropAugmentation(BaseTransform):
    """
    Raindrop augmentation transform for MMPose training pipeline.
    
    This transform applies realistic raindrop effects to training images
    to improve model robustness in adverse weather conditions.
    
    Args:
        probability (float): Probability of applying raindrop effect (0.0-1.0).
        raindrop_config (dict): Configuration for raindrop generation.
        temp_dir (str): Temporary directory for intermediate files.
    """
    
    def __init__(self, probability=0.4, raindrop_config=None, temp_dir='/tmp'):
        super().__init__()
        self.probability = probability
        self.temp_dir = temp_dir
        
        # Default raindrop configuration optimized for pose estimation
        self.default_config = {
            'maxR': 25,              # Maximum droplet radius (moderate size)
            'minR': 15,              # Minimum droplet radius
            'maxDrops': 15,          # Maximum number of droplets
            'minDrops': 5,           # Minimum number of droplets
            'edge_darkratio': 0.2,   # Edge darkening ratio (subtle)
            'return_label': False,   # Only return augmented image
            'label_thres': 128,      # Label threshold
            'shape_variety': True,   # Enable shape variety
            'allowed_shapes': ['default', 'round', 'oval', 'teardrop']  # Exclude irregular/splash
        }
        
        # Merge with provided config
        if raindrop_config is not None:
            self.raindrop_config = {**self.default_config, **raindrop_config}
        else:
            self.raindrop_config = self.default_config
            
        # Ensure temp directory exists
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def transform(self, results):
        """
        Apply raindrop augmentation to the input image.
        
        Args:
            results (dict): Data dict containing image and annotations.
            
        Returns:
            dict: Data dict with augmented image.
        """
        # Skip augmentation based on probability
        if random.random() > self.probability:
            return results
            
        try:
            # Get image from results
            img = results['img']  # numpy array in BGR format
            
            # Convert BGR to RGB for PIL
            img_rgb = img[:, :, ::-1]  # BGR -> RGB
            
            # Convert to PIL Image
            img_pil = Image.fromarray(img_rgb.astype(np.uint8))
            
            # Apply raindrop effect using temporary file approach
            augmented_img = self._apply_raindrop_effect(img_pil)
            
            # Convert back to numpy array in BGR format
            augmented_array = np.array(augmented_img)
            augmented_bgr = augmented_array[:, :, ::-1]  # RGB -> BGR
            
            # Update results
            results['img'] = augmented_bgr.astype(img.dtype)
            
        except Exception as e:
            # If raindrop generation fails, return original image
            pass
            
        return results
    
    def _apply_raindrop_effect(self, img_pil):
        """
        Apply raindrop effect using ROLE library.
        
        Args:
            img_pil (PIL.Image): Input PIL image.
            
        Returns:
            PIL.Image: Augmented image with raindrop effect.
        """
        # Create temporary file for input
        with tempfile.NamedTemporaryFile(suffix='.jpg', dir=self.temp_dir, delete=False) as temp_file:
            temp_path = temp_file.name
            
        try:
            # Save PIL image to temporary file
            img_pil.save(temp_path, 'JPEG')
            
            # Apply raindrop effect
            augmented_img = generateDrops(temp_path, self.raindrop_config)
            
            return augmented_img
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def __repr__(self):
        repr_str = (f'{self.__class__.__name__}('
                   f'probability={self.probability}, '
                   f'raindrop_config={self.raindrop_config})')
        return repr_str


@TRANSFORMS.register_module()
class RaindropAugmentationStage1(RaindropAugmentation):
    """
    Raindrop augmentation specifically for Stage 1 training.
    
    This variant uses stronger augmentation parameters suitable for
    the initial training phase.
    """
    
    def __init__(self, probability=0.4, temp_dir='/tmp'):
        # Stage 1 specific configuration
        stage1_config = {
            'maxR': 25,
            'minR': 15,
            'maxDrops': 15,
            'minDrops': 5,
            'edge_darkratio': 0.25,  # Slightly stronger for stage 1
            'shape_variety': True,
            'allowed_shapes': ['default', 'round', 'oval', 'teardrop']
        }
        
        super().__init__(probability=probability, 
                        raindrop_config=stage1_config,
                        temp_dir=temp_dir)


# Register the transforms
__all__ = ['RaindropAugmentation', 'RaindropAugmentationStage1']
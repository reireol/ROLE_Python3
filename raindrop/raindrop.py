import cv2
import math
import numpy as np
import random
from PIL import Image, ImageFilter


class raindrop():
	def __init__(self, key, centerxy = None, radius = None, input_alpha = None, input_label = None, droplet_type = None):
		if input_label is None:
			self.key = key		
			self.ifcol = False	
			self.col_with = []
			self.center = centerxy
			self.radius = radius
			# Random droplet type if not specified
			if droplet_type is None:
				self.type = random.choice(["default", "round", "oval", "teardrop", "irregular", "splash"])
			else:
				self.type = droplet_type
			# label map's WxH = 4*R , 5*R
			self.labelmap = np.zeros((self.radius * 5, self.radius*4))
			self.alphamap = np.zeros((self.radius * 5, self.radius*4))
			self.background = None
			self.texture = None
			self._create_label()
			self.use_label = False
		else:
			self.key = key
			assert input_alpha is not None, "Please also input the alpha map"
			self.alphamap = input_alpha
			self.labelmap =input_label
			self.ifcol = False
			self.col_with = []
			# default shape should be [h,w]			
			h, w = self.labelmap.shape
			# set the label center
			self.center = centerxy
			self.radius = min(w//4, h//4)
			self.background = None
			self.texture = None
			self.use_label = True

	def setCollision(self, col, col_with):
		self.ifcol = col
		self.col_with = col_with

	def updateTexture(self, bg):		
		# Replace pyblur.GaussianBlur with PIL ImageFilter.GaussianBlur
		fg = Image.fromarray(np.uint8(bg)).filter(ImageFilter.GaussianBlur(radius=5))
		fg = np.asarray(fg)
		

		# Ensure background has proper dimensions for camera matrix
		h, w = fg.shape[:2]
		
		K = np.array([[30*self.radius, 0, w/2],
				[0., 20*self.radius, h/2],
				[0., 0., 1]], dtype=np.float64)
		D = np.array([0.0, 0.0, 0.0, 0.0], dtype=np.float64)
		Knew = K.copy()
		scale_factor = math.pow(self.radius, 1/3)*2
		Knew[0,0] = K[0,0] * scale_factor
		Knew[1,1] = K[1,1] * scale_factor
		
		# Ensure proper data types for OpenCV fisheye
		try:
			fisheye = cv2.fisheye.undistortImage(fg, K, D=D, Knew=Knew)
		except Exception as e:
			# Fallback: use regular undistortion if fisheye fails
			print(f"Fisheye distortion failed: {e}, using original image")
			fisheye = fg.copy()
		

		target_height, target_width = self.alphamap.shape
		if fisheye.shape[:2] != (target_height, target_width):
			fisheye = cv2.resize(fisheye, (target_width, target_height))
		
		# Ensure alphamap is in correct format
		alpha_channel = self.alphamap.astype(np.uint8)
		tmp = np.expand_dims(alpha_channel, axis = -1)		
		tmp = np.concatenate((fisheye, tmp), axis = 2)
		
		self.texture = Image.fromarray(tmp.astype('uint8'), 'RGBA')
		self.texture = self.texture.transpose(Image.FLIP_TOP_BOTTOM)


		
	# create the raindrop label
	def _create_label(self):
		if self.type == "default":
			self._createDefaultDrop()
		elif self.type == "round":
			self._createRoundDrop()
		elif self.type == "oval":
			self._createOvalDrop()
		elif self.type == "teardrop":
			self._createTeardropDrop()
		elif self.type == "irregular":
			self._createIrregularDrop()
		elif self.type == "splash":
			self._createSplashDrop()
		else:
			# Fallback to default
			self._createDefaultDrop()

	def _createDefaultDrop(self):
		"""Original teardrop shape (circle + ellipse)"""
		cv2.circle(self.labelmap, (self.radius * 2, self.radius * 3), self.radius, 128, -1)
		cv2.ellipse(self.labelmap, (self.radius * 2, self.radius * 3), (self.radius, int(1.3*math.sqrt(3) * self.radius)), 0, 180, 360, 128, -1)		
		self._apply_alpha_map()

	def _createRoundDrop(self):
		"""Perfect circular droplet"""
		cv2.circle(self.labelmap, (self.radius * 2, self.radius * 2), self.radius, 128, -1)
		# Apply alpha mapping
		self._apply_alpha_map()

	def _createOvalDrop(self):
		"""Oval-shaped droplet with random orientation"""
		angle = random.randint(0, 180)
		aspect_ratio = random.uniform(1.2, 2.0)
		axes = (self.radius, int(self.radius * aspect_ratio))
		cv2.ellipse(self.labelmap, (self.radius * 2, self.radius * 2), axes, angle, 0, 360, 128, -1)
		self._apply_alpha_map()

	def _createTeardropDrop(self):
		"""Enhanced teardrop with random variation"""
		# Main circle
		cv2.circle(self.labelmap, (self.radius * 2, self.radius * 3), self.radius, 128, -1)
		# Variable ellipse for teardrop effect
		ellipse_ratio = random.uniform(1.1, 1.5)
		angle_variation = random.randint(-15, 15)
		cv2.ellipse(self.labelmap, (self.radius * 2, self.radius * 3), 
		           (self.radius, int(ellipse_ratio * math.sqrt(3) * self.radius)), 
		           angle_variation, 180, 360, 128, -1)
		self._apply_alpha_map()

	def _createIrregularDrop(self):
		"""Irregular droplet with random distortions"""
		# Start with basic circle
		center = (self.radius * 2, self.radius * 2)
		
		# Create irregular shape using multiple overlapping circles
		num_perturbations = random.randint(3, 6)
		for i in range(num_perturbations):
			# Random offset from center
			offset_x = random.randint(-self.radius//3, self.radius//3)
			offset_y = random.randint(-self.radius//3, self.radius//3)
			perturb_radius = random.randint(self.radius//2, int(self.radius * 0.8))
			
			perturb_center = (center[0] + offset_x, center[1] + offset_y)
			cv2.circle(self.labelmap, perturb_center, perturb_radius, 128, -1)
		
		self._apply_alpha_map()

	def _createSplashDrop(self):
		"""Splash-like droplet with multiple small circles"""
		# Main droplet
		main_radius = int(self.radius * 0.7)
		cv2.circle(self.labelmap, (self.radius * 2, self.radius * 2), main_radius, 128, -1)
		
		# Add satellite droplets
		num_satellites = random.randint(2, 5)
		for i in range(num_satellites):
			# Random position around main droplet
			angle = random.uniform(0, 2 * math.pi)
			distance = random.randint(main_radius, int(self.radius * 1.5))
			sat_x = int(self.radius * 2 + distance * math.cos(angle))
			sat_y = int(self.radius * 2 + distance * math.sin(angle))
			sat_radius = random.randint(self.radius//4, self.radius//2)
			
			# Ensure within bounds
			if (0 <= sat_x < self.labelmap.shape[1] and 0 <= sat_y < self.labelmap.shape[0]):
				cv2.circle(self.labelmap, (sat_x, sat_y), sat_radius, 128, -1)
		
		self._apply_alpha_map()

	def _apply_alpha_map(self):
		"""Common alpha map application for all droplet types"""
		# Apply random blur intensity for variation
		blur_radius = random.randint(8, 12)
		self.alphamap = Image.fromarray(np.uint8(self.labelmap)).filter(ImageFilter.GaussianBlur(radius=blur_radius))
		self.alphamap = np.asarray(self.alphamap).astype(np.float64)
		# Ensure alphamap has proper values
		if np.max(self.alphamap) > 0:
			self.alphamap = self.alphamap/np.max(self.alphamap)*255.0
		else:
			self.alphamap = np.zeros_like(self.alphamap)
		# set label map
		self.labelmap[self.labelmap>0] = 1

	def setKey(self, key):
		self.key = key

	def getLabelMap(self):
		return self.labelmap

	def getAlphaMap(self):
		return self.alphamap

	def getTexture(self):
		return self.texture

	def getCenters(self):
		return self.center
		
	def getRadius(self):
		return self.radius

	def getKey(self):
		return self.key

	def getIfColli(self):
		return self.ifcol

	def getCollisionList(self):
		return self.col_with
	
	def getUseLabel(self):
		return self.use_label
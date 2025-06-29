# Setup Guide

This guide will help you set up the ROLE Python 3.11 environment from scratch.

## System Requirements

### Operating System
- Linux (Ubuntu 18.04+, CentOS 7+)
- macOS (10.14+)
- Windows 10/11 (with WSL recommended)

### Hardware Requirements
- **Minimum**: 4GB RAM, 2GB free disk space
- **Recommended**: 8GB+ RAM, 5GB free disk space
- **GPU**: Optional (not currently utilized)

## Installation Methods

### Method 1: Anaconda (Recommended)

Anaconda provides the most reliable environment management for scientific Python packages.

#### 1. Install Anaconda

Download and install Anaconda from https://www.anaconda.com/products/distribution

#### 2. Create Environment

```bash
# Create new environment with Python 3.11
conda create -n role_python3 python=3.11

# Activate environment
conda activate role_python3
```

#### 3. Clone Repository

```bash
git clone https://github.com/yourusername/ROLE_python3.git
cd ROLE_python3
```

#### 4. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python -c "import cv2, PIL, numpy, skimage; print('All dependencies installed successfully')"
```

### Method 2: Virtual Environment (venv)

For users who prefer Python's built-in virtual environment.

#### 1. Install Python 3.11

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

**macOS (with Homebrew):**
```bash
brew install python@3.11
```

**Windows:**
Download Python 3.11 from https://www.python.org/downloads/

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv role_env

# Activate environment
# Linux/macOS:
source role_env/bin/activate
# Windows:
role_env\Scripts\activate
```

#### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install packages
pip install -r requirements.txt
```

### Method 3: Docker (Advanced)

For containerized deployment.

#### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run example
CMD ["python", "example.py"]
```

#### 2. Build and Run

```bash
# Build image
docker build -t role_python3 .

# Run container
docker run -v $(pwd)/datasets:/app/datasets -v $(pwd)/Output_image:/app/Output_image role_python3
```

## Verification

### Basic Functionality Test

```bash
# Test basic import
python -c "from raindrop.dropgenerator import generateDrops; from raindrop.config import cfg; print('✅ Import successful')"

# Test with sample image (if available)
python -c "
import os
from raindrop.dropgenerator import generateDrops
from raindrop.config import cfg

if os.path.exists('datasets/'):
    files = [f for f in os.listdir('datasets/') if f.lower().endswith(('.jpg', '.png'))]
    if files:
        try:
            output = generateDrops(f'datasets/{files[0]}', cfg)
            print('✅ Processing test passed')
        except Exception as e:
            print(f'❌ Processing failed: {e}')
    else:
        print('⚠️  No test images found in datasets/')
else:
    print('⚠️  datasets/ directory not found')
"
```

### Performance Test

```bash
# Time a sample operation
python -c "
import time
from raindrop.dropgenerator import generateDrops
from raindrop.config import cfg
from PIL import Image
import numpy as np

# Create test image
test_img = Image.fromarray(np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8))
test_img.save('test_input.jpg')

start_time = time.time()
output = generateDrops('test_input.jpg', cfg)
end_time = time.time()

print(f'✅ Processing time: {end_time - start_time:.2f} seconds')

# Cleanup
import os
os.remove('test_input.jpg')
"
```

## Troubleshooting Setup Issues

### Common Problems

#### 1. OpenCV Installation Issues

**Error**: `ImportError: No module named 'cv2'`

**Solutions**:
```bash
# Method 1: pip
pip install opencv-python

# Method 2: conda
conda install opencv

# Method 3: System package (Ubuntu)
sudo apt install python3-opencv
```

#### 2. NumPy Compatibility

**Error**: `AttributeError: module 'numpy' has no attribute 'float'`

**Solution**:
```bash
# Ensure NumPy 1.21.0+
pip install "numpy>=1.21.0"
```

#### 3. Pillow Installation

**Error**: `PIL/Pillow installation failed`

**Solutions**:
```bash
# Install system dependencies (Ubuntu)
sudo apt install python3-dev libjpeg-dev zlib1g-dev

# Reinstall Pillow
pip uninstall pillow
pip install pillow
```

#### 4. scikit-image Issues

**Error**: `ImportError: cannot import name 'label' from 'skimage.measure'`

**Solution**:
```bash
# Install specific version
pip install "scikit-image>=0.19.0"
```

#### 5. Memory Issues

**Error**: `MemoryError` or system slowdown

**Solutions**:
- Use smaller test images initially
- Reduce droplet count in config
- Close other applications
- Consider upgrading RAM

### Platform-Specific Issues

#### Windows

**Long path issues**:
```bash
# Enable long paths in Git
git config --system core.longpaths true
```

**Visual C++ requirements**:
- Install Microsoft Visual C++ Redistributable
- Or use conda instead of pip for compiled packages

#### macOS

**Xcode Command Line Tools**:
```bash
xcode-select --install
```

**Homebrew conflicts**:
```bash
# Use isolated environment
conda create -n role_python3 python=3.11
```

#### Linux

**System package conflicts**:
```bash
# Use virtual environment to avoid conflicts
python3.11 -m venv --system-site-packages role_env
```

## Advanced Configuration

### Development Setup

For contributors and developers:

```bash
# Clone with development dependencies
git clone https://github.com/yourusername/ROLE_python3.git
cd ROLE_python3

# Install in development mode
pip install -e .

# Install development tools
pip install pytest black flake8 mypy
```

### Production Setup

For production deployments:

```bash
# Install only runtime dependencies
pip install --no-dev -r requirements.txt

# Set environment variables
export PYTHONPATH="/path/to/ROLE_python3:$PYTHONPATH"

# Run with optimizations
python -O example.py
```

### GPU Acceleration (Experimental)

```bash
# Install OpenCV with CUDA support
pip uninstall opencv-python
pip install opencv-contrib-python

# Verify CUDA
python -c "import cv2; print('CUDA devices:', cv2.cuda.getCudaEnabledDeviceCount())"
```

## Next Steps

After successful setup:

1. **Run Examples**: Try `python example.py`
2. **Read Documentation**: Check `docs/` folder
3. **Experiment**: Modify `raindrop/config.py`
4. **Contribute**: See contribution guidelines

## Support

If you encounter issues not covered here:

1. Check the [Troubleshooting section](README.md#troubleshooting) in README
2. Search [GitHub Issues](https://github.com/yourusername/ROLE_python3/issues)
3. Create a new issue with:
   - Your OS and Python version
   - Complete error messages
   - Steps to reproduce
   - Output of `pip list`

---

**Happy coding!** 🌧️
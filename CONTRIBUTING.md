# Contributing to ROLE Python 3.11

Thank you for your interest in contributing to the ROLE project! This document provides guidelines and information for contributors.

## 🌟 Ways to Contribute

- 🐛 **Bug Reports**: Help us identify and fix issues
- 💡 **Feature Requests**: Suggest new functionality
- 📝 **Documentation**: Improve guides, examples, and API docs
- 🔧 **Code Contributions**: Fix bugs, add features, optimize performance
- 🧪 **Testing**: Add test cases, improve test coverage
- 🎨 **Examples**: Create tutorials, sample applications

## 🚀 Getting Started

### 1. Development Environment Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/ROLE_python3.git
cd ROLE_python3

# Create development environment
conda create -n role_dev python=3.11
conda activate role_dev

# Install dependencies and development tools
pip install -r requirements.txt
pip install pytest black flake8 mypy pre-commit

# Install pre-commit hooks
pre-commit install
```

### 2. Development Workflow

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make changes and test
python example.py  # Test basic functionality
pytest tests/     # Run test suite (when available)

# Format and lint code
black raindrop/
flake8 raindrop/

# Commit changes
git add .
git commit -m "Add: your feature description"

# Push and create pull request
git push origin feature/your-feature-name
```

## 📝 Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some project-specific conventions:

#### Code Formatting
```python
# Use Black for automatic formatting
black raindrop/ example.py

# Configuration in pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']
```

#### Naming Conventions
```python
# Classes: PascalCase
class RaindropGenerator:
    pass

# Functions and variables: snake_case
def generate_drops(image_path, config):
    max_radius = config['maxR']
    return processed_image

# Constants: UPPER_SNAKE_CASE
MAX_DROPLET_SIZE = 200
DEFAULT_CONFIG_PATH = "config.py"

# Private methods: _leading_underscore
def _create_alpha_map(self):
    pass
```

#### Type Hints (Encouraged)
```python
from typing import Tuple, Optional, Union
from PIL import Image
import numpy as np

def generateDrops(
    imagePath: str, 
    cfg: dict, 
    inputLabel: Optional[Image.Image] = None
) -> Union[Image.Image, Tuple[Image.Image, Image.Image]]:
    """Generate raindrop effects with type hints."""
    pass
```

### Documentation Standards

#### Docstrings
```python
def generate_drops(image_path: str, config: dict) -> Image.Image:
    """
    Generate realistic raindrop effects on an image.
    
    This function applies water droplet simulation with configurable
    parameters including size, count, and optical effects.
    
    Args:
        image_path: Path to the input image file
        config: Dictionary containing droplet generation parameters
            - maxR: Maximum droplet radius in pixels
            - minR: Minimum droplet radius in pixels
            - maxDrops: Maximum number of droplets
            - minDrops: Minimum number of droplets
            
    Returns:
        PIL Image with raindrop effects applied
        
    Raises:
        FileNotFoundError: If image_path does not exist
        ValueError: If config parameters are invalid
        
    Example:
        >>> from raindrop.config import cfg
        >>> result = generate_drops('input.jpg', cfg)
        >>> result.save('output.jpg')
    """
    pass
```

#### Code Comments
```python
# Good: Explain WHY, not WHAT
def _apply_fisheye_distortion(self, image):
    # Use fisheye model to simulate light refraction through water droplet
    # This creates the characteristic magnification effect seen in real raindrops
    K = self._calculate_camera_matrix()
    return cv2.fisheye.undistortImage(image, K, D, Knew)

# Avoid: Obvious comments
# Bad: Add 1 to counter
counter += 1
```

## 🧪 Testing Guidelines

### Test Structure
```bash
tests/
├── test_raindrop.py      # Unit tests for raindrop class
├── test_dropgenerator.py # Tests for main generation function
├── test_config.py        # Configuration validation tests
├── test_integration.py   # End-to-end integration tests
└── fixtures/             # Test images and data
    ├── sample_input.jpg
    └── expected_output.jpg
```

### Writing Tests
```python
import pytest
from PIL import Image
import numpy as np
from raindrop.dropgenerator import generateDrops
from raindrop.config import cfg

class TestDropGeneration:
    def test_basic_generation(self):
        """Test basic droplet generation functionality."""
        # Create test image
        test_image = Image.fromarray(
            np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        )
        test_path = 'test_input.jpg'
        test_image.save(test_path)
        
        try:
            # Test generation
            result = generateDrops(test_path, cfg)
            assert isinstance(result, Image.Image)
            assert result.size == test_image.size
        finally:
            os.remove(test_path)
    
    def test_invalid_config(self):
        """Test handling of invalid configuration."""
        invalid_cfg = cfg.copy()
        invalid_cfg['maxR'] = -10  # Invalid radius
        
        with pytest.raises(ValueError):
            generateDrops('test.jpg', invalid_cfg)
            
    @pytest.mark.parametrize("droplet_count", [5, 15, 30, 50])
    def test_droplet_counts(self, droplet_count):
        """Test various droplet count configurations."""
        test_cfg = cfg.copy()
        test_cfg.update({
            'maxDrops': droplet_count,
            'minDrops': droplet_count
        })
        # Test implementation...
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=raindrop

# Run specific test file
pytest tests/test_dropgenerator.py

# Run with verbose output
pytest -v

# Run performance tests
pytest tests/test_performance.py --benchmark-only
```

## 📋 Issue Guidelines

### Bug Reports

Please include:

```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Create image with dimensions X
2. Set config parameters Y
3. Run generateDrops()
4. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Python Version: [e.g., 3.11.2]
- Package Versions: [run `pip list`]

**Additional Context**
- Sample images (if relevant)
- Error messages (full traceback)
- Configuration used
```

### Feature Requests

```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Use Case**
Describe the problem this feature would solve.

**Proposed Solution**
How you envision this feature working.

**Alternatives**
Any alternative solutions you've considered.

**Additional Context**
Any other relevant information or examples.
```

## 🔀 Pull Request Process

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated (if applicable)
- [ ] CHANGELOG.md updated (for significant changes)
- [ ] No merge conflicts with main branch

### PR Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Existing tests pass
- [ ] New tests added for new functionality
- [ ] Manually tested with sample images

## Screenshots/Examples
If applicable, add screenshots or example outputs.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and linting
2. **Code Review**: Project maintainers review the code
3. **Testing**: Manual testing with various image types
4. **Approval**: At least one maintainer approval required
5. **Merge**: Squash and merge to main branch

## 🌐 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Assume good intentions
- Use clear, professional communication

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions, ideas
- **Pull Requests**: Code contributions, reviews
- **Documentation**: Improvements and clarifications

## 🏗️ Development Areas

### Current Priorities

1. **Performance Optimization**
   - GPU acceleration support
   - Batch processing improvements
   - Memory usage optimization

2. **Feature Enhancements**
   - Additional droplet shapes
   - Animation support
   - Real-time processing

3. **Documentation**
   - More examples and tutorials
   - Video demonstrations
   - API reference improvements

4. **Testing**
   - Increased test coverage
   - Performance benchmarks
   - Cross-platform testing

### Architecture Improvements

```python
# Future architecture considerations
class DropletRenderer:
    """Separate rendering logic for better testability."""
    pass

class EffectPipeline:
    """Composable effects pipeline."""
    pass

class ConfigValidator:
    """Validate and sanitize configuration."""
    pass
```

## 📚 Resources for Contributors

### Learning Materials
- [Computer Vision with OpenCV](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [PIL/Pillow Documentation](https://pillow.readthedocs.io/)
- [NumPy User Guide](https://numpy.org/doc/stable/user/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

### Tools and Setup
- [Visual Studio Code](https://code.visualstudio.com/) with Python extensions
- [PyCharm](https://www.jetbrains.com/pycharm/) for advanced development
- [Git](https://git-scm.com/) for version control
- [Anaconda](https://www.anaconda.com/) for environment management

## 🎯 Recognition

Contributors will be:
- Listed in AUTHORS.md
- Mentioned in release notes
- Credited in documentation
- Invited to maintainer team (for significant contributors)

## ❓ Getting Help

- **Technical Questions**: Open a GitHub Discussion
- **Bug Reports**: Create a GitHub Issue
- **General Chat**: Use GitHub Discussions
- **Direct Contact**: [maintainer email]

---

Thank you for contributing to ROLE! Every contribution, no matter how small, helps make this project better for everyone. 🌧️✨
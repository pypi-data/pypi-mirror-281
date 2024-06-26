# UNav

UNav is designed for helping navigation of visually impaired people. It leverages various features and algorithms to provide accurate localization and navigation assistance.

## Features

- **Global Feature Extraction**: Using NetVLAD for image-based localization.
- **Local Feature Extraction**: Using SuperPoint and SuperGlue for detailed image matching.
- **Navigation and Localization**: Combines global and local features for accurate navigation.

## Developer Installation

To install UNav as a developer, follow these steps:

### Prerequisites

- Python 3.6 or higher
- Cython
- NumPy
- PyTorch
- OpenCV
- h5py
- scikit-image

### Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/ai4ce/UNav_Server.git
    cd UNav_Server
    ```

2. Build the Cython extensions in place:
    ```bash
    python setup_so.py build_ext --inplace
    ```

3. Create the source distribution and wheel:
    ```bash
    python setup.py sdist bdist_wheel
    ```

4. Upload the package to PyPI:
    ```bash
    twine upload --verbose dist/*
    ```

## User Installation

Users can directly install UNav from PyPI:

```bash
pip install unav

# Galamsey Detection using Sentinel-2 Satellite Imagery and U-Net

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
  - [1. Set Up Google Earth Engine](#1-set-up-google-earth-engine)
  - [2. Define Area of Interest (AOI)](#2-define-area-of-interest-aoi)
  - [3. Download Sentinel-2 Data](#3-download-sentinel-2-data)
  - [4. Prepare Data for Training](#4-prepare-data-for-training)
  - [5. Train the U-Net Model](#5-train-the-unet-model)
  - [6. Evaluate and Visualize Results](#6-evaluate-and-visualize-results)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Welcome to the **Mine Detection using Sentinel-2 Satellite Imagery and U-Net** project. This repository contains scripts and resources to detect mines in satellite imagery using deep learning techniques, specifically the U-Net architecture. By leveraging Google Earth Engine (GEE) for data acquisition and preprocessing, and TensorFlow/Keras for model training, this project aims to provide an efficient pipeline for identifying mine locations in high-resolution satellite images.

## Features

- **Automated Data Acquisition:** Uses Google Earth Engine to download Sentinel-2 satellite imagery within a specified Area of Interest (AOI).
- **Cloud Masking:** Applies cloud and cirrus masking to ensure clean imagery for analysis.
- **Grid Tiling:** Splits the AOI into manageable grid tiles for efficient processing.
- **Data Preprocessing:** Normalizes images and prepares them for model training by creating overlapping patches.
- **Deep Learning Model:** Implements and trains a U-Net model for multi-class segmentation to detect mines.
- **Visualization:** Provides tools to visualize training metrics and model predictions with appropriate color mappings.

## Demo

![Sample Prediction](![demo_prediction](https://github.com/user-attachments/assets/67ad5916-d236-4404-a4af-8fcca0b98ebb)
) 

*Figure: Sample prediction of mine locations using the trained U-Net model.*

## Installation

### Prerequisites

- **Python 3.12+**
- **Google Earth Engine Account:** [Sign up here](https://earthengine.google.com/signup/)

### Clone the Repository

```bash
git clone https://nonnabyte/ComputerVisionProjects/galamsey-detector.git
cd mine-detection
```

### Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

*If `requirements.txt` is not provided, install the necessary packages manually:*

```bash
pip install earthengine-api requests rasterio matplotlib scikit-learn tensorflow keras
```

### Authenticate Google Earth Engine

```bash
earthengine authenticate
```

Follow the prompts to authenticate your account.

## Usage

### 1. Set Up Google Earth Engine

Ensure that you've authenticated your GEE account as mentioned.

### 2. Define Area of Interest (AOI)

The AOI is defined using geographic coordinates. Modify the coordinates in the script as needed.

### 3. Download Sentinel-2 Data

The script splits the AOI into grid tiles, applies cloud masking, and downloads the median composite images.

### 4. Prepare Data for Training

Load the satellite images and label masks, normalize the data, and create overlapping patches to increase the dataset size.

### 5. Train the U-Net Model

Define the U-Net architecture, compile the model, and train it using the prepared dataset.

### 6. Evaluate and Visualize Results

Plot training metrics and visualize model predictions with appropriate color mappings.



## Project Structure

```
mine-detection/
├── data/
│   ├── satellite_image.tif
│   ├── labels.tif
│   └── tiles/
│       ├── tile_0.tif
│       ├── tile_1.tif
│       └── ...
├── scripts/
│   ├── galamsey.ipynb
├── images/
│   └── demo_prediction.png
└── README.md
```


## License

This project is licensed under the [MIT License](LICENSE).

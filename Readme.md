# 🏠 Multimodal Real Estate Price Prediction  
**Tabular Data + Satellite Imagery**

---

## 📌 Project Overview

This project implements a **multimodal regression pipeline** to predict real estate prices by combining **structured housing attributes** with **satellite imagery** that captures neighborhood-level spatial context.

The primary objective is to evaluate whether **visual information extracted from satellite images** can enhance predictive performance beyond traditional tabular-only models.

All experiments, training, and evaluation were performed using **Kaggle Notebooks**.

---

## 📂 Repository Contents

├── final_notebook.ipynb # Complete pipeline (preprocessing → modeling → explainability)<br>
├── train.xlsx # Training dataset<br>
├── test.xlsx # Test dataset<br>
├── prediction.csv # Final predictions<br>
├── data_fetcher.py<br>
├── preprocessing.ipynb<br>
├── model_training.ipynb<br>
└── README.md<br>



**Note:**  
All code (data preprocessing, CNN feature extraction,training ,modeling, and explainability) is contained within a **single notebook**(final_notebook.ipynb).<br>
Other parts of code have been seperated to meet the requirements of the deliverables.<br>

---

## 📊 Dataset Description

### Input Files

- **train.xlsx**  
  Contains housing features along with the target variable `price`.

- **test.xlsx**  
  Contains the same housing features but without the target variable.

### Target Variable

- **price** – Market value of the property.

### Key Features

**Structural attributes**
- `bedrooms`, `bathrooms`
- `sqft_living`, `sqft_lot`
- `grade`, `condition`
- `view`, `waterfront`

**Neighborhood context**
- `sqft_living15`, `sqft_lot15`

**Spatial coordinates**
- `lat`, `long`

---

## 🧹 Data Preprocessing

- Rows with missing target values (`price`) are removed.
- Missing numerical values are handled using **median imputation**.
- The target variable is log-transformed to reduce skewness:

log_price = log(price + 1)


This transformation improves regression stability and reduces the influence of extreme price outliers.

---

## 🌍 Satellite Image Acquisition

Satellite images are programmatically fetched using the **ESRI World Imagery service** via the **ArcGIS REST API**.

### API Endpoint

https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export


### Image Retrieval Process

- Latitude and longitude values are used to compute a bounding box around each property.
- A fixed spatial region surrounding the property is requested.
- Images are retrieved using standard **HTTP GET requests**.
- Each property is associated with one satellite image.

These images capture:
- Neighborhood layout
- Housing density
- Greenery and open spaces

---

## 🧠 CNN Feature Extraction

A pretrained **Convolutional Neural Network (CNN)** converts satellite images into numerical embeddings.

### CNN Architecture

- **Model:** ResNet-18  
- **Pretraining:** ImageNet  
- **Framework:** PyTorch  

### Usage

- The final classification layer is removed.
- The CNN is used **only as a feature extractor**.
- Each image is converted into a **512-dimensional embedding**.
- No CNN fine-tuning is performed.

### Image Preprocessing

- Resize images to **224 × 224**
- Normalize using ImageNet mean and standard deviation

These embeddings encode high-level visual characteristics of the neighborhood.

---

## 📈 Baseline Model (Tabular Only)

### Model Used

- **XGBoost Regressor**

### Rationale

XGBoost is well-suited for structured data due to:
- Modeling non-linear feature interactions
- Handling heterogeneous feature scales

### Performance

- **R² (log scale):** 0.6993  
- **RMSE (price scale):** 187,610.99  

This model serves as the baseline reference.

---

## 🔬 Tried Architectures

### Random Forest (Multimodal)

A Random Forest regressor was evaluated using tabular features combined with CNN embeddings.

- **R² (log scale):** 0.7273  

**Reason for lower performance**
- Trees are built independently (bagging)
- Less effective with high-dimensional CNN embeddings
- No gradient-based error correction

---

## 🏆 Final Model: Multimodal XGBoost

### Architecture

Tabular Features ─┐<br>
├── XGBoost ──► Price Prediction<br>
CNN Embeddings ───┘<br>


- CNN embeddings are concatenated with tabular features.
- XGBoost learns joint interactions across both modalities.

### Performance

- **Multimodal R² (log scale):** 0.7663  
- **Multimodal RMSE (price scale):** 169,231.18  

This demonstrates a clear improvement over the tabular-only baseline.

---

## 🔍 Exploratory Data Analysis (EDA)

- Correlation heatmaps show strongest influence from:
  - `grade`
  - `sqft_living`
- Spatial plots reveal geographic clustering of property prices.
- Satellite images highlight:
  - Neighborhood density
  - Layout patterns
  - Open spaces

---

## 🧠 Explainability with Grad-CAM

**Grad-CAM (Gradient-weighted Class Activation Mapping)** is used to visualize which regions of satellite images influence CNN feature extraction.

### Observations

CNN attention focuses on:
- Open spaces
- Greenery
- Surrounding house density

Less emphasis is placed on individual buildings.

### Interpretation

Satellite imagery contributes **neighborhood-level environmental context**, complementing structured housing attributes rather than replacing them.

---

## ▶️ How to Run (Kaggle)

1. Open a new Kaggle Notebook
2. Upload:
   - `train.xlsx`
   - `test.xlsx`
   - `multimodal_real_estate.ipynb`
3. Run all cells in order

**Output generated:**
- `prediction.csv`

No additional setup is required.

---

## ▶️ How to Run (Local Machine)

### Requirements

pip install numpy pandas scikit-learn xgboost torch torchvision pillow tqdm matplotlib seaborn requests


### Steps

1. Place the following files in the same directory:
   - `multimodal_real_estate.ipynb`
   - `train.xlsx`
   - `test.xlsx`
2. Open the notebook using Jupyter or VS Code
3. Run all cells sequentially

**Output generated:**
- `prediction.csv`

---

## 📤 Output Format

id,predicted_price

---

## 📌 Final Takeaway

Structural housing attributes dominate real estate price prediction, while **satellite imagery provides complementary neighborhood-level context** that improves performance when fused using **XGBoost**.

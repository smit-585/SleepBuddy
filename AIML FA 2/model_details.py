#!/usr/bin/env python3
"""
Detailed analysis of the SleepBuddy AI model
"""
import joblib
import pandas as pd
import numpy as np

print("=" * 60)
print("SLEEPBUDDY AI MODEL ANALYSIS")
print("=" * 60)

# Load all model components
model = joblib.load('sleep_quality_model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoders = joblib.load('label_encoders.pkl')

print("\nDATASET INFORMATION:")
df = pd.read_csv('Sleep_health_and_lifestyle_dataset.csv')
print(f"Total Records: {len(df)}")
print(f"Features: {len(df.columns) - 1}")  # -1 for Person ID
print(f"Dataset Shape: {df.shape}")

print("\nTARGET VARIABLE:")
sleep_quality_dist = df['Quality of Sleep'].value_counts().sort_index()
print("Original Sleep Quality Distribution (1-10 scale):")
for score, count in sleep_quality_dist.items():
    print(f"  Score {score}: {count} records")

# Show categorization
def categorize_sleep(q):
    if q >= 7: return "Good"
    elif q >= 5: return "Average"
    else: return "Poor"

df["SleepQualityLabel"] = df["Quality of Sleep"].apply(categorize_sleep)
categorical_dist = df["SleepQualityLabel"].value_counts()
print("\nCategorized Sleep Quality Distribution:")
for category, count in categorical_dist.items():
    percentage = (count / len(df)) * 100
    print(f"  {category}: {count} records ({percentage:.1f}%)")

print("\nMODEL DETAILS:")
print(f"Algorithm: {type(model).__name__}")
print(f"Number of Trees: {model.n_estimators}")
print(f"Random State: {model.random_state}")
print(f"Number of Features: {model.n_features_in_}")
print(f"Classes: {list(model.classes_)}")

print("\nMODEL PERFORMANCE:")
print("Accuracy: 98.67% (from training)")
print("Precision: 99% (weighted average)")
print("Recall: 99% (weighted average)")
print("F1-Score: 99% (weighted average)")

print("\nFEATURE ENGINEERING:")
print("Features used in model:")
feature_names = ['Gender', 'Age', 'Occupation', 'Sleep Duration', 'Physical Activity Level', 
                'Stress Level', 'BMI Category', 'Blood Pressure', 'Heart Rate', 'Daily Steps', 'Sleep Disorder']

feature_importances = model.feature_importances_
feature_importance_pairs = list(zip(feature_names, feature_importances))
feature_importance_pairs.sort(key=lambda x: x[1], reverse=True)

print("\nFeature Importance Ranking:")
for i, (feature, importance) in enumerate(feature_importance_pairs, 1):
    print(f"  {i}. {feature}: {importance:.4f} ({importance*100:.2f}%)")

print("\nLABEL ENCODERS:")
for col, encoder in label_encoders.items():
    print(f"\n{col}:")
    for i, class_name in enumerate(encoder.classes_):
        print(f"  {i}: {class_name}")

print("\nSCALER INFORMATION:")
print(f"Scaler Type: {type(scaler).__name__}")
print(f"Features scaled: {len(scaler.feature_names_in_)}")

print("\nFeature Scaling Statistics:")
for i, feature in enumerate(scaler.feature_names_in_):
    print(f"  {feature}:")
    print(f"    Mean: {scaler.mean_[i]:.4f}")
    print(f"    Scale: {scaler.scale_[i]:.4f}")

print("\nDATA PREPROCESSING PIPELINE:")
print("1. Load raw dataset with 11 features")
print("2. Create categorical target from Quality of Sleep:")
print("   - Good: Score >= 7")
print("   - Average: Score 5-6") 
print("   - Poor: Score < 5")
print("3. Remove Person ID and original Quality of Sleep columns")
print("4. Apply Label Encoding to categorical features:")
for col in label_encoders.keys():
    print(f"   - {col}")
print("5. Apply StandardScaler to all features")
print("6. Train RandomForestClassifier with 200 trees")
print("7. Save model, scaler, and encoders as .pkl files")

print("\nAPI INTEGRATION:")
print("Flask API endpoint: /api/predict")
print("Input: JSON with 11 feature values")
print("Output: Prediction + probability scores")
print("CORS enabled for frontend integration")

print("\nFILES IN AIML FA 2 FOLDER:")
import os
files = os.listdir('.')
for file in sorted(files):
    if os.path.isfile(file):
        size = os.path.getsize(file)
        print(f"  {file} ({size:,} bytes)")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)

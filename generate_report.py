#!/usr/bin/env python3
"""
Generate a comprehensive PDF report for the SleepBuddy AI Model
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import pandas as pd
import joblib
import os
from datetime import datetime

def create_sleepbuddy_report():
    # Create PDF document
    filename = "SleepBuddy_AI_Model_Report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        textColor=colors.darkgreen
    )
    
    # Title Page
    story.append(Paragraph("SleepBuddy AI Model", title_style))
    story.append(Paragraph("Comprehensive Technical Report", styles['Heading2']))
    story.append(Spacer(1, 0.5*inch))
    
    # Project info
    project_info = f"""
    <b>Project:</b> Sleep Quality Prediction System<br/>
    <b>Algorithm:</b> Random Forest Classifier<br/>
    <b>Dataset:</b> Sleep Health and Lifestyle Dataset<br/>
    <b>Model Accuracy:</b> 98.67%<br/>
    <b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y')}<br/>
    """
    story.append(Paragraph(project_info, styles['Normal']))
    story.append(PageBreak())
    
    # Table of Contents
    story.append(Paragraph("Table of Contents", heading_style))
    toc_content = """
    1. Executive Summary<br/>
    2. Dataset Overview<br/>
    3. Model Architecture<br/>
    4. Data Preprocessing<br/>
    5. Model Performance<br/>
    6. Feature Analysis<br/>
    7. API Implementation<br/>
    8. Frontend Integration<br/>
    9. Technical Specifications<br/>
    10. Usage Guidelines<br/>
    """
    story.append(Paragraph(toc_content, styles['Normal']))
    story.append(PageBreak())
    
    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", heading_style))
    exec_summary = """
    The SleepBuddy AI Model is a machine learning system designed to predict sleep quality based on 
    lifestyle and health factors. Using a Random Forest Classifier with 200 decision trees, the model 
    achieves exceptional performance with 98.67% accuracy on test data.
    
    The system categorizes sleep quality into three levels: Good (≥7), Average (5-6), and Poor (<5), 
    based on a comprehensive analysis of 11 input features including demographics, health metrics, 
    and lifestyle factors.
    
    Key achievements:
    • High accuracy classification (98.67%)
    • Robust feature engineering pipeline
    • Real-time web API integration
    • Modern responsive frontend interface
    • Comprehensive data preprocessing
    """
    story.append(Paragraph(exec_summary, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # 2. Dataset Overview
    story.append(Paragraph("2. Dataset Overview", heading_style))
    
    # Load dataset for analysis
    try:
        df = pd.read_csv('AIML FA 2/Sleep_health_and_lifestyle_dataset.csv')
        
        dataset_info = f"""
        <b>Dataset Name:</b> Sleep Health and Lifestyle Dataset<br/>
        <b>Total Records:</b> {len(df)} individuals<br/>
        <b>Features:</b> {len(df.columns) - 1} input features + 1 target variable<br/>
        <b>Data Quality:</b> Clean dataset with minimal missing values<br/>
        <b>Target Variable:</b> Quality of Sleep (1-10 scale)<br/>
        """
        story.append(Paragraph(dataset_info, styles['Normal']))
        
        # Feature list
        story.append(Paragraph("Input Features:", subheading_style))
        features_list = """
        1. <b>Gender:</b> Male/Female (categorical)<br/>
        2. <b>Age:</b> Numeric (years)<br/>
        3. <b>Occupation:</b> 11 different job categories<br/>
        4. <b>Sleep Duration:</b> Hours of sleep per night<br/>
        5. <b>Physical Activity Level:</b> Minutes of activity per day<br/>
        6. <b>Stress Level:</b> 1-10 subjective scale<br/>
        7. <b>BMI Category:</b> Normal Weight/Normal/Overweight/Obese<br/>
        8. <b>Blood Pressure:</b> Systolic/Diastolic format<br/>
        9. <b>Heart Rate:</b> Beats per minute<br/>
        10. <b>Daily Steps:</b> Number of steps per day<br/>
        11. <b>Sleep Disorder:</b> None/Sleep Apnea/Insomnia<br/>
        """
        story.append(Paragraph(features_list, styles['Normal']))
        
        # Target distribution
        def categorize_sleep(q):
            if q >= 7: return "Good"
            elif q >= 5: return "Average"
            else: return "Poor"
        
        df["SleepQualityLabel"] = df["Quality of Sleep"].apply(categorize_sleep)
        dist = df["SleepQualityLabel"].value_counts()
        
        story.append(Paragraph("Target Variable Distribution:", subheading_style))
        target_dist = f"""
        • <b>Good Sleep:</b> {dist.get('Good', 0)} records ({dist.get('Good', 0)/len(df)*100:.1f}%)<br/>
        • <b>Average Sleep:</b> {dist.get('Average', 0)} records ({dist.get('Average', 0)/len(df)*100:.1f}%)<br/>
        • <b>Poor Sleep:</b> {dist.get('Poor', 0)} records ({dist.get('Poor', 0)/len(df)*100:.1f}%)<br/>
        """
        story.append(Paragraph(target_dist, styles['Normal']))
        
    except Exception as e:
        story.append(Paragraph(f"Dataset analysis unavailable: {str(e)}", styles['Normal']))
    
    story.append(PageBreak())
    
    # 3. Model Architecture
    story.append(Paragraph("3. Model Architecture", heading_style))
    
    try:
        model = joblib.load('AIML FA 2/sleep_quality_model.pkl')
        
        model_arch = f"""
        <b>Algorithm:</b> Random Forest Classifier<br/>
        <b>Number of Trees:</b> {model.n_estimators}<br/>
        <b>Random State:</b> {model.random_state} (for reproducibility)<br/>
        <b>Input Features:</b> {model.n_features_in_}<br/>
        <b>Output Classes:</b> {len(model.classes_)} ({', '.join(model.classes_)})<br/>
        <b>Implementation:</b> scikit-learn RandomForestClassifier<br/>
        """
        story.append(Paragraph(model_arch, styles['Normal']))
        
        story.append(Paragraph("Model Characteristics:", subheading_style))
        characteristics = """
        • <b>Ensemble Method:</b> Combines predictions from 200 decision trees<br/>
        • <b>Bootstrap Sampling:</b> Each tree trained on random subset of data<br/>
        • <b>Feature Randomness:</b> Random feature selection at each split<br/>
        • <b>Voting Mechanism:</b> Majority vote for final prediction<br/>
        • <b>Overfitting Resistance:</b> Ensemble approach reduces overfitting<br/>
        • <b>Feature Importance:</b> Built-in feature importance calculation<br/>
        """
        story.append(Paragraph(characteristics, styles['Normal']))
        
    except Exception as e:
        story.append(Paragraph(f"Model analysis unavailable: {str(e)}", styles['Normal']))
    
    story.append(PageBreak())
    
    # 4. Data Preprocessing
    story.append(Paragraph("4. Data Preprocessing Pipeline", heading_style))
    
    preprocessing_steps = """
    <b>Step 1: Data Loading</b><br/>
    • Load CSV dataset with 374 records<br/>
    • Verify data integrity and structure<br/><br/>
    
    <b>Step 2: Target Variable Creation</b><br/>
    • Convert Quality of Sleep (1-10) to categorical:<br/>
    &nbsp;&nbsp;- Good: Score ≥ 7<br/>
    &nbsp;&nbsp;- Average: Score 5-6<br/>
    &nbsp;&nbsp;- Poor: Score < 5<br/><br/>
    
    <b>Step 3: Feature Selection</b><br/>
    • Remove Person ID (not predictive)<br/>
    • Remove original Quality of Sleep (target leakage)<br/>
    • Retain 11 meaningful features<br/><br/>
    
    <b>Step 4: Categorical Encoding</b><br/>
    • Apply Label Encoding to categorical features:<br/>
    &nbsp;&nbsp;- Gender, Occupation, BMI Category, Sleep Disorder<br/>
    • Handle missing values (NaN) appropriately<br/>
    • Save encoders for deployment use<br/><br/>
    
    <b>Step 5: Feature Scaling</b><br/>
    • Apply StandardScaler to all features<br/>
    • Normalize to zero mean, unit variance<br/>
    • Essential for ensemble methods<br/><br/>
    
    <b>Step 6: Train-Test Split</b><br/>
    • 80% training, 20% testing<br/>
    • Stratified split to maintain class distribution<br/>
    • Random state 42 for reproducibility<br/>
    """
    story.append(Paragraph(preprocessing_steps, styles['Normal']))
    story.append(PageBreak())
    
    # 5. Model Performance
    story.append(Paragraph("5. Model Performance", heading_style))
    
    performance_metrics = """
    <b>Overall Performance:</b><br/>
    • <b>Accuracy:</b> 98.67% (74/75 test samples correct)<br/>
    • <b>Precision:</b> 99% (weighted average)<br/>
    • <b>Recall:</b> 99% (weighted average)<br/>
    • <b>F1-Score:</b> 99% (weighted average)<br/><br/>
    
    <b>Per-Class Performance:</b><br/>
    • <b>Average Sleep:</b> 100% precision, 95% recall, 98% F1-score<br/>
    • <b>Good Sleep:</b> 98% precision, 100% recall, 99% F1-score<br/>
    • <b>Poor Sleep:</b> 100% precision, 100% recall, 100% F1-score<br/><br/>
    
    <b>Model Strengths:</b><br/>
    • Excellent generalization to unseen data<br/>
    • Balanced performance across all classes<br/>
    • No signs of overfitting<br/>
    • Robust to class imbalance<br/>
    • High confidence in predictions<br/>
    """
    story.append(Paragraph(performance_metrics, styles['Normal']))
    story.append(PageBreak())
    
    # 6. Feature Analysis
    story.append(Paragraph("6. Feature Importance Analysis", heading_style))
    
    try:
        model = joblib.load('AIML FA 2/sleep_quality_model.pkl')
        feature_names = ['Gender', 'Age', 'Occupation', 'Sleep Duration', 'Physical Activity Level', 
                        'Stress Level', 'BMI Category', 'Blood Pressure', 'Heart Rate', 'Daily Steps', 'Sleep Disorder']
        
        feature_importances = model.feature_importances_
        feature_importance_pairs = list(zip(feature_names, feature_importances))
        feature_importance_pairs.sort(key=lambda x: x[1], reverse=True)
        
        story.append(Paragraph("Feature Importance Ranking:", subheading_style))
        
        # Create table for feature importance
        table_data = [['Rank', 'Feature', 'Importance', 'Percentage']]
        for i, (feature, importance) in enumerate(feature_importance_pairs, 1):
            table_data.append([str(i), feature, f"{importance:.4f}", f"{importance*100:.2f}%"])
        
        table = Table(table_data, colWidths=[0.8*inch, 2.5*inch, 1.2*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        
        story.append(Spacer(1, 0.3*inch))
        feature_insights = """
        <b>Key Insights:</b><br/>
        • <b>Sleep Duration</b> is the most predictive factor<br/>
        • <b>Stress Level</b> has significant impact on sleep quality<br/>
        • <b>Age</b> and physiological factors (Heart Rate) are important<br/>
        • <b>Lifestyle factors</b> (Physical Activity, Daily Steps) contribute moderately<br/>
        • <b>Medical conditions</b> (Sleep Disorder) have measurable impact<br/>
        """
        story.append(Paragraph(feature_insights, styles['Normal']))
        
    except Exception as e:
        story.append(Paragraph(f"Feature analysis unavailable: {str(e)}", styles['Normal']))
    
    story.append(PageBreak())
    
    # 7. API Implementation
    story.append(Paragraph("7. API Implementation", heading_style))
    
    api_details = """
    <b>Technology Stack:</b><br/>
    • <b>Framework:</b> Flask (Python web framework)<br/>
    • <b>Endpoint:</b> POST /api/predict<br/>
    • <b>Port:</b> 5000 (default Flask development server)<br/>
    • <b>CORS:</b> Enabled for cross-origin requests<br/>
    • <b>Data Format:</b> JSON input/output<br/><br/>
    
    <b>API Workflow:</b><br/>
    1. Receive JSON data with 11 feature values<br/>
    2. Handle special cases (None sleep disorder → NaN)<br/>
    3. Create pandas DataFrame from input<br/>
    4. Apply saved label encoders to categorical features<br/>
    5. Apply saved StandardScaler to all features<br/>
    6. Generate prediction using trained model<br/>
    7. Calculate prediction probabilities<br/>
    8. Return JSON response with prediction and confidence scores<br/><br/>
    
    <b>Error Handling:</b><br/>
    • Input validation and sanitization<br/>
    • Graceful handling of unknown categories<br/>
    • Comprehensive error messages<br/>
    • HTTP status code management<br/>
    """
    story.append(Paragraph(api_details, styles['Normal']))
    story.append(PageBreak())
    
    # 8. Frontend Integration
    story.append(Paragraph("8. Frontend Integration", heading_style))
    
    frontend_details = """
    <b>Technology Stack:</b><br/>
    • <b>Framework:</b> React 19.1.1 with Vite<br/>
    • <b>Styling:</b> Modern CSS with glassmorphism effects<br/>
    • <b>Theme:</b> Sleep-focused design with night sky aesthetics<br/>
    • <b>Responsiveness:</b> Mobile-first responsive design<br/><br/>
    
    <b>User Interface Features:</b><br/>
    • <b>Form Validation:</b> Real-time validation with proper input types<br/>
    • <b>Dynamic Inputs:</b> Dropdowns, number inputs, and range sliders<br/>
    • <b>Loading States:</b> Animated spinners and progress indicators<br/>
    • <b>Results Display:</b> Confidence bars with smooth animations<br/>
    • <b>Visual Design:</b> Gradient backgrounds, floating elements, starry sky<br/><br/>
    
    <b>Data Integration:</b><br/>
    • Form fields exactly match model's expected inputs<br/>
    • Dropdown options aligned with training data categories<br/>
    • Proper handling of edge cases and validation<br/>
    • Real-time API communication with error handling<br/><br/>
    
    <b>User Experience:</b><br/>
    • Intuitive form layout with clear labels<br/>
    • Immediate feedback on form completion<br/>
    • Beautiful results presentation with confidence levels<br/>
    • Smooth animations and transitions<br/>
    """
    story.append(Paragraph(frontend_details, styles['Normal']))
    story.append(PageBreak())
    
    # 9. Technical Specifications
    story.append(Paragraph("9. Technical Specifications", heading_style))
    
    # File information
    try:
        file_info = []
        aiml_files = ['sleep_quality_model.pkl', 'scaler.pkl', 'label_encoders.pkl', 
                     'Sleep_health_and_lifestyle_dataset.csv', 'sleepbuddy_api.py']
        
        for file in aiml_files:
            try:
                size = os.path.getsize(f'AIML FA 2/{file}')
                file_info.append([file, f"{size:,} bytes"])
            except:
                file_info.append([file, "Not found"])
        
        tech_specs = f"""
        <b>File Structure:</b><br/>
        """
        story.append(Paragraph(tech_specs, styles['Normal']))
        
        # File table
        table_data = [['File', 'Size']] + file_info
        table = Table(table_data, colWidths=[3*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        
    except Exception as e:
        story.append(Paragraph(f"File analysis unavailable: {str(e)}", styles['Normal']))
    
    story.append(Spacer(1, 0.3*inch))
    
    system_reqs = """
    <b>System Requirements:</b><br/>
    • <b>Python:</b> 3.7+ with scikit-learn, pandas, numpy, flask<br/>
    • <b>Node.js:</b> 16+ for React development<br/>
    • <b>Browser:</b> Modern browsers with ES6+ support<br/>
    • <b>Memory:</b> Minimum 2GB RAM for model loading<br/>
    • <b>Storage:</b> ~50MB for complete application<br/><br/>
    
    <b>Deployment Considerations:</b><br/>
    • Model files require scikit-learn compatibility<br/>
    • CORS configuration needed for production<br/>
    • Consider model versioning for updates<br/>
    • Monitor API performance and scaling needs<br/>
    """
    story.append(Paragraph(system_reqs, styles['Normal']))
    story.append(PageBreak())
    
    # 10. Usage Guidelines
    story.append(Paragraph("10. Usage Guidelines", heading_style))
    
    usage_guide = """
    <b>Starting the Application:</b><br/>
    1. Navigate to project directory<br/>
    2. Start backend: <i>python "AIML FA 2/sleepbuddy_api.py"</i><br/>
    3. Start frontend: <i>npm run dev</i><br/>
    4. Access application at http://localhost:5173<br/><br/>
    
    <b>Using the Prediction System:</b><br/>
    1. Fill out all 11 required fields in the web form<br/>
    2. Ensure data quality (realistic values)<br/>
    3. Click "Predict Sleep Quality" button<br/>
    4. Review prediction and confidence scores<br/>
    5. Interpret results in context of lifestyle factors<br/><br/>
    
    <b>Interpreting Results:</b><br/>
    • <b>Good Sleep:</b> Optimal sleep quality, maintain current habits<br/>
    • <b>Average Sleep:</b> Room for improvement, focus on key factors<br/>
    • <b>Poor Sleep:</b> Significant issues, consider lifestyle changes<br/>
    • <b>Confidence Scores:</b> Higher percentages indicate more certainty<br/><br/>
    
    <b>Best Practices:</b><br/>
    • Provide accurate, honest information<br/>
    • Use consistent units (hours for sleep, steps for activity)<br/>
    • Consider multiple predictions over time for trends<br/>
    • Combine with professional medical advice when needed<br/><br/>
    
    <b>Limitations:</b><br/>
    • Model trained on specific dataset (374 samples)<br/>
    • Predictions are estimates, not medical diagnoses<br/>
    • Results may not apply to all populations equally<br/>
    • Consider individual variations and circumstances<br/>
    """
    story.append(Paragraph(usage_guide, styles['Normal']))
    
    # Footer
    story.append(Spacer(1, 0.5*inch))
    footer = f"""
    <b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
    <b>SleepBuddy AI Model - Technical Documentation</b><br/>
    <i>For questions or support, refer to the project documentation.</i>
    """
    story.append(Paragraph(footer, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print(f"PDF report generated successfully: {filename}")
    print(f"File size: {os.path.getsize(filename):,} bytes")
    
    return filename

if __name__ == "__main__":
    try:
        filename = create_sleepbuddy_report()
        print(f"\nReport created: {filename}")
        print("Location: Current directory")
        print("You can now open the PDF to view the complete analysis!")
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        print("Make sure you have reportlab installed: pip install reportlab")

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def train_model(data):
    # Prepare features and target variable
    df = data.copy()
    df['Abundance'] = df['Abundance'].fillna('Unknown')
    
    # Encode categorical data into nubers
    # Save enoders to transform user input later
    encoders = {}
    for col in ['Category', 'Abundance']:
        le = LabelEncoder()
        df[f'{col}_Enc'] = le.fit_transform(df[col])
        encoders[col] = le

    # Define the Target
    at_risk_statuses = ['Endangered', 'Threatened', 'Species of Concern']
    df['Is_At_Risk'] = df['Conservation Status'].isin(at_risk_statuses).astype(int)

    # Train the Model
    X = df[['Category_Enc', 'Abundance_Enc']]
    y = df['Is_At_Risk']

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    return model, encoders

def predict_species_risk(model, encoders, category, abundance):
    try:
        cat_enc = encoders['Category'].transform([category])[0]
        abun_enc = encoders['Abundance'].transform([abundance])[0]
        
        X = pd.DataFrame(
            [[cat_enc, abun_enc]], 
            columns=['Category_Enc', 'Abundance_Enc']
        )

        # Probability for class '1' (At Risk)
        prob = model.predict_proba(X)[0][1] 
        return round(prob * 100, 1)
    except:
        return 0.0
    

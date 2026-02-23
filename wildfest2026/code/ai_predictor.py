import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

def train_model(species_df, parks_df):
    # calc Biodiversity Density on the park level first
    # Density = Species Count / Acres
    species_counts = species_df.groupby('Park Name').size().reset_index(name='Species_Count')
    parks_with_metrics = pd.merge(parks_df, species_counts, on='Park Name')
    parks_with_metrics['Biodiversity_Density'] = (parks_with_metrics['Species_Count'] / parks_with_metrics['Acres']) * 1000

    # merge these park-level metrics back into the species list
    df = pd.merge(species_df, parks_with_metrics[['Park Name', 'Acres', 'Biodiversity_Density']], on='Park Name', how='left')
    
    # fill categorical na with 'Unknown' and numerical na with median
    df['Abundance'] = df['Abundance'].fillna('Unknown')
    df['Acres'] = df['Acres'].fillna(df['Acres'].median())
    df['Biodiversity_Density'] = df['Biodiversity_Density'].fillna(df['Biodiversity_Density'].median())
    
    # encode Categorical Data with LabelEncoder from sklearn
    encoders = {}
    for col in ['Category', 'Abundance']:
        le = LabelEncoder()
        df[f'{col}_Enc'] = le.fit_transform(df[col])
        encoders[col] = le

    # define target as the most concerning "statuses of endangerment"
    at_risk_statuses = ['Endangered', 'Threatened', 'Species of Concern']
    df['Is_At_Risk'] = df['Conservation Status'].isin(at_risk_statuses).astype(int)

    # train with these 4 features
    features = ['Category_Enc', 'Abundance_Enc', 'Acres', 'Biodiversity_Density']
    X = df[features]
    y = df['Is_At_Risk']

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    return model, encoders

def predict_species_risk(model, encoders, category, abundance, acres, density):
    try:
        # encode the input features using the same encoders from training
        cat_enc = encoders['Category'].transform([category])[0]
        abun_enc = encoders['Abundance'].transform([abundance])[0]
        
        # DataFrame columns must match the order and names used in training
        X = pd.DataFrame(
            [[cat_enc, abun_enc, acres, density]], 
            columns=['Category_Enc', 'Abundance_Enc', 'Acres', 'Biodiversity_Density']
        )

        # get the probability of being 'At Risk' (Class 1)
        prob = model.predict_proba(X)[0][1] 
        return round(prob * 100, 1)
    except:
        return 0.0
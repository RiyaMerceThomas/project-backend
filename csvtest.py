import pandas as pd

# Load the CSV data into a DataFrame
df = pd.read_csv('COVIDATA.csv')

# Define the columns with their respective weights
fever_weight = 0.75
body_pain_weight = 0.75
runny_nose_weight = 0.5
difficulty_in_breathing_weight = 1.5
nasal_congestion_weight = 0.5
sore_throat_weight = 0.5
severity_weight = 1.5
contact_with_covid_patient_weight = 2
spo2_weight = 1.5

def map_fever(value):
    return 0.1 if value <= 98 else 0.5 if value <= 104 else 1


# Calculate the weighted sum
weighted_sum = (
    df['fever'].map(map_fever) * fever_weight +
    df['body_pain'] * body_pain_weight +
    df['runny_nose'] * runny_nose_weight +
    df['difficulty_in_breathing'] * difficulty_in_breathing_weight +
    df['nasal_congestion'] * nasal_congestion_weight +
    df['sore_throat'] * sore_throat_weight +
    df['severity'].map({'Mild': 0.1, 'Moderate': 0.7, 'Severe': 1}) * severity_weight +
    df['contact_with_covid_patient'].map({'Yes': 1, 'No': 0, 'Not known':0.5}) * contact_with_covid_patient_weight +
    df['spo2'].map({'High': 0, 'Low': 1}) * spo2_weight
)

# Define the threshold for infection status
threshold = 4  # You can adjust this threshold as needed

# Assign infected status based on the threshold
df['Infected'] = (weighted_sum >= threshold).astype(int)

# Save the modified DataFrame back to a CSV file
df.to_csv('modified_data.csv', index=False)
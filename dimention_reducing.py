import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Load the data
df = pd.read_csv('Food_nutrions_fact.csv', low_memory=False)

# Turns cells with missing data as '-' to np.nan
df = df.replace('-', np.nan)

# Assume that the first 3 columns are non-numeric and drop them
df_numeric = df.drop(df.columns[:3], axis=1)

# Create an imputer object that replaces NaN values with the mean value of the column
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

# Apply the imputer to the DataFrame
df_numeric_imputed = imputer.fit_transform(df_numeric)

# Convert the result back to a DataFrame
df_numeric_imputed = pd.DataFrame(df_numeric_imputed, columns=df_numeric.columns)

# Standardize the features to have mean=0 and variance=1
features_scaled = StandardScaler().fit_transform(df_numeric_imputed.values)

# Apply PCA
pca = PCA(n_components=10)
principal_components = pca.fit_transform(features_scaled)

# Convert the principal components for each sample to a dataframe
df_numeric_imputed = pd.DataFrame(df_numeric_imputed, columns=[f'PC{i+1}' for i in range(df_numeric_imputed.shape[1])])

print(df_numeric_imputed.head())
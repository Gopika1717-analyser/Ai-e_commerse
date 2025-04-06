# Product Recommendation System based on Browsing and Purchase History

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast

# Load datasets
customer_df = pd.read_csv("C:\\Users\Admin\\3D Objects\\ai.python\\ Personalized E-Commerce\\customer_data_collection.csv")
product_df = pd.read_csv("C:\\Users\\Admin\\3D Objects\\ai.python\\Personalized  E-Commerce\\product_recommendation_data.csv")

# Fill missing values and clean up
customer_df = customer_df.dropna(subset=['Browsing_History', 'Purchase_History'])
product_df = product_df.dropna(subset=['Category', 'Subcategory'])

# Convert stringified lists into real lists
customer_df['Browsing_History'] = customer_df['Browsing_History'].apply(ast.literal_eval)
customer_df['Purchase_History'] = customer_df['Purchase_History'].apply(ast.literal_eval)
product_df['Similar_Product_List'] = product_df['Similar_Product_List'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])

# Combine product category data into one text field for vectorization
product_df['combined'] = product_df['Category'] + ' ' + product_df['Subcategory'] + ' ' + product_df['Brand']

# Vectorize the product features
vectorizer = CountVectorizer()
product_vectors = vectorizer.fit_transform(product_df['combined'])

# Recommendation function
def recommend_products(customer_id, top_n=5):
    customer = customer_df[customer_df['Customer_ID'] == customer_id]
    if customer.empty:
        return []

    # Combine browsing and purchase history
    interests = customer.iloc[0]['Browsing_History'] + customer.iloc[0]['Purchase_History']
    interests_str = ' '.join(interests)
    
    # Vectorize customer interests
    interest_vector = vectorizer.transform([interests_str])

    # Compute cosine similarity with product vectors
    similarity_scores = cosine_similarity(interest_vector, product_vectors).flatten()

    # Get top product indices
    top_indices = similarity_scores.argsort()[::-1][:top_n]

    # Return top matching products
    return product_df.iloc[top_indices][['Product_ID', 'Category', 'Subcategory', 'Brand', 'Product_Rating']]

# Example usage
if _name_ == '_main_':
    customer_id = 'C1000'  # change as needed
    recommendations = recommend_products(customer_id, top_n=5)
    print("Recommended products for customer", customer_id)
    print(recommendations)
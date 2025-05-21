# HairStylist
Developed an AI application to analyze users’ hair type from images and provide haircare recommendations based on
their predicted hair type, selected price range, and products' top feedback.

# Deployed Web App: 
https://hairstylist-xytvh4e35rqqf7hckt3hse.streamlit.app/

# Tech Stack:
Python, TensorFlow, Streamlit, OpenCV, Pillow, Matplotlib, TextBlob

# Overview:

1. The application uses transfer learning model, MobileNetV2, to analyze user's image to predict their hairtype as Curly, Straight, Wavy, Kinky.

2. Based on the user's predicted hairtype, the application provides hair care recommendations.

3. The application uses content-filtering, TF-IDF with cosine similarity to filter products according to user's hairtype. It uses 2 datasets a hairtypekeyword dataset and a product dataset (shampoo_data.csv) to match keywords with products.

4. It also uses basic sentiment analysis (textblob) to filter products according to the top reviews/feedbacks. 

5. The application has clean UI built with streamlit that allows users's to either upload their photos or take photos directly and then provide haircare recommendations. Links are provided for each product.

6. Deployed the application using Streamlit Cloud.

# Features:

1. Dataset: The application has total 3 datasets:
     
     1. hair_dataset.csv: It is developed by converting the different image folders in Dataset folder to image paths in the feature column and with each label in hairtype dataframe as their target, generated using label.py.The Dataset folder is from Kaggle.
     
     2. hairtypekeyword.csv: This contains keywords specific to each hairtype as their target. The keywords can be found in the product dataset in product highlights, specifications, description etc.
     
     3. shampoo_data.csv: It contains product details specific to each hairtype. This dataset is from Kaggle.

2. Image analysis using transfer learning: The application uses a transfer-learning model MobileNetV2 for image analysis and classification. It uses Data Augmentation techniques to optimize performance.

3. Image pre-processing using OpenCV: The model uses OpenCV to pre-process images.

4. Interactive Data visualisation: Uses matplotlib to visualise image data.

5. Test Accuracy: 0.80 to 0.86 (varies due to randomness). The model with highest accuracy (0.86) is saved for future predictions. 

6. Product Recommendation using content-based filtering: The system uses scikit-learn's  TF-IDF and cosine similarity to match products from shampoo_data.csv with keywords from hairtypekeyword.csv and filter them according to prices, similarity score etc.

7. Sentiment analysis using textblob: Uses textblob for basic sentiment analysis of product feedback and filter products according to feedback_score. The products with top feedback scores are prioritised.

8. User Interface: The application has clean UI built with streamlit that allows users to either upload their photos or take photos directly and then provide haircare recommendations. Links are provided for each product. Users can can also select their own price range from the drop down menu to get products according to their preferred price range.

9. Deployment: Deployed a web app using Streamlit Cloud.
   







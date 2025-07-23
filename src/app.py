import streamlit as st
import time
import tempfile
from PIL import Image
from prediction import predict_hairtype
from productrecommendation import recommend_products

st.markdown("""
    <style>
    .navbar {
        background-color: #ffb6c1; 
        padding: 15px;
        text-align: center;
        color: white;
        font-size: 32px;
        font-style: italic;
        font-weight: bold;
        border-radius: 8px;
    }
    .product-card {
        background-color: #f9f9f9;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        width: 100%; 
        
        box-sizing: border-box; /* Ensure padding is included in the width */
    }
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 4px 4px 15px rgba(0,0,0,0.2);
        cursor: pointer;
    }
    .product-card h4 {
        font-size: 14px;
        color: #333;
        margin-bottom: 8px;
    }
    .product-card p {
        margin: 5px 0;
        font-size: 14px;
        color: #666;
    }
    .product-card a {
        text-decoration: none;
        color: inherit;
    }
    .product-card a:hover {
        color: #0056b3;
    }
    .product-card img {
        width: 300px;
        height: 300px;
        border-radius: 8px;
    }
    </style>

    <div class="navbar">💅 Hey Diva 💅</div>
    <h1 style='text-align: center; font-size: 50px; color: #FF69B4;'><strong>Welcome To HairStylist</strong></h1>
""",
unsafe_allow_html=True)

option = st.radio("Choose an option:", ("Upload an Image", "Take Photo"))
image_path = None

if option == "Upload an Image":
    uploaded_file = st.file_uploader("Upload an image of your hair", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            image_path = temp_file.name
            image.save(image_path)

elif option == "Take Photo":
    camera_image = st.camera_input("Take Photo")
    if camera_image:
        image = Image.open(camera_image)
        st.image(image, caption="Taken Photo", use_container_width=True)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            image_path = temp_file.name
            image.save(image_path)
            
if image_path:
    if "last_uploaded_image" not in st.session_state or st.session_state.last_uploaded_image != image_path:
        st.session_state.last_uploaded_image = image_path #Stores new image
        with st.spinner("Please wait a moment..."):
            time.sleep(3)
            st.session_state.hair_prediction = predict_hairtype(image_path) 
    
    prediction = st.session_state.hair_prediction  
    st.markdown(f"""
        <p style="font-size:25px; font-weight:bold; text-align:center;">
            <strong>Your Hair Type is: {prediction}</strong>
        </p>
    """, unsafe_allow_html=True)
    st.write("")  

    if prediction=='CurlyHair':
        st.write("Curly hair tends to be dry and frizzy, so moisture is key. Use a sulfate-free, hydrating shampoo 2–3 times a week and always follow up with a deep conditioner. Detangle hair while it's wet using a wide-tooth comb and apply a leave-in conditioner or curl cream for hydration. Avoid brushing dry hair to prevent frizz. Style with a lightweight gel or mousse for definition and let your curls air dry or use a diffuser for volume.")
    elif prediction=='WavyHair':
        st.write("Wavy hair needs lightweight moisture to maintain its texture without weighing it down. Use a mild, sulfate-free shampoo every 2–3 days and condition the ends to prevent dryness. Avoid heavy oils or butters, as they can flatten waves. After washing, scrunch damp hair with a curl-enhancing mousse or gel and let it air dry for a natural look. To refresh waves between washes, use a spray bottle with water and a bit of leave-in conditioner.")
    elif prediction=='KinkyHair':
        st.write("Kinky hair requires intense hydration and protection to prevent dryness and breakage. Wash once a week with a moisturizing shampoo and follow up with a deep conditioner. The LOC method (Leave-in conditioner, Oil, Cream) helps lock in moisture. Protective styles like braids or twists can minimize manipulation. Keep the scalp hydrated with natural oils like coconut or castor oil, and always sleep with a satin bonnet or pillowcase to reduce friction and breakage.")
    elif prediction=='StraightHair':
        st.write("Straight hair can get oily quickly, so it's best to use a gentle, volumizing shampoo every 1–2 days. Avoid applying conditioner to the roots to prevent greasiness, and use a lightweight conditioner on the ends instead. To maintain volume, avoid heavy styling products. If using heat tools, apply a heat protectant beforehand. A clarifying shampoo once in a while can help remove buildup and keep hair fresh.")
    
    st.write("Recommended Products for Your Hair Type:")

    st.markdown("""
    <style>
    div[data-baseweb="select"] > div {
        transition: all 0.3s ease-in-out;
        border-radius: 5px;
    }
    
    div[data-baseweb="select"] > div:hover {
        opacity: 50%;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)
    price_options = ["All Prices", "Under ₹200", "₹200 - ₹500", "₹500 - ₹1000", "₹1000+"]
    selected_price = st.selectbox("Choose Your Price:", price_options, index=0)


    if selected_price == "Under ₹200":
        min_price, max_price = 0, 200
    elif selected_price == "₹200 - ₹500":
        min_price, max_price = 200, 500
    elif selected_price == "₹500 - ₹1000":
        min_price, max_price = 500, 1000
    elif selected_price == "₹1000+":
        min_price, max_price = 1000, float("inf")
    else:
        min_price, max_price = 0, float("inf")  


    recommended_products = recommend_products(prediction, max_price=max_price, min_feedback=0.2, top_n=50)

    recommended_products = recommended_products[(recommended_products['Product Cost'] >= min_price) & 
                                            (recommended_products['Product Cost'] <= max_price)]

    if recommended_products.empty:
        st.warning("No matching products found within the selected price range.")
    else:
        if "num_displayed" not in st.session_state:
            st.session_state.num_displayed = 5  

        for i in range(0, st.session_state.num_displayed, 2):
            col1, col2 = st.columns(2)
        
            if i < len(recommended_products):
                with col1:
                    row = recommended_products.iloc[i]
                    st.markdown(f"""
                    <div class="product-card">
                        <a href="{row['Link']}" target="_blank">
                            <h4>{row['Product Name']}</h4>
                        </a>
                        <img src="{row['Product_Img_Link']}" alt="{row['Product Name']}">
                        <p><b>Price:</b> ₹{row['Product Cost']}</p>
                        <p><b>Top Review:</b> "{row['feedback']}"</p>
                    </div>
                    """, unsafe_allow_html=True)
        
            if i + 1 < len(recommended_products):
                with col2:
                    row = recommended_products.iloc[i + 1]
                    st.markdown(f"""
                    
                    <div class="product-card">
                        <a href="{row['Link']}" target="_blank">
                        <h4>{row['Product Name']}</h4>
                        </a>
                        <img src="{row['Product_Img_Link']}" alt="{row['Product Name']}">
                        <p><b>Price:</b> ₹{row['Product Cost']}</p>
                        <p><b>Top Review:</b> "{row['feedback']}"</p>
                    </div>
                    <br>
                    """, unsafe_allow_html=True)

        if st.session_state.num_displayed < len(recommended_products):
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("Show More"):
                st.session_state.num_displayed += 5  
                st.rerun()

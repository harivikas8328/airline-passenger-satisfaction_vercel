
import streamlit as st
import requests

st.set_page_config(page_title="Quick Passenger Predictor", layout="centered")

# API_URL = "https://airline-passenger-satisfaction-1-aklg.onrender.com/predict"
API_URL="https://<your-vercel-project>.vercel.app/predict"
st.title("✈️ Quick Passenger Predictor")
st.write("A lightweight model using the top 8 predictive features.")

with st.form("prediction_form"):
    st.subheader("Flight Info")

    col1, col2, col3 = st.columns(3)

    with col1:
        customer_type = st.selectbox(
            "Customer Type",
            ["Loyal Customer", "disloyal Customer"]
        )

    with col2:
        travel_type = st.selectbox(
            "Type of Travel",
            ["Personal Travel", "Business travel"]
        )

    with col3:
        flight_class = st.selectbox(
            "Class",
            ["Eco", "Eco Plus", "Business"]
        )

    st.subheader("Service Ratings (0-5)")

    r_col1, r_col2 = st.columns(2)

    with r_col1:
        wifi = st.slider("Inflight wifi service", 0, 5, 3)
        boarding = st.slider("Online boarding", 0, 5, 3)
        entertainment = st.slider("Inflight entertainment", 0, 5, 3)

    with r_col2:
        seat = st.slider("Seat comfort", 0, 5, 3)
        leg_room = st.slider("Leg room service", 0, 5, 3)

    submit = st.form_submit_button("Predict Satisfaction")

if submit:

    payload = {
        "Type_of_Travel": travel_type,
        "Class": flight_class,
        "Customer_Type": customer_type,
        "Inflight_wifi_service": wifi,
        "Online_boarding": boarding,
        "Inflight_entertainment": entertainment,
        "Seat_comfort": seat,
        "Leg_room_service": leg_room
    }

    try:
        with st.spinner("Analyzing passenger satisfaction..."):

            response = requests.post(
                API_URL,
                json=payload,
                timeout=60
            )

            response.raise_for_status()
            result = response.json()

            prediction = result.get("prediction")

            if prediction == "satisfied":
                st.success("Result: The passenger is Satisfied! 🎉")
            elif prediction:
                st.warning(f"Result: The passenger is {prediction.title()}. 😞")
            else:
                st.error(f"Unexpected API response: {result}")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to FastAPI backend.")

    except requests.exceptions.Timeout:
        st.error("API request timed out. Please try again.")

    except requests.exceptions.HTTPError as e:
        st.error(f"API HTTP Error: {e}")
        st.write(response.text)

    except Exception as e:
        st.error(f"An error occurred: {e}")

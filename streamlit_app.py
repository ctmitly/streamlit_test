import streamlit as st 
import requests

# Set the app title 
st.title('Congrats! You now can code HERE in StreamLit') 

# Add a welcome message 
st.write('Welcome to Streamlit app!') 

# Create a text input 
widgetuser_input = st.text_input('Enter a custom message:', 'Hello, Streamlit!') 

# Display the customized message 
st.write('Customized Message:', widgetuser_input)


#API calls
response = requests.get('https://api.vatcomply.com/rates?base=MYR')

# if response.status_code == 200:
#     data = response.json()
#     st.write('Output:')
#     st.json(data)  # nicely formatted JSON output

if response.status_code == 200:
    data = response.json()
    st.write('Output:')
    
    # Extract currency rates
    rates = data['rates']
    
    # Create a dropdown for currency selection
    selected_currency = st.selectbox('Select a currency:', list(rates.keys()))
    
    # Display the selected currency rate
    st.write(f'The exchange rate for {selected_currency} is: {rates[selected_currency]}')
    
    # Display the full JSON data
    st.json(data)  # nicely formatted JSON output

else:
    st.error(f"API call failed with status code: {response.status_code}")



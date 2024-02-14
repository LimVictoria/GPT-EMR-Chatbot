import openai
import streamlit as st
from streamlit_chat import message

openai.api_key = st.secrets["api_secret"]


# creating a function which will generate the calls from the api
def generate_response(prompt, temperature):
    try:
        completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",  # This should match the available chat models
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        # Extract the response message
        message_content = completions.choices[0].message['content']
        return message_content
    except Exception as e:
        return f"Error: {e}"


# Main Streamlit code
def main():
    # Clear the generated responses from the previous session
    #st.session_state['generated'] = []

    # Create a slider for temperature
    temperature = st.sidebar.slider('Temperature', min_value=0.1, max_value=1.0, step=0.1, value=0.5)

    st.title("GPT–EMR Chatbot")

    def get_text():
        input_text = st.text_area("Medical Inquiries: ", key="input")
        return input_text

    user_input = get_text()

    if user_input:
        # Generate response
        response = generate_response(user_input, temperature)

        # Display response
        message(user_input, is_user=True)  # Displaying user input
        message(response)  # Displaying generated response

        # Store the output
        st.session_state['past'].append(user_input)  # This is the user input (prompt)
        st.session_state['past'].append(response)  # This is the generated response

    # create empty container to store the chat
    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if st.session_state['past']:
        for i in range(len(st.session_state['past'])):
            is_user = i % 2 == 0  # True if i is even, False if i is odd
            key = str(i) + ('_user' if is_user else '_generated')
            message(st.session_state['past'][i], is_user=is_user, key=key)





if __name__ == '__main__':
    main()

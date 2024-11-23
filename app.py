import streamlit as st
import os
import requests
from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv(find_dotenv())

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "API_KEY"

# Initialize the model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Streamlit app header
st.write("Leetcode Roaster - Get Ready to be Roasted ")

# Input for Leetcode username
username = st.text_input("Enter Leetcode username")

API = "https://leetcode-stats-api.herokuapp.com/"

if username is not None:
    url = f"{API}{username}"  # Construct API URL

    try:
        # Make the GET request
        response = requests.get(url)
        data = response.json()  # Parse the JSON response

        # Check if the response is successful
        if data["status"] == "success":
            # Remove "SubmissionCalendar" key if it exists
            if "submissionCalendar" in data:
                del data["submissionCalendar"]
            
            # Create the roasting prompt
            template = '''
            Give me a most brutal and most dark humor, bad language roast on this Leetcode stats:
            {response}
            '''
            prompt = PromptTemplate(template=template, input_variables=["response"])
            formatted_prompt = prompt.format(response=data)  # Use parsed data

            # Generate roast using the LLM
            display = None
            roast = llm.invoke(formatted_prompt)
            
            print(roast.content)
            display = roast.content
            # display = roast["content"]
            st.write(display)
        else:
            st.error("Wrong Username! Please check again.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")

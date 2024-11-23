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

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

st.title("Leetcode Roaster")
st.write("Get Ready to be Roasted")

username = st.text_input("Enter Leetcode username")

API = "https://leetcode-stats-api.herokuapp.com/"


url = f"{API}{username}"
try:

    response = requests.get(url)
    data = response.json() 

    if data["status"] == "success":

        if "submissionCalendar" in data:
            del data["submissionCalendar"]
        

        template = '''
        Give me a most brutal and most dark humor, bad language roast on this Leetcode stats:
        {response}
        '''
        prompt = PromptTemplate(template=template, input_variables=["response"])
        formatted_prompt = prompt.format(response=data)  

        st.write("-Generating may take some time-")
        roast = llm.invoke(formatted_prompt)
        
        # print(roast.content)
        display = roast.content
        # display = roast["content"]
        st.write(display)
    else:
        st.error("Wrong Username! Please check again.")
except requests.exceptions.RequestException as e:
    st.error(f"An error occurred: {e}")

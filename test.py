from dotenv import load_dotenv
import os

load_dotenv()  # Loads the .env file

# Access the variables
api_key = os.getenv("API_KEY")
debug = os.getenv("DEBUG") == "True"


print(api_key)
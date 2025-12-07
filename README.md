## Project2 Part 2 — LLM-Only System

Replace the entire architecture with a single, prompt-driven LLM system.  
Goal: see how well a powerful LLM can understand recipes and support conversational interaction without explicit rules.

### Requirements:
google-genai  
python-dotenv  
beautifulsoup4  
requests

### LLM Setup (Gemini API)  
Use Google’s Gemini API to build and test recipe assistant.

**Step 1 — Create an API Key**  
Go to Google AI StudioLinks to an external site.  
Sign in with your Google account.  
Create a Gemini API key and copy it — you’ll need it for authentication.  

**Step 2 — Save Your API Key Securely**  
Create a file named `.env` in your project directory and add the following line:  
```
GEMINI_API_KEY=your_api_key_here
```
This keeps your key private and prevents it from being hardcoded in your scripts.
Make sure that your `.env` file is included in your `.gitignore` so it is not pushed to GitHub.  

To load the API key from your `.env` file in Python, use the python-dotenv library:  

**Step 3 — Install Required Libraries**
Install the necessary dependencies:
```
pip install google-genai python-dotenv
```
google-genai — official client for accessing Gemini models
python-dotenv — loads environment variables from your .env file

**Step 4 — Load the API Key and Initialize the Client**
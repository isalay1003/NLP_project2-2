from dotenv import load_dotenv
import os
from google import genai
from web_scraper import fetch

if __name__ == "__main__":
    url = input("Enter recipe url: ")
    if url == "":
        url = "https://www.allrecipes.com/recipe/6701/persimmon-bread-i/"
        # url = "https://www.allrecipes.com/recipe/219491/to-die-for-chicken-pot-pie/"
        # url = 'https://www.allrecipes.com/recipe/76961/creamy-make-ahead-mashed-potatoes/'
        # url = 'https://www.allrecipes.com/recipe/18282/easy-mushroom-rice/'
        
    title, ingredients, step_texts = fetch(url)
    # print(f"We are now looking at recipe: {title}")
    # print("Please enter the your question.\n")
    
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
    client = genai.Client(api_key=api_key)

    
    prompt = f'''I am looking at the recipe of {title}\nThis is the ingredient list: {ingredients}
These are the steps:\n{step_texts}
Next, I will ask you questions about this recipe.'''
    # print(prompt)
    
    chat = client.chats.create(model="gemini-2.5-flash")
    response = chat.send_message_stream(prompt)
    for chunk in response:
        print(chunk.text, end="")
        

    user_input = input("\n\n- User: ")
    while user_input != "":
        response = chat.send_message_stream(user_input)
        for chunk in response:
            print(chunk.text, end="")
        user_input = input("\n\n- User: ")
    
    print("Quit")
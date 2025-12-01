## Part 2 — LLM-Only System

### Deliverables for Part 2
You will turn in:
- Your code (in a .zip file).
    - This should include the code that:
        - Accepts a recipe URL from the user
        - Scrapes the recipe page
        - Sends relevant content to the LLM and returns an answer
    - Include any prompt(s) you used for the LLM.
    - Similarly to project 1 and project 2 part 1, a readme.txt with link to your GitHub repo.
- Conversation analysis examples (.pdf with text and screenshots):
    - 3 example conversations where the LLM-only approach performs better than your rules-based system.
    For each of these 3, write 1–3 sentences explaining why the LLM did better (e.g., handled ambiguity, answered open-ended cooking questions, better intent recognition, did not require an explicit and rigid parse to understand recipe information, etc.).
    - 3 example conversations where the LLM-only approach fails or struggles.
    For each of these 3, write 1–3 sentences explaining why you think it failed (e.g., hallucinated a step, lost track of state, gave unsafe advice, misunderstood what “that” referred to, etc.).
    These failure examples do not have to be cases that your rules-based system could handle — they can just be cases where the LLM itself breaks.
- You should also list the model name and settings (e.g. gemini-2.5-flash-lite, temperature, etc.) used for each conversation.
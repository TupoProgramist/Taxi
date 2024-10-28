import groq
import re

# Get the job ID for tracking
job_id = job["id"]
print(f"Job ID: {job_id}")

class AI:
    def __init__(self, api):
        self.api = api
        self.model = "llama3-groq-70b-8192-tool-use-preview"
        self.temperature = 0.2
        self.client = groq.Client(api_key=self.api)
        self.session = self.client.create_session()
    
    def extract_keywords(self, user_input):
        
        prompt = f"{user_input}\n 
        Це запит користувача. Виділи з нього ключові слова у списку []"
        
        completion = self.client.chat.completions.create(
            model = self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature = self.temperature,
            max_tokens=6000,
            top_p=1,
            stream=False,
            stop=None
        )
        
        # Get the response text
        answer = completion.choices[0].message
        keyword_list = re.findall(r'\[([^\]]*)\]', answer)
        
        if keyword_list:
            # Split the keywords into a Python list (assuming they are comma-separated)
            keywords = keyword_list[0].split(',')
            # Clean up any extra whitespace around the keywords
            keywords = [kw.strip() for kw in keywords]
        else:
            keywords = []  # If no keywords are found, return an empty list

        # Validate based on the answer
        return keywords
    
    def derive_keywords(self, keywords):
        prompt = f"Проаналізуй текст каналу. Він про можливості, стипендії, гранти, фонд,и подібне? \n Відповідь тільки 0 or 1. \n{combined_posts}"
        
        completion = self.client.chat.completions.create(
            model = self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=6000,
            top_p=1,
            stream=False,
            stop=None,
        )
        
        # Get the response text
        answer = completion.choices[0].message
        #response['choices'][0]['message']['content'].strip().lower()
        
        # Validate based on the answer
        return answer.content
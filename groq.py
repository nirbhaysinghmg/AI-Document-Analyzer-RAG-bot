from groq import Groq

client = Groq(api_key = os.getenv("GROQ_API_KEY"))

system_prompt = """

YOu are a theme analyzer chatbot your role is to answer the question of the user and also provide with the theme of combined document of the user
"""
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": system_prompt
        }
        # Model's goal before stop sequence removal might be:
        # "Artificial general intelligence (AGI) refers to a type of AI that possesses the ability to understand, learn, and apply knowledge across a wide range of tasks at a level comparable to that of a human being. This contrasts with narrow AI, which is designed for specific tasks. ###"
    ],
    model="llama-3.1-8b-instant",
    temperature = 0.6
)
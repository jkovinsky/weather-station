from google import genai
import os, json


GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")



def gen_forecast_summary(forecast):
    client = genai.Client(api_key=GEMINI_API_KEY)
    client_response = ""
    try:

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            config={
                "system_instruction" : "Only output a summary of the weather forecast"
            },
            contents=f"Provide a concise summary of the weather forecast: {forecast}"
        )
      
        client_response = response.text
        return client_response
    except Exception as error:
        print(f"Unexpected: {error}")
    
    return client_response
    
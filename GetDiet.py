import openai
openai.api_key = "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"
def getdietchart(performance):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Create a diet chart according to indian diet if number of reps in exercise increased by {performance}%",
    temperature=0.3,
    max_tokens=200,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )
  generated_text = response.choices[0].text
  return generated_text 

import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')


def prompt_GEMINI():
    prompt = "Suggest 2 projects on AI in healthcare, with objective, data, and methods."
    response =  model.generate_content(prompt)
    topics = response.text.strip().split("\n")
    output = ""
    for topic in topics:
        output += f"- {topic}\n"
    return output

def update_readme(topics_text):
    with open("README.md", "r") as file:
        content = file.readlines()

    # Find where to insert topics (e.g., under markers `<!--C++_TOPICS-->`)
    start_index = content.index("<!--C++_TOPICS-->\n") + 1
    end_index = content.index("<!--END_C++_TOPICS-->\n")
    
    # Update the README with new topics
    content = content[:start_index] + [topics_text] + content[end_index:]
    with open("README.md", "w") as file:
        file.writelines(content)

if __name__ == "__main__":
    response = prompt_GEMINI()
    update_readme(response)

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_cpp_learning_topics():
    prompt = "Suggest 5 interesting topics to learn about C++ for a beginner to intermediate learner."
    response = openai.Completion.create(
        engine="text-davinci-003",  # Or the latest model available to you
        prompt=prompt,
        max_tokens=100
    )
    suggestions = response.choices[0].text.strip().split("\n")
    return suggestions

def format_topics(topics):
    topics_text = "### Suggested C++ Topics to Learn\n\n"
    for topic in topics:
        topics_text += f"- {topic}\n"
    return topics_text

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
    cpp_topics = get_cpp_learning_topics()
    topics_text = format_topics(cpp_topics)
    update_readme(topics_text)

import os
import textwrap
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont, ImageOps


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')


def generate_tile(tileCount, text):
    # Create a 200x200 pixel image with RGBA mode for transparency
    image = Image.new("RGBA", (200, 200), (255, 192, 203, 128))  # Pink color with 50% opacity
    draw = ImageDraw.Draw(image)  # Initialize drawing context
    font = ImageFont.truetype("arial.ttf", 16)  # Define the text and font 

    # Word wrap the text within a specified width
    wrapped_text = "\n".join(textwrap.fill(line, width=15) for line in textwrap.wrap(text, width=15))

    # Calculate text position to center it using textbbox
    text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (200 - text_width) // 2
    text_y = (200 - text_height) // 2
    draw.multiline_text((text_x, text_y), wrapped_text, fill="black", font=font, align="center") # Draw the wrapped text in the center
    corner_radius = 30  # Adjust the radius as needed
    mask = Image.new("L", (200, 200), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, 200, 200), radius=corner_radius, fill=255)
    rounded_image = ImageOps.fit(image, (200, 200), centering=(0.5, 0.5))
    rounded_image.putalpha(mask)
    rounded_image.save(f"resources/image{str(tileCount)}.png")


def prompt_GEMINI():
    prompt = "Suggest 2 projects on AI in healthcare, with objective, data, and methods."
    response =  model.generate_content(prompt)
    topics = response.text.strip().split("\n")
    for i,item in enumerate(topics):
        generate_tile(i+1, item)
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

import openai
import os
from flask import Flask, render_template, request
from dotenv import dotenv_values
import json

config = dotenv_values(".env")

openai.api_key = config["OPENAI_API_KEY"] or os.getenv("OPENAI_API_KEY")

app = Flask(__name__,
            template_folder='templates',
            static_url_path='',
            static_folder='static'
            )


def get_colours(description):
    prompt = f"""
        You are a color palette generating machine. You are given a sentence and you have to generate a color palette for it. Return the colors in a JSON array of hex colors.
        Generate color palettes that fit the theme, mood or instruction in the prompt.
        The Palette should provide between 4 and 8 colors.

        Q: Convert the following description of a color palette into a color palette: healthy leaves
        A: ["#3D550C", "#81B622", "#ECF87F", "#59981A"]

        Q: Convert the following description of a color palette into a color palette: pastel dreams
        A: ["#FBE7C6", "#B4F8C8", "#A0E7E5", "#FFAEBC"]

        Q: Convert the following description of a color palette into a color palette: {description}
        A:
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    colors = json.loads(response.choices[0].text)
    return colors


@ app.route('/palette', methods=["POST"])
def fetch_palette():
    query = request.form.get("query")
    received_colors = get_colours(query)
    return {"colors": received_colors}


@ app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

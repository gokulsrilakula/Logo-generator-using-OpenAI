from flask import Flask, render_template, request, send_from_directory
import openai
from PIL import Image
import requests
from io import BytesIO
import os

app = Flask(__name__)
openai.api_key = 'your_api_key' 

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        project_name = request.form['project_name']
        tagline = request.form['tagline']
        num_logos = int(request.form['num_logos'])
        generate_logos(project_name, tagline, num_logos)
        return render_template('index.html', logos=os.listdir('static/logos'), num_logos=num_logos)
    return render_template('index.html', logos=[], num_logos=0)

def generate_logos(project_name, tagline, n=5):
    for i in range(n):
        prompt = f"Create a logo with the words '{project_name}' and an optional tagline '{tagline}' in a modern style."
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        if not os.path.exists('static/logos'):
            os.makedirs('static/logos')
        img.save(f'static/logos/gemini_logo_{i+1}.png')

@app.route('/static/logos/<filename>')
def send_logo(filename):
    return send_from_directory('static/logos', filename)

if __name__ == '__main__':
    app.run(debug=True)

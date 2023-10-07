from flask import Flask, render_template, request, redirect, url_for
# To start using this app, you first need to type in the terminal 'pip install requests'
import requests

app = Flask(__name__)

api_key = 'bDnEbbqzPLaaok4ule1hMl3UdXx8fNZ1'
base_url = 'https://api.nytimes.com/svc/topstories/v2/'


@app.route('/', methods=['GET', 'POST'])
def get_top_stories():
    if request.method == 'POST':
        section = request.form['section']
        return redirect(url_for('get_top_stories', section=section))

    section = request.args.get('section', 'home')

    endpoint = f'{base_url}{section}.json'
    params = {'api-key': api_key}

    response = requests.get(endpoint, params=params)
    data = response.json()

    section_title = section

    articles = data.get('results', [])[:4]
    return render_template('index.html', articles=articles, section_title=section_title)


@app.route('/update_section', methods=['POST'])
def update_section():
    section = request.form['section']
    return redirect(url_for('get_top_stories', section=section))


if __name__ == '__main__':
    app.run()
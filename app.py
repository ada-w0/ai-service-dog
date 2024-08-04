from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Service Dog</title>
        <link rel="stylesheet" type="text/css" href="/static/style.css">
    </head>
    <body>
        <h1>AI Service Dog</h1>
        <h3>ASD: A technological solution to help warn visually impaired people of moving cars and approaching objects using AI.</h3>
        <h3>Test ASD! Flip your camera and walk up close to a wall, or point your camera toward a street with moving cars.</h3>
        <h3>Coded in Python (Flask) and HTML for Katy Youth Hacks! More CSS and website text-to-speech to be added soon.</h3>
        <br>
        <button onclick="openScript()">Start AI Service Dog U•(ω)•U</button>
        <br>
        <br>
        <br>
        <p>Created by Ada Wang wang-ada000</p>
        <script>
            function openScript() {
                window.open('/run-script', '_blank');
            }
        </script>
    </body>
    </html>
    '''

@app.route('/run-script')
def run_script():
    # Path to your Python script
    script_path = 'YOURLOCALPATHHERE'
    subprocess.Popen(['python', script_path])
    return 'Script is running (´▽`ʃ♡ƪ)! ASD is detecting...'

if __name__ == '__main__':
    app.run(port=5000)

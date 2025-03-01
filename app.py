from flask import Flask, request, jsonify, send_from_directory
from actions import bp as actionsbp
from filters import bp as filtersbp
from android import bp as androidbp
from helpers import allowed_extension, get_secure_filename_filepath


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

app.secret_key = 'SECRET_KEY'

app.register_blueprint(actionsbp)
app.register_blueprint(filtersbp)
app.register_blueprint(androidbp)


@app.route('/')
def index():
    return jsonify({
        'message': 'Welcome to my image API',
        '/images': 'To upload or get images',
        '/actions': {
            '/resize': {
                "filename": "image.png",
                "width": "300",
                "height": "200"
            },
            'preste/:name': {
                "filename": "image.png"
            },
            'rotate': {
                "filename": "image.png",
                "degree": "45"
            },
            '/flip': {
                "filename": "image.png",
                "direction": "horizontal"
            }
        },
        '/filters/blur': {
            "filename": "image.png",
            "radius": 4
        },
        '/android': {
            "filename": "image.png"
        }
    })



@app.route('/images', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':

        if 'file' not in request.files:
            return jsonify({'error': 'No file was selected'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file was selected'}), 400

        if not allowed_extension(file.filename):
            return jsonify({'error': 'The extension is not supported.'}), 400
        
        filename, filepath = get_secure_filename_filepath(file.filename)
        
        file.save(filepath)
        return jsonify({
            'message': 'File successfully uploaded',
            'filename': filename,
        }), 201


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

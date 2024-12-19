from flask import Flask, request, jsonify
from actions import bp as actionsbp
from helpers import allowed_extension, get_secure_filename_filepath


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

app.secret_key = 'SECRET_KEY'

app.register_blueprint(actionsbp)


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

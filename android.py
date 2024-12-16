from flask import Blueprint


bp = Blueprint('android', __name__)

@bp.route('/android', methods=["POST"])
def create_images():
    pass

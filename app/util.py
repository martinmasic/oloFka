from flask import make_response, jsonify
from flask.json import JSONEncoder
from werkzeug.security import generate_password_hash, check_password_hash


class CustomJSONEncoder(JSONEncoder):
	def default(self, obj):
		if hasattr(obj, 'jsonize'):
			return obj.jsonize()
		else:
			return super().default(obj)


def make_password_hash(password):
	return generate_password_hash(password, 'pbkdf2:sha512:100000', salt_length=12)


def make_error_response(message, status_code):
	return jsonify({'message': message}), status_code

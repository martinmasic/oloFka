from flask import jsonify, request

from app import app
from app.logic import *
from app.security import *


@app.route('/users', methods=['POST'])
def create_user_route():
	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')
	email = request.form.get('email')
	password = request.form.get('password')
	

	user = create_user(first_name, last_name, email, password)

	if user is not None:
		return '', 201
	else:
		return make_error_response('Fail', 400)


@app.route('/auth', methods=['POST'])
def auth_user_route():
	email = request.form.get('email')
	password = request.form.get('password')

	user = authenticate_user(email, password)

	if user is not None:
		return jsonify(generate_access_token(user.id))
	else:
		return make_error_response('Invalid user credentials', 403)


@app.route('/projects', methods=['GET'])
@jwt_required
def list_projects_route():
	return jsonify({'projects': list_projects(active_user().id)})


@app.route('/projects', methods=['POST'])
@jwt_required
def create_project_route():
	name = request.form.get('name')
	description = request.form.get('description')
	project = create_project(active_user().id, name, description)

	if project is not None:
		return '', 201
	else:
		return make_error_response('Fail v2', 400)


@app.route('/projects/<project_id>', methods=['GET'])
@jwt_required
def list_project_documents_route():
	project = Project.get_by_id(project_id)
	if project.author == active_user().id:
		return jsonify({'project_documents': list_project_documents_route(project)}) 



@app.route('/documents', methods=['GET'])
@jwt_required
def list_documents_route():
	return jsonify({'documents': list_documents()})


#TODO finish this
@app.route('/projects/<project_id>', methods=['POST'])
@jwt_required
def create_project_document_route():
	title = request.form.get('title')
	document_type = request.form.get('document_type')
	revision = request.form.get('revision')
	#visibility
	place_in_project = request.form.get('place_in_project') #TODO how to find this automagically?
	
	document = create_document(project_id, title, active_revision, place_in_project, document_type)









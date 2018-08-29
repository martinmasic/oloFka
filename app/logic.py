from datetime import datetime

from app.models import *
from app.util import *


def create_user(first_name, last_name, email, password, date_of_birth=None,
				birthplace=None, occupation=None, profile_image=None):
	try:
		user = User.create(
			first_name=first_name, last_name=last_name, email=email, 
			password_hash=make_password_hash(password), date_of_birth=date_of_birth,
			birthplace=birthplace, occupation=occupation, profile_image=profile_image
		)
		return user
	except IntegrityError as e:
		return None


def authenticate_user(email, password):
	user = User.get_or_none(User.email == email)
	if user is not None and check_password_hash(user.password_hash, password):
		return user
	else:
		return None


def update_user(user_id, first_name=None, last_name=None, email=None, date_of_birth=None,
				birthplace=None, occupation=None, profile_image=None, visibility=None, access_level=None):
	try:
		data = {
			'first_name': first_name, 'last_name': last_name, 'email': email,
			'date_of_birth': date_of_birth, 'birthplace': birthplace,
			'occupation': occupation, 'profile_image': profile_image, 
			'visibility': visibility, 'access_level': access_level
		}

		return User.update({k: v for k, v in data if v is not None}).where(User.id == user_id).execute() > 0
	except IntegrityError as e:
		return False


def change_user_password(user_id, old_password, new_password):
	user = User.get_or_none(User.id == user_id)
	if user is not None and check_password_hash(user.password_hash, old_password):
		user.password_hash = make_password_hash(new_password)
		user.save()
		return True
	else:
		return False


# def delete_user(user_id):
#	... revisions
# 	Document.delete().where(Document.project.author_id == user_id).execute()
# 	... projects
# 	... document_tags
# 	... project_tags
# 	... tags
# 	... user_settings
# 	... user


def list_projects(user_id):
	return list(Project.select().where(Project.author_id == user_id))


def create_project(user_id, name, description=None):
	project = Project.create(
		author_id=user_id, time_created=datetime.now(), name=name, description=description
	)
	return project


def update_project(project_id, name=None, description=None, visibility=None):
	data = {
		'name': name, 'description': description, 'visibility': visibility
	}
	return Project.update({k: v for k, v in data if v is not None}).where(Project.id == project_id).execute() > 0


def delete_project(project_id):
	for document in list_project_documents(project_id):
		delete_document(document.id)
	ProjectTag.delete().where(ProjectTag.project == project_id).execute()
	Project.delete().where(Project.id == project_id)


def create_document(project_id, title, active_revision, place_in_project, document_type=DocumentType.GENERIC):
	document = Document.create(
		project_id=project_id, title=title, time_created=datetime.now(), document_type=document_type,
		place_in_project=place_in_project
	)
	revision = Revision.create(document=document.id, time_created=datetime.now())
	Document.update(active_revision=revision).where(Document.id == document.id).execute()
	# can I access document.id? if so, can I asccess document.active_revision? if so, will the change propagate to
	# Document ?
	return document


def update_document(document_id, title=None, document_type=None, active_reision=None, visibility=None):
	data = {
		'project': project, 'title': title, 'document_type': document_type, 'active_revision': active_revision,
		'visibility': visibility, 'place_in_project': place_in_project
	}
	return Document.update({k: v for k, v in data if v is not None}).where(Document.id == document_id).execute() > 0


def delete_document(document_id):
	Revision.delete().where(Revision.document == document_id).execute()
	DocumentTag.delete().where(DocumentTag.document == document_id).execute()
	Document.delete().where(Document.id == document_id).execute()


def list_project_documents(project_id):
	return list(Document.select().where(Document.project == project_id))


def create_revision(document_id, content):
	revision = Revision.create(
		document_id=document_id, time_created=datetime.now(), content=content
	)
	return revision


def update_revision(revision_id, content):
	return Revision.update({'time_created': datetime.now(), 'content': content}).where(Revision.id == revision_id).execute() > 0


def delete_revision(revision_id):
	Revision.delete().where(Revision.id == revision_id).execute()


def create_tag(user_id, name):
	tag = Tag.create(
		user=user_id, name=name
	)
	return tag


def update_tag(tag_id, name):
	return Tag.create({'name': name}).where(Tag.id == tag_id).execute() > 0


def delete_tag(tag_id):
	DocumentTag.delete().where(DocumentTag.tag == tag_id).execute()
	ProjectTag.delete().where(ProjectTag.tag == tag_id).execute()
	Tag.delete().where(Tag.id == tag_id).execute()


def create_document_tag(document_id, tag_id):
	document_tag = DocumentTag.create(
		document=document_id, tag=tag_id
	)
	return document_tag	


# def update_document_tag()


def delete_document_tag(document_tag_id):
	DocumentTag.delete().where(DocumentTag.id == document_tag_id).execute()


def create_project_tag(project_id, tag_id):
	project_tag = ProjectTag.create(
		project=project_id, tag=tag_id
	)
	return project_tag


# def update_project_tag()


def delete_project_tag(project_tag_id):
	ProjectTag.delete().where(ProjectTag.id == project_tag_id).execute()






from peewee import *

db = SqliteDatabase("store.db")


class BaseModel(Model):
	class Meta:
		database = db

	def jsonize(self):
		if not hasattr(self, '_json_fields'):
			klass = self.__class__
			self._json_fields = [a for a in dir(klass) if isinstance(getattr(klass, a), Field)]

		return {k: getattr(self, k) for k in self._json_fields}


class Visibility:
	PRIVATE = 0
	PUBLIC = 1


class AccessLevel:
	BASIC = 1
	ADMIN = 2


class DocumentType:
	GENERIC = 0
	POEM = 1
	ESSAY = 2
	PLAY = 3
	NOVEL = 4
	SHORT_STORY = 5


class User(BaseModel):
	first_name = CharField()
	last_name = CharField()
	email = CharField(unique=True)
	password_hash = CharField()
	date_of_birth = DateField(null=True)
	birthplace = CharField(null=True)
	occupation = CharField(null=True)
	profile_image = CharField(null=True)
	visibility = IntegerField(default=Visibility.PRIVATE)
	access_level = IntegerField(default=AccessLevel.BASIC)

	def jsonize(self):
		return {
			'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name,
			'email': self.email, 'date_of_birth': self.date_of_birth, 'birthplace': self.birthplace,
			'occupation': self.occupation, 'profile_image': self.profile_image
		}
	

class Project(BaseModel):
	author = ForeignKeyField(User, backref="projects")
	time_created = DateTimeField()
	name = CharField()
	description = TextField(null=True)
	visibility = IntegerField(default=Visibility.PRIVATE)


class Document(BaseModel):
	project = ForeignKeyField(Project, backref="documents")
	title = CharField()
	time_created = DateTimeField()
	document_type = CharField()
	active_revision = DeferredForeignKey("Revision", null=True)
	visibility = IntegerField(default=Visibility.PRIVATE)
	place_in_project = IntegerField()


class Revision(BaseModel):
	document = ForeignKeyField(Document, backref="revisions")
	time_created = DateTimeField()
	content = TextField(null=True)


class Tag(BaseModel):
	user = ForeignKeyField(User, backref="tags")
	name = CharField()


class DocumentTag(BaseModel):
	document = ForeignKeyField(Document, backref="tags")
	tag = ForeignKeyField(Tag, backref="documents")


class ProjectTag(BaseModel):
	project = ForeignKeyField(Project, backref="tags")
	tag = ForeignKeyField(Tag, backref="projects")


class UserSettings(BaseModel):
	pass


if __name__ == "__main__":
	db.create_tables([User, Project, Document, Revision, Tag, DocumentTag, ProjectTag, UserSettings], safe=True)


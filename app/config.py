from datetime import timedelta

DEBUG = True
SECRET_KEY = '1234567890123456789'  # TODO: Use something real
JWT_EXPIRATION_DELTA = timedelta(days=30)
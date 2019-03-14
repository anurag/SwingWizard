import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  ADMINS = ['your-email@example.com']
  UPLOAD_FOLDER = basedir+'/app/static/uploads'
  ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','mp4'])

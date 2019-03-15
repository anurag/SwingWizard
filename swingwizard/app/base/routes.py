from app import *
from app.base import *
from app.helpers import *
from app.models import User
from app.auth.forms import *
from flask import *
from io import BytesIO
from fastai import *
from fastai.vision import *
from flask_login import current_user,login_user,logout_user,login_required
from werkzeug.urls import url_parse



@bp.route('/')
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('base.user',username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('base.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('base.user',username=current_user.username)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    path = Path(str(basedir+f'/app/static/uploads/{current_user.username}'))
    if os.path.exists(path):
      if len(get_files(path))>0:
        for x in get_files(path): os.remove(x)
      os.rmdir(path)
    logout_user()
    return redirect(url_for('base.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('base.user'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered')
        return redirect(url_for('base.login'))
    return render_template('register.html', title='Register', form=form)


# @bp.route('/')
# @bp.route('/home/<username>', methods=['GET', 'POST'])
# @login_required
# def home(username):
#   user = User.query.filter_by(username=username).first_or_404()
#   path = Path(str(basedir+f'/app/static/uploads/{current_user.username}'))
#   if not os.path.exists(path): os.makedirs(path)
#   return render_template('user.html',user=user)


@bp.route('/home/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    path = Path(str(basedir+f'/app/static/uploads/{current_user.username}'))
    if not os.path.exists(path): os.makedirs(path)
    return render_template('user.html', user=user)


@bp.route('/inputvideo/<username>',methods=['GET','POST'])
@login_required
def input_video(username):
  user = User.query.filter_by(username=username).first_or_404()
  path = Path(str(basedir+f'/app/static/uploads/{current_user.username}'))
  if not os.path.exists(path): os.makedirs(path)
  if os.path.exists(path):
    if len(get_files(path))>0:
      for x in get_files(path): os.remove(x)
  if request.method == 'POST':
    fname = get_filename(path,save=True)
    get_frames(fname)
    frames = get_image_files(path)
    return redirect(url_for('base.uploads_video',username=current_user.username))
  return render_template('inputVideo.html',user=user,username=current_user.username)

@bp.route('/inputimage/<username>',methods=['GET','POST'])
@login_required
def input_image(username):
  user = User.query.filter_by(username=username).first_or_404()
  path = Path(str(basedir+f'/app/static/uploads/{current_user.username}'))
  if not os.path.exists(path): os.makedirs(path)
  if os.path.exists(path):
    if len(get_files(path))>0:
      for x in get_files(path): os.remove(x)
  if request.method == 'POST':
    fname = get_filename(path,save=True)
    frames = get_image_files(path)
    return redirect(url_for('base.uploads_image',username=current_user.username))
  return render_template('inputImage.html',user=user)


@bp.route('/uploadsvideo/<username>')
@login_required
def uploads_video(username):
  user = User.query.filter_by(username=username).first_or_404()
  path = Path(str(basedir+f'/app/static/uploads/{current_user.username}'))
  frames = get_image_files(path)
  lst = [re.compile(r'([^/]+$)').search(str(x)).group(1) for x in frames]
  fnames = [f"{current_user.username}/{x}" for x in lst]
  return render_template('uploadVideo.html',user=user,
                         username=current_user.username,
                         f1=fnames[0],f2=fnames[1],f3=fnames[2],f4=fnames[3],f5=fnames[4])

@bp.route('/uploadsimage/<username>')
@login_required
def uploads_image(username):
  user = User.query.filter_by(username=username).first_or_404()
  path = Path(str(basedir+f'/app/static/uploads/{current_user.username}'))
  frames = get_image_files(path)
  lst = [re.compile(r'([^/]+$)').search(str(x)).group(1) for x in frames]
  fnames = [f"{current_user.username}\\{x}" for x in lst]
  return render_template('uploadImage.html',user=user,
                         username=current_user.username,f1=fnames[0])


@bp.route('/resultsvideo/<username>')
@login_required
def results_video(username):
  user = User.query.filter_by(username=username).first_or_404()
  path = Path(str(basedir+f'/app/static/uploads/{current_user.username}'))
  if not os.path.exists(path): os.makedirs(path)
  frames = get_image_files(path)
  lst = [re.compile(r'([^/]+$)').search(str(x)).group(1) for x in frames]
  fnames = [f"{current_user.username}/{x}" for x in lst]
  f1=fnames[0];p1,c1=get_results(frames,0)
  f2=fnames[1];p2,c2=get_results(frames,1)
  f3=fnames[2];p3,c3=get_results(frames,2)
  f4=fnames[3];p4,c4=get_results(frames,3)
  f5=fnames[4];p5,c5=get_results(frames,4)
  return render_template('resultsVideo.html',user=user,
                         f1=f1,p1=p1,c1=c1,
                         f2=f2,p2=p2,c2=c2,
                         f3=f3,p3=p3,c3=c3,
                         f4=f4,p4=p4,c4=c4,
                         f5=f5,p5=p5,c5=c5)


@bp.route('/resultsimage/<username>')
@login_required
def results_image(username):
  user = User.query.filter_by(username=username).first_or_404()
  path = Path(str(basedir+f'/app/static/uploads/{current_user.username}'))
  if not os.path.exists(path): os.makedirs(path)
  frames = get_image_files(path)
  lst = [re.compile(r'([^/]+$)').search(str(x)).group(1) for x in frames]
  fnames = [f"{current_user.username}/{x}" for x in lst]
  f1=fnames[0];p1,c1=get_results(frames,0)
  return render_template('resultsImage.html',user=user,
                         username=current_user.username,
                         f1=f1,p1=p1,c1=c1)


@bp.route('/deletinguploads/<username>')
@login_required
def deleting_uploads(username):
  user = User.query.filter_by(username=username).first_or_404()
  path = Path(str(basedir+f'/app/static/uploads/{current_user.username}'))
  if not os.path.exists(path): os.makedirs(path)
  for f in get_files(path):
    os.remove(f)
  return redirect(url_for('base.user',username=current_user.username,user=user))

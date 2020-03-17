from application import app, db, api
from flask import render_template, request, json, jsonify, Response, redirect, flash, url_for, session
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm
from flask_restplus import Resource
from application.course_list import course_list

###########################################

@api.route('/api', '/api/')
class GetAndPost(Resource):
  #GET All
  def get(self):
    return jsonify(User.objects.all())

  #POST
  def post(self):
    data = api.payload
    user = User(user_id=data['user_id'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
    user.set_password(data['password'])
    user.save()
    return jsonify(User.objects(user_id=data['user_id']))

@api.route('/api/<idx>')
class GetUpdateAndDelete(Resource):

  #GET ONE
  def get(self, idx):
    return jsonify(User.objects(user_id=idx))

  #Put
  def put(self, idx):
    data = api.payload
    User.objects(user_id=idx).update(**data)
    return jsonify(User.objects(user_id=idx))

  #Delete
  def delete(self, idx):
    User.objects(user_id=idx).delete()
    return jsonify("User has been deleted!")

###########################################

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
  return render_template('index.html', index=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if session.get('username'):
    return redirect(url_for('index'))

  form = LoginForm()
  if form.validate_on_submit():
    email       = form.email.data
    password    = form.password.data

    user = User.objects(email=email).first()
    if user and user.get_password(password):
      flash(f"{user.first_name}, you are successfully logged in!", "success")
      session['user_id'] = user.user_id
      session['username'] = user.first_name
      return redirect('/index')
    else:
      flash("Sorry, something went wrong.", "danger")
  return render_template('login.html', title="Login", form=form, login=True)

@app.route('/logout')
def logout():
  session['user_id'] = False
  session.pop('username', None)
  return redirect(url_for('index'))

@app.route('/courses')
@app.route('/courses/<term>')
def courses(term=None):
  if term is None:
    term = "String 2019"
  classes = Course.objects.order_by("+courseID")
  return render_template('courses.html', courseData=classes, courses=True, term=term)
  

@app.route("/register", methods=['POST','GET'])
def register():
  if session.get('username'):
    return redirect(url_for('index'))

  form = RegisterForm()
  if form.validate_on_submit():
    user_id     = User.objects.count()
    user_id     += 1

    email       = form.email.data
    password    = form.password.data
    first_name  = form.first_name.data
    last_name   = form.last_name.data

    user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.save()
    flash("You are successfully registered!","success")
    return redirect(url_for('index'))
  return render_template("register.html", title="Register", form=form, register=True)

@app.route('/enrollment', methods=["GET","POST"])
def enrollment():

    if not session.get('username'):
      return redirect(url_for('login'))

    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    user_id = session.get('user_id')

    if courseID:
      if Enrollment.objects(user_id=user_id, courseID=courseID):
        flash(f"Oops! Your are already registered in this is course {courseTitle}", "danger")
        return redirect(url_for("courses"))
      else:
        Enrollment(user_id=user_id, courseID=courseID).save()
        flash(f"You are enrolled in {courseTitle}!", "success")

    courses = course_list()

    return render_template("enrollment.html", title="Enrollment", enrollment=True, classes=courses) 

# @app.route('/api/')
# @app.route('/api/<idx>')
# def api(idx=None):
#   if (idx== None):
#     jdata = Course.objects.order_by("+courseID")
#   else:
#     courseData = Course.objects.order_by("+courseID")
#     jdata = courseData[int(idx)]
#   return Response(json.dumps(jdata), mimetype="application/json")

@app.route('/user')
def user():
  #User(user_id=1, first_name="Christian", last_name="Hur", email="christian@uta.com", password="abc1234").save()
  #User(user_id=2, first_name="Mary", last_name="Jane", email="mary.jane@uta.com", password="password123").save()

  users = User.objects.all()
  return render_template('user.html', users=users)
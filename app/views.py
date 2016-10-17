from flask import render_template, url_for, g, session, redirect, flash, request
from flask.ext.stormpath import StormpathError, StormpathManager, User, login_required, login_user, logout_user, user
from app import app, db, stormpath_manager
from .forms import RegisterForm, LoginForm,UnlockForm,AtForm,AqForm
from models import Tut, Quiz
from hashlib import md5

# Default page
@app.route('/')
@app.route('/index')
def startpage():
    tutnames = db.session.query(Tut.name).all()
    tutnames = [tutname for (tutname ,) in tutnames]
    return render_template('startpage.html', tutnames=tutnames)

# Reference for styling
@app.route('/ref')
@login_required
def reference():
    tutnames = db.session.query(Tut.name).all()
    tutnames = [tutname for (tutname ,) in tutnames]
    return render_template('reference.html', tutnames = tutnames)

# Admin page to add new tutorials and quizzes
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    print "Submitting"
    qform = AqForm(prefix="qform")
    form = AtForm(prefix="form")
    if qform.validate_on_submit() and qform.name.data:
        print "Submitting"
        quiz = Quiz(name=qform.name.data, question=qform.question.data, answer=qform.answer.data)
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for('startpage'))
    if form.validate_on_submit() and form.name.data:
        tut = Tut(name=form.name.data, content=form.content.data, question=form.question.data, answer=form.answer.data)
        db.session.add(tut)
        db.session.commit()
        return redirect(url_for('startpage'))
    tutnames = db.session.query(Tut.name).all()
    tutnames = [tutname for (tutname ,) in tutnames]
    return render_template('admin.html', form=form, qform=qform, tutnames = tutnames)
# Tutorial page
@app.route('/tutorial/<tno>', methods=['GET', 'POST'])
@login_required
def tutorial(tno):
    # Check if the user has reached the level
    if g.user.custom_data["tutno"] < int(tno):
        flash("You are not eligible to view this tutorial yet. Unlock this one first.")
        return redirect(url_for('tutorial', tno=g.user.custom_data["tutno"]))
    
    form = UnlockForm()
    t = Tut.query.get(int(tno))
    if form.validate_on_submit():
        if form.answer.data == t.answer:
            g.user.custom_data["tutno"]+=1
            g.user.save()
            if g.user.custom_data["tutno"] > Tut.query.count():
                g.user.custom_data['completed'] = True
                g.user.save()
                flash("Thank you for completing the course")
                return redirect(url_for('startpage'))
            return redirect(url_for('tutorial', tno=g.user.custom_data["tutno"]))
        else:
            flash('Sorry, %r is not the correct answer. Please try again.' % form.answer.data)
    maxt = Tut.query.count()
    tutnames = db.session.query(Tut.name).all()
    tutnames = [tutname for (tutname ,) in tutnames]
    return render_template('tutorial.html', tno = t.id, name=t.name, content=t.content, question=t.question, answer=t.answer, form=form, maxt=maxt, tutnames = tutnames)

@app.before_request
def getuser():
    g.user = user

# Stormpath registration
@app.route('/cregister', methods=['GET','POST'])
def register():
    error = None
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            account = stormpath_manager.application.accounts.create({
            'given_name': form.given_name.data,
            'surname': form.surname.data,
            'username': form.username.data,
            'email': form.email.data,
            'password': form.password.data,
            'custom_data': { 'tutno' : 1, 
                             'completed' : False, 
                             'avatar' : 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(form.email.data.encode('utf-8')).hexdigest(), 128)} 
            })
            _user = User.from_login(
                form.email.data,
                form.password.data,
            )
            login_user(_user, remember=True)
            flash('You were logged in.')
            tutnames = db.session.query(Tut.name).all()
            tutnames = [tutname for (tutname ,) in tutnames]
            return render_template('startpage.html', tutnames=tutnames)
        except StormpathError, err:
            error = err.message
            flash('Please try again' + str(error))
    return render_template('register.html', form=form)

# Logout stormpath
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('startpage'))
# Quizzes
@app.route('/quizzler')
@login_required
def quizzler():
    quizs = Quiz.query.all()
    tutnames = db.session.query(Tut.name).all()
    tutnames = [tutname for (tutname ,) in tutnames]
    return render_template('quizzler.html', quizs=quizs, tutnames = tutnames)
# Individual Quiz page 
@app.route('/quiz/<qno>', methods=['GET','POST'])
@login_required
def quiz(qno):
    form = UnlockForm()
    quiz = Quiz.query.get(int(qno))
    if form.validate_on_submit():
        if form.answer.data == quiz.answer:
            flash("Correct answer")
            return redirect(url_for('quizzler'))
        else:
            flash('Try again')
    tutnames = db.session.query(Tut.name).all()
    tutnames = [tutname for (tutname ,) in tutnames]
    return render_template('quiz.html', quiz=quiz, form=form, tutnames = tutnames)
    
    
# Stormpath login
@app.route('/clogin', methods=['GET','POST'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        try:
            _user = User.from_login(
                form.email.data,
                form.password.data,
            )
            login_user(_user, remember=True)
            flash('You were logged in.')
            tutnames = db.session.query(Tut.name).all()
            tutnames = [tutname for (tutname ,) in tutnames]
            return redirect(url_for('tutorial', tno=g.user.custom_data["tutno"]))
        except StormpathError, err:
            error = err.message
            flash('Please try again')
    return render_template('login.html', form=form)

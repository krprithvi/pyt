from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, RadioField, TextAreaField, HiddenField, PasswordField
from wtforms.validators import DataRequired
# Form for a new user
class RegisterForm(Form):
    given_name = StringField('given_name',validators=[DataRequired()])
    surname = StringField('surname',validators=[DataRequired()])
    username = StringField('username',validators=[DataRequired()])
    email = StringField('email',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
# Form to login
class LoginForm(Form):
    email = StringField('email',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
# Proceed to the next level
class UnlockForm(Form):
    answer = StringField('answer',validators=[DataRequired()])
# Admin adding a tutorial form
class AtForm(Form):
    name = StringField('name',validators=[DataRequired()])
    content = TextAreaField('content',validators=[DataRequired()])
    question = TextAreaField('question',validators=[DataRequired()])
    answer = StringField('answer',validators=[DataRequired()])
# Admin adding a quiz form
class AqForm(Form):
    name = StringField('name',validators=[DataRequired()])
    question = TextAreaField('question',validators=[DataRequired()])
    answer = StringField('answer',validators=[DataRequired()])

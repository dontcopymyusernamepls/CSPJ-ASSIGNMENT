from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from wtforms import Form, SubmitField, PasswordField, IntegerField, FloatField, StringField, TextAreaField, validators, SelectField, BooleanField

class SignupForm(Form):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username =  StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired(), Regexp('^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z]).{8,20}$', message='Password must contain 1 uppercase and lowercase letter, 1 special character [!@#$&*], at least 2 numerical and at least 8 characters.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
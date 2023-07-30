from flask import Flask, render_template,request, redirect, url_for, flash, make_response, abort, Response
from form import SignupForm, LoginForm
from flask import *
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_required, login_user
import shelve, SingpassUser
import pyotp
import smtplib
app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)

Bootstrap(app)
# verifying TOTP codes with PyOTP
# generating TOTP codes with provided secret
totp = pyotp.TOTP("base32secret3232")
print(totp.now())

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "Login"

class Userr(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

users = [Userr(id) for id in range(1, 19)]

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/404")
def error404():
    return render_template('404.html')

@app.route("/booking")
def booking():
    return render_template('booking.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/service")
def service():
    return render_template('service.html')

@app.route("/team")
def team():
    return render_template('team.html')

@app.route("/testimonal")
def testimonal():
    return render_template('testimonal.html')

@app.route("/Userpage")
@login_required
def Userpage():
    return render_template('Userpage.html')

@app.route('/Signup', methods=['GET', 'POST'])
def Users():
    Users_form = SignupForm(request.form)
    if request.method == 'POST' and Users_form.validate():
        Users_dict = {}
        db = shelve.open('Users.db', 'c')
        try:
            Users_dict = db['Users']
        except:
            print("Error in retrieving Users from Users.db.")

        Users = Users.Users(Users_form.first_name.data, Users_form.last_name.data,
                            Users_form.username.data, Users_form.email.data,
                            Users_form.Password.data)
        Users_dict[Users.get_user_id()] = Users
        db['Users'] = Users_dict
        Users_dict = db['Users']
        Users = Users_dict[Users.get_user_id()]
        print(Users.get_first_name(), Users.get_last_name(), "was stored in Users.db successfully with Users_id ==",
              Users.get_user_id())

        db.close()

        flash("account successfully created")
        return redirect(url_for("Userpage"))
    return render_template('signup.html', form=Users_form)

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    UserLogin_form = LoginForm(request.form)
    Users_dict = {}
    db = shelve.open('Users.db', 'r')
    Users_dict = db['Users']
    db.close()

    Users_list = []
    for key in Users_dict:
        Users = Users_dict.get(key)
        Users_list.append(Users)

        break
    if request.method == 'POST' and UserLogin_form.validate():
        if UserLogin_form.username.data == Users.get_username() and UserLogin_form.password.data == Users.get_Password():
            user = Userr(id)
            login_user(user)
            return redirect(request.args.get("next"))
        else:
            return abort(401)

    return render_template('login.html', form=UserLogin_form)

@app.route("/login/2fa/")
def login_2fa():
    # generating random secret key for authentication
    secret = pyotp.random_base32()
    return render_template("login_2fa.html", secret=secret)

@app.route("/login/2fa/", methods=["POST"])
def login_2fa_form():
    # getting secret key used by user
    secret = request.form.get("secret")
    # getting OTP provided by user
    otp = int(request.form.get("otp"))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(request.form.get("otp")):
        # inform users if OTP is valid
        flash("The TOTP 2FA token is valid", "success")
        return redirect("http://127.0.0.1:5000/Userpage")
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token!", "danger")
        return redirect(url_for("login_2fa"))

@login_manager.user_loader
def load_user(userid):
    return Userr(userid)
    
if __name__ == "__main__":
    app.run()


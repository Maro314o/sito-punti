from flask import Blueprint,render_template,request

autenticazione=Blueprint('autenticazione',__name__)

@autenticazione.route('/login',methods=['GET','POST'])
def login():
    email=request.form.get('email')
    password=request.form.get('password')
    print(email,password)

    return  render_template("login.html")

@autenticazione.route("/logout",methods=['GET','POST'])
def logout():
    return render_template("logout.html")

@autenticazione.route("/sign_up",methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        cognome=request.form.get('cognome')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        if email.lower()==f's-{cognome}.{firstName}@isiskeynes.it':
            print('balls')


    return render_template("sign_up.html")
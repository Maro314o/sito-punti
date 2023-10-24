from flask import Blueprint,render_template,request,flash

autenticazione=Blueprint('autenticazione',__name__)

@autenticazione.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
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
        email=(request.form.get('email')).lower()
        firstName=request.form.get('firstName')
        cognome=request.form.get('cognome')
        password=request.form.get('password')
        password_di_conferma=request.form.get('password_di_conferma')
        if '@isiskeynes.it' not in email:
           flash('Il dominio dell\' email é sbagliato',category='error')
        if 's-' not in email:
            flash('hai dimenticato di mettere \'s-\' nell\' email',category='error')
        if email!=f's-{cognome.lower()}.{firstName.lower()}@isiskeynes.it':
            flash('L\'email non corrisponde con il nome e cognome',category='error')
        if len(password)< 5 :
            flash('La password deve essere almeno di 5 caratteri',category='error')
        if password != password_di_conferma:
            flash('La password di conferma non e\' corretta',category='error')
        flash('Account creato con successo!',category='success')




    return render_template("sign_up.html")
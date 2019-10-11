from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)



app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/")
def index():
    template = jinja_env.get_template('base.html')
    return template.render(username='',password='',verifypassword='',email='')


@app.route("/", methods=['POST'])
def validate_user():
    cusername = request.form['username']
    cpassword = request.form['password']
    cverifypassword = request.form['verifypassword']
    cemail=request.form['email']
    cusername_error = ''
    cpassword_error = ''
    cverifypassword_error=''
    cemail_error=''
    csubmit_error=''
    template = jinja_env.get_template('base.html')
    if cusername == '' or cpassword =='' or cverifypassword == '':
        csubmit_error = '* fields are mandatory'
 
    elif len(cusername) < 3 or len(cusername) > 20 or (' ' in cusername ):
            cusername_error = 'username is invalid'
    elif len(cpassword) < 3 or len(cpassword) > 20 or (' ' in cpassword ):
            cpassword_error = 'password is not valid'
    elif cverifypassword != cpassword:
            cverifypassword_error = 'please enter same password as in password field'
            cverifypassword = ''
    elif ('@' not in cemail) or ('.' not in cemail) or (' ' in cemail) or len(cemail)<3 or len(cemail)>20:
            cemail_error = 'Email is not valid'
            cemail=''
    
    if not cusername_error and not cpassword_error and not cverifypassword_error and not csubmit_error and not cemail_error:  
        return redirect('/welcome?username={0}'.format(cusername))
    else:
        return template.render(username=cusername,username_error=cusername_error,
                          password=cpassword,password_error=cpassword_error,
                          verifypassword=cverifypassword,verifypassword_error=cverifypassword_error,email=cemail,
                          email_error=cemail_error,submit_error=csubmit_error)
    


@app.route('/welcome')
def valid_user():
    cusername = request.args.get('username')
    template = jinja_env.get_template('welcome.html')
    return template.render(name=cusername)

app.run()

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from passlib.hash import pbkdf2_sha256
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = 'BLA'
app.config["MYSQL_USER"] = "bf14e622f6f4c1"
app.config["MYSQL_PASSWORD"] = "6d245eb6"
app.config["MYSQL_DB"] = "heroku_8b9c59c73ae5d38"
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        full_name = request.form["full_name"]
        contact_email = request.form["contact_email"]
        message = request.form["message"]
        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO messages (full_name,contact_email,message) VALUES ({full_name!r}, {contact_email!r}, {message!r})")
        mysql.connection.commit()
        flash('You successfully sent us a message :)', category='message_success')
        return render_template("index.html")



@app.route('/artist', methods=['POST', 'GET'])
def artist():
    if request.method == 'GET':
        print("Get")
        return render_template("artist_signup.html")
    else:
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        domain = request.form["domain"]
        experience = request.form["experience"]
        email = request.form["email"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email LIKE %s", [email])  #check id email already exists
        if len(cur.fetchall()) >0:
            flash('Oups! This email already exists!', category='danger')
            return render_template("artist_signup.html")
        else:
            cur.execute(f"INSERT INTO freelancers (first_name,last_name, email,domain, experience) VALUES ({first_name!r}, {last_name!r}, {email!r}, {domain!r}, {experience!r})")
            mysql.connection.commit()
            flash('You successfully joined our artist pool :)', category='success')
            return render_template("index.html")


@app.route('/recruiter_signup', methods=['POST', 'GET'])
def recruiter_signup():
    if request.method == 'GET':
        return render_template('recruiter_signup.html')
    else:
        username = request.form["username"]
        email = request.form["email"]
        # insert the new user into the database:
        password = pbkdf2_sha256.hash(request.form["password"])
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email LIKE %s", [email])  #check id email already exists
        if len(cur.fetchall()) >0:
            flash('Oups! This email already exists!', 'signup_danger')
            return render_template("recruiter_signup.html")
        else:
            cur.execute(f"INSERT INTO users (username, email, password) VALUES ({username!r}, {email!r}, {password!r})")
            mysql.connection.commit()
            session["username"] = request.form["username"]
            session["email"] = request.form["email"]
            flash('You are now signed up :)', "signup_success")
            return redirect(url_for("login"))


@app.route('/recruiter', methods=['POST', 'GET'])
def recruiter():
    if request.referrer is None:
        return redirect(url_for('login'))

    else:
        if session.get("email"):
            curl = mysql.connection.cursor()
            curl.execute("SELECT * FROM projects")
            data = curl.fetchall()
            username = session.get("username")
            domain_dict = {}
            select_stmt = ("SELECT domain ,COUNT(*) FROM freelancers GROUP BY DOMAIN")
            curl.execute(select_stmt)
            tuples=curl.fetchall()
            domain_dic = {}
            for i in range(len(tuples)):
              k = list(tuples[i].values())[0]
              v = list(tuples[i].values())[1]
              domain_dic[k]=v

            get_exp = ("SELECT experience, COUNT(*)  FROM freelancers GROUP BY experience;")
            curl.execute(get_exp)
            tuples=curl.fetchall()
            exp_dic = {}
            for i in range(len(tuples)):
              k = list(tuples[i].values())[0]
              v = list(tuples[i].values())[1]

              exp_dic[k]=float(v)

            curl.close()
            return render_template(
                "recruiter_2.html",
                projects=data,
                domain_dic=domain_dic, exp_dic = exp_dic, username=username)



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor()
        curl.execute("SELECT * FROM users WHERE email LIKE %s", [email])
        user = curl.fetchone()
        curl.close()
        if user is None:
            flash('Oups! This email address does not exist.', category='danger')
            return render_template("recruiter_login.html")

        elif len(user) > 0:
            if pbkdf2_sha256.verify(password, user["password"]):
                session['username'] = user['username']
                session['email'] = user['email']
                check_login = True
                return recruiter()
            else:
                flash('Oups, wrong password!', category='danger')
                return render_template("recruiter_login.html")
    else:
        return render_template("recruiter_login.html")


@app.route('/create_project',methods=['POST', 'GET'])
def create_project():
        if request.method == 'GET':
            return render_template('create_project_2.html')
        else:
            project_title = request.form["project_title"]
            contact_email = request.form["contact_email"]
            project_des = request.form["project_des"]
            skill_level = request.form["skill_level"]
            # insert the new user into the database:
            cur = mysql.connection.cursor()
            cur.execute(f"INSERT INTO projects (project_title, contact_email, project_des, skill_level) VALUES ({project_title!r}, {contact_email!r}, {project_des!r}, {skill_level!r})")
            mysql.connection.commit()
            session["project_title"] = request.form["project_title"]
            session["contact_email"] = request.form["contact_email"]
            session["project_des"] = request.form["project_des"]
            session["skill_level"] = request.form["skill_level"]
            flash('You added a new project', category="success")
            return redirect(url_for("recruiter"))

@app.route('/find_artist',methods=['POST', 'GET'])
def find_artist():
    if session.get("email"):
        curl = mysql.connection.cursor()
        curl.execute("SELECT * FROM freelancers")
        data = curl.fetchall()
        curl.close()
        return render_template(
            "findworkforce.html",
            freelancers=data)
    else:
        return redirect(url_for('login'))

def multiple_buttons(condition):
    if session.get("email"):
        curl = mysql.connection.cursor()
        curl.execute("SELECT * FROM freelancers WHERE domain LIKE %s", [condition])
        data = curl.fetchall()
        curl.close()
        return render_template(
            "findworkforce.html",
            freelancers=data)
    else:
        return redirect(url_for('login'))

@app.route('/showall',methods=['POST'])
def showall():
    return multiple_buttons(None)


@app.route('/illustrator',methods=['POST'])
def illustrator():
    return multiple_buttons('Illustrator')

@app.route('/digital',methods=['POST'])
def digital():
    return multiple_buttons('Digital Designer')

@app.route('/filmmaker',methods=['POST'])
def filmmaker():
    return multiple_buttons('Filmmaker')

@app.route('/graphic',methods=['POST'])
def graphic():
    return multiple_buttons('Graphic Design')


@app.route('/photographer',methods=['POST'])
def photographer():
    return multiple_buttons('photographer')




@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    flash("You are now logged out", category='logout')
    return index()


@app.route('/imprint')
def imprint():
    return render_template("imprint.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(AssertionError)
def mysql_error(err):
    return render_template("400.html")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
from markupsafe import escape
from flask import *  

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=<HOSTNAME>;PORT=<PORT NUMBER>;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=<USERNAME>;PWD=<PASSWORD>",'','')
print(conn)
print("connection successful...")

app = Flask(__name__)
app.secret_key = 'your secret key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        name =request.form['name']
        password=request.form['password']
     
    
        sql =f"select * from customer where name='{escape(name)}' and password='{escape(password)}'"
        stmt = ibm_db.exec_immediate(conn, sql)
        data = ibm_db.fetch_both(stmt)

        if data:
            session["name"] = escape(name)
            session["password"] = escape(password)
            return redirect("customer")
        else:
            flash("Username and Password Mismatch","danger")
    return redirect(url_for("index"))


@app.route('/customer',methods=["GET","POST"])
def customer():
    return render_template("customer.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            address=request.form['address']
            contact=request.form['contact']
            password=request.form['password']
            sql = "SELECT * FROM customer WHERE name=?"
            stmt =ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,name)
            ibm_db.execute(stmt)
            account =ibm_db.fetch_assoc(stmt)
            
            if account:
                return "aldready found"
            else:
                insert_sql = "insert into customer(name,address,contact,password)values(?,?,?,?)"
                prep_stmt = ibm_db.prepare(conn,insert_sql)
                ibm_db.bind_param(prep_stmt,1,name)
                ibm_db.bind_param(prep_stmt,2,address)
                ibm_db.bind_param(prep_stmt,3,contact)
                ibm_db.bind_param(prep_stmt,4,password)
                ibm_db.execute(prep_stmt)

                flash("Record Added  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("index"))
            con.close()

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
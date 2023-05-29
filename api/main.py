from flask import Flask,render_template,request,session,redirect,url_for,flash, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json
import csv

# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='kusumachandashwini'


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/transport'
db=SQLAlchemy(app)

# here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))



class maintable(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    truckno=db.Column(db.Integer)
    ttype=db.Column(db.String(50))
    From=db.Column(db.String(50))
    to=db.Column(db.String(50))
    consignor=db.Column(db.String(50))
    consignee=db.Column(db.String(50))
    transporter=db.Column(db.String(50))
    distance=db.Column(db.Integer)
    rate=db.Column(db.Integer)
    goods=db.Column(db.String(100))
    quantity=db.Column(db.Integer)
    driver=db.Column(db.String(50))
    num=db.Column(db.Integer)
    amount=db.Column(db.Integer)


class vehicle(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    vehicleno=db.Column(db.Integer)
    model=db.Column(db.String(50))
    year=db.Column(db.Integer)
    vtype=db.Column(db.String(50))
    mileage=db.Column(db.String(50))
    color=db.Column(db.String(50))
    book=db.Column(db.String(50))
  
class employee(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    age=db.Column(db.Integer)
    mobno=db.Column(db.Integer)
    gender=db.Column(db.String(50))
    salary=db.Column(db.Integer)
    address=db.Column(db.String(50))
  
class order(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    customer=db.Column(db.String(50))
    orderdate=db.Column(db.String(50))
    goods=db.Column(db.String(50))
    From=db.Column(db.String(50))
    to=db.Column(db.String(50))
    duedate=db.Column(db.String(50))
    status=db.Column(db.String(50))
  
  
@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/records')
@login_required
def records():
    query=db.engine.execute(f"SELECT * FROM `maintable`") 
    return render_template('records.html',query=query)


@app.route("/delete/<string:id>",methods=['POST','GET'])
@login_required
def delete(id):
    db.engine.execute(f"DELETE FROM `maintable` WHERE `maintable`.`id`={id}")
    flash("Slot Deleted Successful","danger")
    return redirect('/records')


@app.route("/deletevehicle/<string:id>",methods=['POST','GET'])
@login_required
def deletevehicle(id):
    db.engine.execute(f"DELETE FROM `vehicle` WHERE `vehicle`.`id`={id}")
    flash("Slot Deleted Successful","danger")
    return redirect('/managevehicles')

@app.route("/deleteemployee/<string:id>",methods=['POST','GET'])
@login_required
def deleteemployee(id):
    db.engine.execute(f"DELETE FROM `employee` WHERE `employee`.`id`={id}")
    flash("Slot Deleted Successful","danger")
    return redirect('/manageemployee')

@app.route("/deleteorder/<string:id>",methods=['POST','GET'])
@login_required
def deleteorder(id):
    db.engine.execute(f"DELETE FROM `order` WHERE `order`.`id`={id}")
    flash("Slot Deleted Successful","danger")
    return redirect('/manageorder')


# @app.route("/edit/<string:id>",methods=['POST','GET'])
# @login_required
# def edit(id):
#     posts=maintable.query.filter_by(id=id).first()
#     if request.method=="POST":
#         truckno=request.form.get('truckno')
#         ttype=request.form.get('ttype')
#         From=request.form.get('From')
#         to=request.form.get('to')
#         consignor=request.form.get('consignor')
#         consignee=request.form.get('consignee')
#         transporter=request.form.get('transporter')
#         distance=request.form.get('distance')
#         rate=request.form.get('rate')
#         goods=request.form.get('goods')
#         quantity=request.form.get('quantity')
#         driver=request.form.get('driver')
#         num=request.form.get('num')
#         amount=request.form.get('amount')
#         query=db.engine.execute(f"UPDATE `maintable` SET `truckno`='{truckno}',`ttype`='{ttype}',`From`='{From}',`to`='{to}',`consignor`='{consignor}',`consignee`='{consignee}',`transporter`='{transporter}',`distance`='{distance}',`rate`='{rate}',`goods`='{goods}',`quantity`='{quantity}',`driver`='{driver}',`num`='{num}',`amount`='{amount}' WHERE `maintable`.`id`={id}")
#         flash("Slot is Updated","success")
#         return redirect('/records')
    
#     return render_template('edit.html',posts=posts)

@app.route("/editvehicle/<string:id>",methods=['POST','GET'])
@login_required
def editvehicle(id):
    posts=vehicle.query.filter_by(id=id).first()
    if request.method=="POST":
        vehicleno=request.form.get('vehicleno')
        model=request.form.get('model')
        year=request.form.get('year')
        vtype=request.form.get('vtype')
        mileage=request.form.get('mileage')
        color=request.form.get('color')
        book=request.form.get('book')

        query=db.engine.execute(f"UPDATE `vehicle` SET `vehicleno`='{vehicleno}',`model`='{model}',`year`='{year}',`vtype`='{vtype}',`mileage`='{mileage}',`color`='{color}',`book`='{book}' WHERE `vehicle`.`id`={id}")
        flash("Slot is Updated","success")
        return redirect('/managevehicles')
    
    return render_template('editvehicle.html',posts=posts)

@app.route("/editemployee/<string:id>",methods=['POST','GET'])
@login_required
def editemployee(id):
    posts=employee.query.filter_by(id=id).first()
    if request.method=="POST":
        name=request.form.get('name')
        age=request.form.get('age')
        mobno=request.form.get('mobno')
        gender=request.form.get('gender')
        salary=request.form.get('salary')
        address=request.form.get('address')

        query=db.engine.execute(f"UPDATE `employee` SET `name`='{name}',`age`='{age}',`mobno`='{mobno}',`gender`='{gender}',`salary`='{salary}',`address`='{address}' WHERE `employee`.`id`={id}")
        flash("Slot is Updated","success")
        return redirect('/manageemployee')
    
    return render_template('editemployee.html',posts=posts)

@app.route("/editorder/<string:id>",methods=['POST','GET'])
@login_required
def editorder(id):
    posts=order.query.filter_by(id=id).first()
    if request.method=="POST":
        customer=request.form.get('customer')
        orderdate=request.form.get('orderdate')
        goods=request.form.get('goods')
        From=request.form.get('From')
        to=request.form.get('to')
        duedate=request.form.get('duedate')
        status=request.form.get('status')

        query=db.engine.execute(f"UPDATE `order` SET `customer`='{customer}',`orderdate`='{orderdate}',`goods`='{goods}',`From`='{From}',`to`='{to}',`duedate`='{duedate}',`status`='{status}' WHERE `order`.`id`={id}")
        flash("Slot is Updated","success")
        return redirect('/manageorder')
    
    return render_template('editorder.html',posts=posts)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        # newuser=User(username=username,email=email,password=encpassword)
        # db.session.add(newuser)
        # db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/adddetails',methods=['POST','GET'])
@login_required
def adddetails():
    if request.method=="POST":
        truckno=request.form.get('truckno')
        ttype=request.form.get('ttype')
        From=request.form.get('From')
        to=request.form.get('to')
        consignor=request.form.get('consignor')
        consignee=request.form.get('consignee')
        transporter=request.form.get('transporter')
        distance=request.form.get('distance')
        rate=request.form.get('rate')
        goods=request.form.get('goods')
        quantity=request.form.get('quantity')
        driver=request.form.get('driver')
        num=request.form.get('num')
        amount=request.form.get('amount')

        query=db.engine.execute(f"INSERT INTO `maintable` (`truckno`,`ttype`,`From`,`to`,`consignor`,`consignee`,`transporter`,`distance`,`rate`,`goods`,`quantity`,`driver`,`num`,`amount`) VALUES ('{truckno}','{ttype}','{From}','{to}','{consignor}','{consignee}','{transporter}','{distance}','{rate}','{goods}','{quantity}','{driver}','{num}','{amount}')")
    

        flash("Booking Confirmed","info")
    return render_template('maintable.html')

@app.route('/managevehicles',methods=['POST','GET'])
@login_required
def managevehicles():
    if request.method=="POST":
        vehicleno=request.form.get('vehicleno')
        model=request.form.get('model')
        year=request.form.get('year')
        vtype=request.form.get('vtype')
        mileage=request.form.get('mileage')
        color=request.form.get('color')
        book=request.form.get('book')

        query=db.engine.execute(f"INSERT INTO `vehicle` (`vehicleno`,`model`,`year`,`vtype`,`mileage`,`color`,`book`) VALUES ('{vehicleno}','{model}','{year}','{vtype}','{mileage}','{color}','{book}')")
        flash("Booking Confirmed","info")
    query=db.engine.execute(f"SELECT * FROM `vehicle`") 
    return render_template('vehicle.html',query=query)

@app.route('/manageorder',methods=['POST','GET'])
@login_required
def manageorder():
    if request.method=="POST":
        customer=request.form.get('customer')
        orderdate=request.form.get('orderdate')
        goods=request.form.get('goods')
        From=request.form.get('From')
        to=request.form.get('to')
        duedate=request.form.get('duedate')
        status=request.form.get('status')

        query=db.engine.execute(f"INSERT INTO `order` (`customer`,`orderdate`,`goods`,`From`,`to`,`duedate`,`status`) VALUES ('{customer}','{orderdate}','{goods}','{From}','{to}','{duedate}','{status}')")
        flash("Booking Confirmed","info")
    query=db.engine.execute(f"SELECT * FROM `order`") 
    return render_template('order.html',query=query)
    

    

@app.route('/manageemployee',methods=['POST','GET'])
@login_required
def manageemployee():
    if request.method=="POST":
        name=request.form.get('name')
        age=request.form.get('age')
        mobno=request.form.get('mobno')
        gender=request.form.get('gender')
        salary=request.form.get('salary')
        address=request.form.get('address')

        query=db.engine.execute(f"INSERT INTO `employee` (`name`,`age`,`mobno`,`gender`,`salary`,`address`) VALUES ('{name}','{age}','{mobno}','{gender}','{salary}','{address}')")
        flash("Booking Confirmed","info")
    query=db.engine.execute(f"SELECT * FROM `employee`") 
    return render_template('employee.html',query=query)




@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My database is not Connected'


# Bill print
@app.route("/bill/<string:id>",methods=['POST','GET'])
@login_required
def bill(id):
    posts=maintable.query.filter_by(id=id).first()
    if request.method=="POST":
        truckno=request.form.get('truckno')
        ttype=request.form.get('ttype')
        From=request.form.get('From')
        to=request.form.get('to')
        consignor=request.form.get('consignor')
        consignee=request.form.get('consignee')
        transporter=request.form.get('transporter')
        distance=request.form.get('distance')
        rate=request.form.get('rate')
        goods=request.form.get('goods')
        quantity=request.form.get('quantity')
        driver=request.form.get('driver')
        num=request.form.get('num')
        amount=request.form.get('amount')
        
    
    return render_template('bill.html',posts=posts)


@app.route('/download')
def download():
    return render_template('download_csv.html')

# @app.route('/download/report/csv')
# def download_report():
#  conn = None
#  cursor = None
#  try:
#   conn = db.connect()
#   cursor = conn.cursor(pymysql.cursors.DictCursor)
   
#   conn.execute("SELECT * FROM employees")
#   result = cursor.fetchall()
 
#   output = io.StringIO()
#   writer = csv.writer(output)
   
#   line = ['Id, TRUCK NUMBER, TRUCK TYPE, FROM, TO, CONSIGNOR, CONSIGNEE, TRANSPORTER, DISTANCE, RATE, GOODS	QUANTITY, DRIVER, DRIVER MOBILE NO,TOTAL AMOUNT']
#   writer.writerow(line)
 
#   for row in result:
#    line = [str(row['id']) + ',' + row['truckno'] + ',' + row['ttype'] + ',' + row['From'] + ',' + row['to'] + ',' + row['consignor'] + ',' + row['consignee'] + ',' + row['transporter'] + ',' + row['distance'] + ',' + row['rate'] + ',' + row['goods'] + ',' + row['quantity'] + ',' + row['driver'] + ',' + row['num'] + ',' + row['amount']]
#    writer.writerow(line)
 
#   output.seek(0)
   
#   return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=employee_report.csv"})
#  except Exception as e:
#   print(e)
#  finally:
#   cursor.close() 
#   conn.close()

# @app.route('/download/report/csv')
# def download_report():
#     result = maintable.query.all()

#     output = io.StringIO()
#     writer = csv.writer(output)

#     line = ['Id, First Name']
#     writer.writerow(line)

#     for row in result:
#         line = [str(row.id) + ',' + row.truckno]
#         writer.writerow(line)

#     output.seek(0)

#     return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=employee_report.csv"})


@app.route('/export')
def export():
    query=db.engine.execute(f"SELECT * FROM `maintable`") 
    print(query)
    fields = ["Id", "Truck No", "Truck Type", "From", "To", "Consigner", "Consignee", "Transporter", "Distance", "Rate", "Goods", "Quantity", "Driver", "Mobile No", "Amount"]
    with open("records.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(fields) 
        for post in query:
            writer.writerow([post.id, post.truckno, post.ttype, post.From, post.to, post.consignor, post.consignee, post.transporter, post.distance, post.rate, post.goods, post.quantity, post.driver, post.num, post.amount])
        flash("Saved to 'records.csv'", "info")
        
    return redirect('/records')

app.run(debug=True)    

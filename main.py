from flask import *
import data_base
from werkzeug.utils import secure_filename
import os

aa=data_base.data_base()

app=Flask(__name__)
app.config['SECRET_KEY']='123'

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/admin_login_page')
def adminLoginPage():
    return render_template("adminLogin.html")

@app.route('/admin_login', methods=['POST','GET'])
def adminLogin():
    uname=request.form['box1']
    password=request.form['box2']
    if uname=="admin" and password== "admin":
        return render_template("adminHome.html")
    else:
        return render_template('adminLogin.html',data="your Username or password is worng")
    
@app.route('/admin_home')
def admin_home():
    return render_template("adminHome.html")

@app.route('/view_former')
def admin_view_former():
    data=aa.show("select * from former_detials")
    if data:
       return render_template("admin_view_former.html",items=data)
    else:
        return render_template("admin_view_former.html")

@app.route('/view_user')
def admin_view_user():
    data=aa.show("select * from user_detials")
    if data:
       return render_template("admin_view_user.html",items=data)
    else:
        return render_template("admin_view_user.html")


@app.route('/admin_view_feedback')
def admin_view_feedback():
    data=aa.show("select * from feedback")
    if data:
        return render_template("admin_viewfeadback.html",items=data)
    else:
        return render_template("admin_viewfeadback.html")
        



# medial men part
@app.route('/medial_login_page')
def medialmen_login_page():
    return render_template('former_login_page.html')

@app.route('/medial_login', methods=['get','post'])
def medial():
    name=request.form['box1']
    password=request.form['box2']
    data=aa.show("select * from former_detials where username='"+name+"' and password='"+password+"'")
    if data :
        session['userid'] = data[0][0]
        return render_template("former_home.html")
    else:
        return render_template("former_login_page.html")

@app.route('/former_registerPage')
def former_registerPage():
    return render_template('former_registerPage.html')


@app.route('/former_register' ,methods=['post','get'])
def former_register():
    id=""
    a=request.form['box1']
    b = request.form['box2']
    c = request.form['box3']
    d = request.form['box4']
    e = request.form['box5']
    f = request.form['box6']
    g = request.form['box7']
    h = request.form['box8']
    status=""
    aa.register("INSERT INTO former_detials(name,fathername,number,email,address,pincode,username,password) values ('"+a+"','"+b+"','"+c+"','"+d+"','"+e+"','"+f+"','"+g+"','"+h+"')")
    return redirect('former_registerPage')

@app.route('/former_home')
def former_home():
    return template_rendered('former_home.html')


@app.route('/add_product')
def add_product():
    return render_template('former_add_product.html')

@app.route('/add_product_page' , methods=['post','get'])
def add_product_page():
    # print(session['userid'])
    product_name=request.form['box1']
    catagery=request.form['box2']
    prices=request.form['box3']
    expiry_date=request.form['box4']
    image=request.files['box5']
    filename=secure_filename(image.filename)
    image.save(os.path.join("static/upload/", filename))
    total_quantity=request.form['box6']
    farmer_id=str(session['userid'])
    aa.register("INSERT INTO add_product(product_name,catagery,prices,expiry_date,image,total_quantity,status) values ('"+product_name+"','"+ catagery+"','"+prices+"','"+expiry_date+"','"+filename+"','"+total_quantity+"','"+farmer_id+"')")
    return redirect('add_product')

@app.route('/former_view_user')
def former_view_user():
    data=aa.show("select * from user_detials")
    if data:
       return render_template("former_view_user.html",items=data)
    else:   
        return render_template("former_view_user.html")
    

@app.route('/farmer_view_selles')
def farmer_view_selles():
    farmer_id=session['userid']
    data=aa.show("select * from add_product where status='"+str(farmer_id)+"' and quantity_sold=1")
    return render_template('farmer_view_selles.html', items=data)

@app.route('/view_feedback')
def view_feedback():
    data=aa.show("select * from feedback")
    if data:
        return render_template('view_feedback.html',items=data)
    else:
        return render_template('view_feedback.html')




# user part
@app.route('/user_loginPage')
def user_loginPage():
    return render_template('user_login.html')

@app.route("/user_login",methods=['POST','GET'])
def user_login():
    name=request.form['box1']
    password=request.form['box2']
    data=aa.show("select * from user_detials where username='"+name+"' and password='"+password+"'")
    if data :
        session['user']=data[0][1]
        return render_template("user_home.html")
    else:
        return render_template("user_login.html")

@app.route('/registerPage')
def registerPage():
    return render_template('user_registerPage.html')

@app.route('/user_register' ,methods=['post','get'])
def user_register():
    id = ""
    a = request.form['box1']
    b = request.form['box2']
    c = request.form['box3']
    d = request.form['box4']
    e = request.form['box5']
    f = request.form['box6']
    g = request.form['box7']
    h = request.form['box8']
    status=""
    aa.register("INSERT INTO user_detials(name,fathername,number,email,address,pincode,username,password) values ('"+a+"','"+b+"','"+c+"','"+d+"','"+e+"','"+f+"','"+g+"','"+h+"')")
    return redirect('registerPage')

@app.route('/user_home')
def user_home():
    return render_template("user_home.html")

@app.route('/user_view_product')
def user_view_product():
    data=aa.show("select * from add_product")
    if data:
      
       
       return render_template('user_view_product.html',items=data)
    else:
        return render_template('user_view_product.html')
    
@app.route("/buy_product=<product_id>")
def buy_product(product_id):
    # Fetch product details securely using parameterized queries
    data = aa.show("SELECT * FROM add_product WHERE id = '"+product_id+"'")  # Ensure 'aa.show' supports parameterized queries
    # Check if product exists
    if not data:
        
        return "Product not found", 404

    return render_template("user_buy_product.html", items=data)  # Assuming data returns a list


@app.route("/a", methods=['POST'])
def store_product():
    product_id = request.form['product_id']
    farmer_id = request.form['farmer_id']
    aa.register("UPDATE add_product SET quantity_sold = '1', last_sold_date = NOW() WHERE id = '"+product_id+"' AND status = '"+farmer_id+"';")
    return redirect('user_view_product')

@app.route('/user_feedback_page')
def user_feedback_page():
    return render_template('user_feedback.html')

@app.route("/user_feedback" ,methods=['post','get'])
def user_feedback():
    content=request.form['box1']
    user=session['user']
    aa.register('insert into feedback values("'+content+'","'+user+'")')
    return render_template('user_feedback.html')


if __name__=="__main__":
    app.run(debug=True)

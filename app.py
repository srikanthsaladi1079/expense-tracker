#Import Libraries        
from flask import Flask,render_template,redirect,url_for,request,session,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime,timezone
from models import db,User,Expense
from collections import defaultdict
from functools import wraps
from sqlalchemy import or_,func

#Custom login required 
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page","danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

#Initialize app and cofigure
app = Flask(__name__)
app.secret_key = "expense-tracker-key"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///expenses.db'
db.init_app(app)    

#Home page
@app.route('/')
def index():
    return render_template("index.html")

#Register User
@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        #Check if email already exists 
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already Registered! Please Log in.","warning")
            return redirect(url_for("login")) #Already exists 
        
        #Password check
        if password != confirm_password:
            flash("Passwords did not match.","danger")
            return redirect(url_for('register'))
        
        #Save new user 
        hashed_pw = generate_password_hash(password)
        new_user = User(name=name,email=email,password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful. Please Log in!","success")
        return redirect(url_for("login"))
    
    return render_template("register.html")

#Login Route  
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id   
            return redirect(url_for("profile"))
        else:
            return render_template("login.html")
            
    return render_template("login.html")

#Logout 
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

#delete_data route 
@app.route('/delete_data',methods=['GET','POST'])
def delete_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session["user_id"]
    
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        
        user = User.query.get(user_id)
        
        #validate password match
        if password != confirm_password:
            return render_template("delete_data.html",error="Passwords do not match.")
        
        #Validate password correctness
        if not check_password_hash(user.password, password):
            return render_template("delete_data.html",error="Incorrect Password")
        
        #convert string dates to datetime.date
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return render_template("delete_data.html",error="Invalid date format")
        
        #Get expenses in range       
        expenses_to_delete = Expense.query.filter(Expense.user_id == user_id, Expense.date >= start_date_obj, Expense.date <= end_date_obj).all()
        
        if not expenses_to_delete:
            return redirect(url_for("delete_data"),error="No expenses found in the selected date range")
        
        #Delete Matched expenses  
        for exp in expenses_to_delete:
            db.session.delete(exp)
        db.session.commit()
        
        return redirect(url_for("dashboard"))
    
    return render_template("delete_data.html")

#delete account 
@app.route('/delete_account',methods={'GET','POST'})
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    error = None
    
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form["confirm_password"]
        
        if not password or not confirm_password:
            error = "All Fields are required."
        elif password != confirm_password:
            error = "Passwords does not match."
        else:
            user = User.query.get(session['user_id'])
            
            if not user or not check_password_hash(user.password, password):
                error = "Incorrect Password."
            else:
                #Delete user data
                Expense.query.filter_by(user_id=user.id).delete()
                db.session.delete(user)
                db.session.commit()
                session.clear()
                return redirect(url_for("register"))
    
    return render_template("delete_account.html", error=error)

#forgot-password
@app.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    error = None
    success = None
    
    if request.method == "POST":
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not email or not new_password or not confirm_password:
            error = "All fields are required."
        elif new_password != confirm_password:
            error = "Passwords do not match"
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                hashed_pw = generate_password_hash(new_password)
                user.password = hashed_pw
                db.session.commit()
                success = "Password Updated Successfully."
                return redirect('/login')
            else:
                error = "No account found with this email."
    
    return render_template("forgot_password.html",error=error,success=success)

#profile route
@app.route('/profile', methods=['GET','POST'])
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_password = request.form['new_password']
        
        #Update name and email 
        user.name = name 
        user.email = email 
        
        #If password is provided
        if new_password.strip() != "":
            user.password = generate_password_hash(new_password)
        
        db.session.commit()
        return redirect('/dashboard')
    
    return render_template('profile.html', user=user)

#Dashboard route 
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
        
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('dashboard.html',user=user)

#Add Expense Route 
@app.route('/add_expense',methods=['GET','POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        title = request.form.get('title')
        amount = request.form.get('amount')
        category = request.form.get('category')
        note = request.form.get('note')
        
        new_expense = Expense (
            title=title,
            amount=amount,
            category=category,
            note=note,
            user_id=session['user_id']
        )
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('view_expenses'))

    return render_template('add_expense.html')

#view expenses 
@app.route('/view_expenses')
def view_expenses():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    search_query = request.args.get('query','').strip()
    
    if search_query:
        expenses = Expense.query.filter(Expense.user_id == user_id, or_(Expense.title.ilike(f'%{search_query}%'), Expense.category.ilike(f'%{search_query}%'),Expense.note.ilike(f'%{search_query}%'))).all()
    else:
        expenses = Expense.query.filter_by(user_id=user_id).all()
    return render_template('view_expenses.html',expenses=expenses)

#edit expense      
@app.route('/edit_expense/<int:id>',methods=['GET','POST'])
@login_required
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    
    if request.method == 'POST':
        expense.title = request.form['title']
        expense.amount = request.form['amount']
        expense.category = request.form['category']
        expense.note = request.form['note']
        
        db.session.commit()
        flash("Expenses updated Successfully","success")
        return redirect(url_for('view_expenses'))
    return render_template('edit_expense.html',expense=expense)

@app.route('/delete_expense/<int:id>',methods=['GET','POST'])
def delete_expense(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    expense = Expense.query.get_or_404(id)
    
    if expense.user_id != session['user_id']:
        return "unauthorized", 403
    
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('view_expenses'))

#edit profile 
@app.route('/edit_profile',methods=['GET','POST'])
def edit_profile():
    if request.method == 'POST':
        pass
    return render_template("edit_profile.html")

#tools 
@app.route('/tools')
def tools():
    return render_template('tools.html')

#Downlaod CSV            
@app.route('/download_csv')
def download_csv():
    return "Coming Soon"

#Downlaod PDF           
@app.route('/download_pdf')
def download_pdf():
    return "Coming Soon"

#View Pie-Chart       
@app.route('/pie_chart')
def pie_chart():
    return "Coming Soon"

#View Bar Graph 
@app.route('/bar_graph')
def bar_graph():
    return "Coming Soon"

#Monthly Summary 
@app.route("/summary")
@login_required
def summary():
    user_id = session.get("user_id")
    expenses = Expense.query.filter_by(user_id=user_id).all()
    
    total_spent = sum(exp.amount for exp in expenses)
    
    #Category wise breakdown
    category_totals = {}
    for exp in expenses:
        category = exp.category 
        category_totals[category] = category_totals.get(category, 0) + exp.amount
        
    #Top Category 
    top_category = max(category_totals, key=category_totals.get)
    
    return render_template("summary.html", total_spent=total_spent, top_category=top_category,category_totals=category_totals)

#Run the App
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
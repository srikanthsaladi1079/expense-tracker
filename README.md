# 💸 Expense Tracker - Flask Project

A clean, modern web application to track your daily expenses, built using **Flask**, **SQLite**, **SQLAlchemy**, and **Bootstrap**.

---

## 🚀 Features

- 🔐 User Registration and Login system
- 👤 Edit Profile
- ➕ Add New Expense (Category, amount, date, note)
- 🗒️ View All Expenses in table format
- 🧹 Edit or Delete Individual Expenses
- 📊 Summary Page for total Expenses
- 🧰 Tools Page (Download Options - Coming Soon)
- 🧹 Delete All Data
- ❌ Delete Account Permanently
- 🥰 Clean UI using Bootstrap

---
 ## 📌 Use Case

 Managing daily expenses is often a challenge for individuals. This app acts as a **personal finance assistant**, helping users:

 - Record every expense in a structured way
 - View and Analyze their spending pattern
 - Track total expenses over time
 - Delete old data or accounts when needed
 - Search for any particualr expense with keyword

 Whether you're a student, professional, or home user - this tracker simplifies budgeting and expense control in a clean, beginner-friendly way.

---

## ⚒️ Tech Stack

- **Backend:** Flask, Python, SQLAlchemy
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite
- **Tools:** Flask-Login, Jinja2

---

## 📂 Project Structure

Expense-Tracker/
|
|--- static/ # Bootstrap and static assets
|-- templates/ #HTML Pages
|  |-- index.html
|  |-- register.html
|  |-- login.html
|  |-- dashboard.html
|  |-- add_expense.html
|  |-- view_expenses.html
|  |-- profile.html
|  |-- forgot_password.html
|  |-- tools.html
|  |-- delete_data.html
|  |-- delete_account.html
|  |-- summary.html
|  |-- edit_profile.html
|
|--- app.py # Main Flask application
|--- models.py # Database models
|--- requirements.txt # Required Packages
|--- README.md # You are Here

---

## ✅ SetUp Instructions

1. **Clone the repository**
```bash
git clone https://github.com/srikanthsaladi1079/expense-tracker.git
cd expense-tracker

2. **Create virtual environment and activate**

python -m venv venv
venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate # On Linux/macOS

3. Install dependencies
 pip install -r requirements.txt

4. Run the app
 python app.py

**App will be live at http://127.0.0.1:5000


📦 Future Improvements

- Budget Limit Notifications
- Graphical Summary (Pie-Chart/Bar-Chart)
- Export Monthly Reports
- Downloadable PDF/CSV for offline use
- Google OAuth Login
- Mobile Responsive Enhancements
- Email Based password reset
- Flash Messages when there's error and successful login or retreival

🧑‍💻 Author

Built with 💖 by Srikanth Saladi
Github : srikanthsaladi1079


🌟 show some Love
If you like this project, drop a ⭐ on GitHub!

--- 

📝 License

This Project is open-source and available under the [MIT License](LICENSE),

You are free to use, modify, and distribute it with proper attribution.

---

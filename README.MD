💰 ShahiLedger

A modern personal finance & loan management system built with Django.

ShahiLedger is a full-stack Django web application that helps users manage:

💳 Bank & Cash balances

📊 Income & Expenses

🤝 Loans Given, Taken & Received

📈 Automatic wallet updates

📥 Excel export support

Designed for clarity, simplicity, and real-world financial tracking.

🚀 Features
🏦 Wallet System

Separate Bank and Cash balance

Automatic balance updates

Real-time total calculation

💸 Transactions

Add Income & Expense

Choose payment method (Bank/Cash)

Automatic wallet adjustment

Categorization & description support

🤝 Loan Management

Loan Given

Loan Taken

Loan Received

Auto transaction creation

Per-person loan tracking

Loan history view

Pending calculation logic

📊 Excel Export

Monthly transaction export

Loan export support

Uses OpenPyXL

🛠 Tech Stack
Technology	Purpose
Python 3.11	Backend
Django 5	Web Framework
SQLite	Database
OpenPyXL	Excel export
HTML/CSS	Frontend
📂 Project Structure
ShahiLedger/
│
├── finance/            # Main app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│
├── ShahiLedger/        # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── templates/
├── manage.py
├── requirements.txt
⚙️ Installation (Local Setup)
1️⃣ Clone Repository
git clone https://github.com/Mannatxdev/ShahiLedger.git
cd ShahiLedger
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Apply Migrations
python manage.py migrate
5️⃣ Create Superuser
python manage.py createsuperuser
6️⃣ Run Server
python manage.py runserver

Open:

http://127.0.0.1:8000/
📸 Core Functional Logic
🧠 Smart Loan Logic
Loan Type	Wallet Impact
GIVEN	Expense
TAKEN	Income
RECEIVED	Income
🧮 Pending Calculation
Pending = Total Given - Total Taken - Total Received
🔐 Authentication

Django built-in authentication

One Wallet per User (auto-created via signals)

📌 Future Improvements

User Dashboard Charts

REST API version

Multi-user shared ledger

PDF export

Deployment (Railway / Render)

👨‍💻 Author

Mannat Kumar
GitHub: https://github.com/Mannatxdev.


# 🖨️ Smart Xerox Services

## 📌 Project Overview

Smart Xerox Services is a web-based application that simplifies document printing and Xerox service management. It allows users to upload documents, select printing options, and make secure online payments without visiting a physical store.

---

## 🚀 Features

### 👤 User Features

* Upload documents (PDF, images)
* Automatic page detection
* Select number of copies and document type
* Manual page input option
* Secure online payment integration
* View order details

### 🛠️ Admin Features

* Manage user orders
* Monitor payments
* Handle document processing
* Track system activity

---

## 🧑‍💻 Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Django (Python)

### Database

* MongoDB

### Deployment

* Render (Cloud Platform)

---

## 📁 Project Structure

```
smartproject/
│
├── backend/
│   ├── backend/        # Django project
│   ├── smartxerox/     # App
│   ├── staticfiles/
│   ├── media/
│   ├── db.sqlite3
│   └── manage.py
│
├── requirements.txt
├── Procfile
├── runtime.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```
git clone https://github.com/YOUR_USERNAME/smart-xerox-services.git
cd smart-xerox-services
```

### 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Run Migrations

```
python manage.py migrate
```

### 5️⃣ Run Server

```
python manage.py runserver
```

---

## 🌐 Deployment (Render)

1. Push project to GitHub
2. Create a new Web Service in Render
3. Add:

   * Build Command: `pip install -r requirements.txt`
   * Start Command: `gunicorn backend.wsgi`
4. Add environment variable:

   * `PYTHON_VERSION = 3.11`

---

## 🔐 Security Features

* Secure authentication system
* Safe file handling
* Payment integration security

---

## ❗ Known Issues

* SQLite not suitable for production
* Requires proper static file configuration

---

## 🔮 Future Enhancements

* Order tracking system
* Email/SMS notifications
* Admin dashboard improvements
* Mobile app version

---

## 🤝 Contribution

Contributions are welcome! Feel free to fork the repository and submit pull requests.

---

## 📄 License

This project is developed for educational purposes.

---

## 👨‍💻 Author

** SHEKAPURAM PRANAY **
Smart Xerox Services Project

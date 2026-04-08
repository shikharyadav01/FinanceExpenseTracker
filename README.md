# 💰 AI-Powered Expense Tracker

An intelligent Expense Tracker web application built using Flask, enhanced with AI and Machine Learning features to help users track, analyze, and understand their spending habits.

---

## 🚀 Features

### 🧾 Core Features

* ➕ Add, edit, and delete expenses
* 📂 Categorize expenses (Food, Transport, Rent, Utilities, etc.)
* 📅 Filter expenses by date and category
* 📊 Interactive dashboard with charts
* 💾 Data stored using SQLite
* 📥 Export filtered data to CSV

---

### 🤖 AI Features

* 🧠 **Smart Expense Categorization**
  Automatically classifies expenses based on description using AI (Gemini API + fallback logic)

* 📊 **AI Spending Insights**
  Generates insights like:

  * "You spent 45% on Food"
  * Helps users understand spending patterns

* 📈 **Expense Prediction (Machine Learning)**
  Predicts future expenses using Linear Regression

* 💬 **AI Chat Assistant**
  Ask questions like:

  * "How much did I spend on food?"
  * "What is my highest expense?"

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* SQLAlchemy

### Frontend

* HTML
* Tailwind CSS
* JavaScript
* Chart.js

### AI & ML

* Google Gemini API
* Scikit-learn (Linear Regression)

### Database

* SQLite

---

## 📁 Project Structure

```
expense-tracker/
│
├── app.py
├── ai/
│   ├── gemini.py
│   ├── insights.py
│
├── ml_model.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── edit.html
│
├── static/
├── requirements.txt
└── .env
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
```

### 2. Create Virtual Environment

```
python -m venv venv
```

### 3. Activate Environment

```
venv\Scripts\activate
```

### 4. Install Dependencies

```
pip install -r requirements.txt
```

### 5. Setup Environment Variables

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

### 6. Run the App

```
python app.py
```

---

## 📊 How It Works

1. User adds expense
2. AI categorizes expense automatically
3. Data is stored in database
4. Dashboard updates with:

   * Charts
   * AI insights
   * Predictions
5. User can query data using AI chatbot

---

## 🎯 Use Cases

* Personal finance management
* Budget tracking
* Spending analysis
* Learning full-stack + AI integration

---

## 🔥 Highlights

* Real-world full-stack project
* AI + ML integration
* Production-level architecture
* Clean UI with Tailwind
* Scalable design

---

## 🚀 Future Improvements

* User authentication (login/signup)
* Cloud database (PostgreSQL)
* Budget alerts & notifications
* Voice-based expense input
* Mobile app version

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork and submit a pull request.

---

## 📜 License

This project is licensed under the MIT License.

---

## ⭐ Support

If you found this project useful, give it a ⭐ on GitHub!

---

## 👨‍💻 Author

**Shikhar Yadav**
CSE Data Science Student

---

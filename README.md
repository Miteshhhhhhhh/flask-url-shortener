# 🔗 Flask URL Shortener

   ### 🚀 Live Demo
   **[Click Here - https://flask-url-shortener-9tkq.onrender.com](https://flask-url-shortener-9tkq.onrender.com)**

### 📸 Screenshots

![Homepage] <img width="819" height="460" alt="flask_url_shortener" src="https://github.com/user-attachments/assets/9c92e953-e57b-4681-93f8-0b5434f53ddf" />

![Shortened Link] <img width="1364" height="638" alt="shortener_url_2" src="https://github.com/user-attachments/assets/b0ec20bf-2bb5-42cc-95f7-698cabf26655" />



A minimal URL shortener built with Flask and SQLite. Generate short links, track clicks, copy them with one click, and delete them when needed.

## ✨ Features

- **URL Shortening**: Convert long URLs into 6-character short codes
- **Click Analytics**: Tracks how many times each short link was visited
- **Timestamps**: Shows when each short URL was created
- **URL Deletion**: Delete short links with confirmation dialog
- **Duplicate Prevention**: Same URL returns existing short code instead of creating new
- **One-Click Copy**: Copy short link to clipboard instantly
- **Open Link Button**: Test your short URL directly
- **SQLite Database**: Lightweight, serverless, zero-config database

## 🚀 Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite3
- **Frontend**: HTML, Vanilla JavaScript
- **Deployment**: Gunicorn + Render

   ### ⚠️ Note
   Hosted on Render's free tier. Short links may expire if the server restarts due to SQLite's ephemeral storage.

## 📦 Setup Locally

1. **Clone the repo**
      ```bash
   git clone https://github.com/Miteshhhhhhhh/flask-url-shortener.git
2. Install dependencies
      ```bash
     pip install -r requirements.txt
3. Run the app
      ```bash
     python flask_url.py
4. Open browser
      ```bash
     http://127.0.0.1:5000
   

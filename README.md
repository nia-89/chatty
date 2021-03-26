# Chatty

Analyze Your WhatsApp Chat

This was originally meant to be a really quick Valentine's day surprise for my husband while learning Python but ended up growing into something more. Once this version is done, I'm planning on refactoring the application and adding unit and feature testing.

> py -3 -m venv venv


> venv\Scripts\activate


> pip install -r requirements.txt


> set FLASK_APP=main.py


> set FLASK_ENV=development


> flask run

Access http://localhost:5000 in your favourite browser

- [x] Upload a WhatsApp chat export from Android or iOS
- [x] Wordcloud
- [x] Top ten busiest days
- [x] Pie chart of messages per user
- [ ] Mutli-line chart of messages over time per user
- [x] Choose a shape for the wordcloud
- [ ] Choose a colour palette for the wordcloud
- [ ] Emoji analysis
- [ ] Loading bar during file upload and processing


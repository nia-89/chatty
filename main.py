from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pandas
import time
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config.from_pyfile('config.py')

ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(time.strftime('%Y-%m-%d_%H%M%S') + '_' + uploaded_file.filename)
            uploaded_file = uploaded_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
            import chatty as mcd
            filename = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
            chat_text = mcd.open_whatsapp_txt(filename)
            data = mcd.parse_whatsapp_txt(chat_text)
            data_frame = mcd.generate_data_frame(data)
            words = mcd.split_messages_into_words(data_frame)
            words_for_cloud = ' '.join(words)
            if request.form.get('mask'):
                mask_img = request.form.get('mask')
                word_cloud = mcd.generate_word_cloud(words_for_cloud, selected_mask=mask_img)
            else:
                word_cloud = mcd.generate_word_cloud(words_for_cloud)
            messages_by_user = mcd.get_number_of_messages_by_user(data_frame).to_json()
            messages_by_date_top_10 = mcd.get_number_of_messages_by_date(data_frame).head(10).to_html(header=False)
            #TODO Messages over time chart
            #messages_over_time = mcd.get_messages_over_time_by_user(data_frame).to_json()
            return render_template('results.html',
                word_cloud=word_cloud,  
                user_messages=messages_by_user,
                top_10_dates=messages_by_date_top_10
                )
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

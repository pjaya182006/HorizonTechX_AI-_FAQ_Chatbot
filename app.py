import os
import csv
import json
from io import StringIO
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, make_response
from config import Config
from utils.db_manager import DatabaseManager
from utils.nlp_engine import NLPEngine

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app()

db = DatabaseManager(Config.DATABASE_PATH)
nlp = NLPEngine(Config.FAQ_JSON_PATH)

print("FAQ File:", Config.FAQ_JSON_PATH)
print("Number of FAQs Loaded:", len(nlp.get_all_faqs()))
@app.route('/')
def index():
    faqs = nlp.get_all_faqs()
    return render_template('index.html', faqs=faqs)

@app.route('/chatbot')
def chatbot():
    if 'username' not in session:
        session['username'] = f"Guest_{datetime.now().strftime('%M%S')}"
    return render_template('chatbot.html', username=session['username'])

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    username = session.get('username', 'Guest')
    
    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400
        
    # Match query via NLP engine
    answer, confidence, suggestions = nlp.match_question(message, Config.CONFIDENCE_THRESHOLD)
    
    # Save transaction session metrics to SQLite logs
    db.log_message(username, message, answer, confidence)
    
    return jsonify({
        'answer': answer,
        'confidence': round(confidence, 2),
        'suggestions': suggestions
    })

@app.route('/api/feedback', methods=['POST'])
def api_feedback():
    return jsonify({'status': 'Feedback tracked successfully.'})

@app.route('/api/export/csv')
def export_csv():
    username = session.get('username', 'Guest')
    history = db.get_chat_history(username)
    
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Timestamp', 'User Message', 'Bot Response', 'Confidence Score'])
    for r in history:
        cw.writerow([r[4], r[1], r[2], r[3]])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=chat_history_{username}.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and 'login' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')
        if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Admin authentication vector verified.', 'success')
        else:
            flash('Invalid admin credentials payload.', 'danger')
            
    if not session.get('admin_logged_in'):
        return render_template('admin.html', authenticated=False)
        
    # Process actions if authenticated
    if request.method == 'POST' and 'add_faq' in request.form:
        q = request.form.get('question')
        a = request.form.get('answer')
        if q and a:
            nlp.add_faq(q, a)
            flash('New FAQ added to registry framework.', 'success')
            
    if request.method == 'GET' and request.args.get('delete'):
        faq_id = int(request.args.get('delete'))
        nlp.delete_faq(faq_id)
        flash('FAQ trace dropped.', 'warning')
        return redirect(url_for('admin'))

    faqs = nlp.get_all_faqs()
    analytics = db.get_analytics_summary()
    logs = db.get_global_logs(50)
    
    return render_template('admin.html', authenticated=True, faqs=faqs, analytics=analytics, logs=logs)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/about')
def about(): return render_template('about.html')

@app.route('/contact')
def contact(): return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
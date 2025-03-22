from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import smtplib
from email.message import EmailMessage
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email configuration
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', EMAIL_ADDRESS)

@app.route('/')
def home():
    return jsonify({"message": "Portfolio API is running!"})

@app.route('/contact', methods=['POST'])
def contact():
    try:
        print("xx")
        data = request.get_json()
        print(data)
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create email
        msg = EmailMessage()
        msg['Subject'] = f"Portfolio Contact: {data['subject']}"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        
        # Email body
        email_body = f"""
        You have received a new message from your portfolio website:
        
        Name: {data['name']}
        Email: {data['email']}
        Subject: {data['subject']}
        
        Message:
        {data['message']}
        """
        
        msg.set_content(email_body)
        
        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        
        # Log success
        logger.info(f"Contact form submission from {data['email']}")
        
        return jsonify({"message": "Message sent successfully!"}), 200
    
    except Exception as e:
        # Log error
        logger.error(f"Error processing contact form: {str(e)}")
        return jsonify({"error": "An error occurred processing your request."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


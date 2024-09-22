from flask import Flask, request, flash, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.secret_key = "123"

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_ADDRESS')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route("/", methods=["POST"])
def mail_route():
    data = request.get_json()
    
    # Extract emailId and messageBody
    email_id = data.get('email')
    message_body = data.get('message')

    print(email_id, "email")
    print(message_body, "message")

    if email_id and message_body:
        # Ensure email_id is a list
        to_mail_list = email_id if isinstance(email_id, list) else [email_id]

        for recipient in to_mail_list:
            print("Message:", message_body)
            print("Sender:", app.config['MAIL_USERNAME'])
            print("Recipient:", recipient)

            msg = Message(subject="Your Subject Here", sender=app.config['MAIL_USERNAME'], recipients=[recipient])
            msg.body = message_body
            try:
                mail.send(msg)
            except Exception as e:
                print("Error sending email:", e)
                return jsonify({"status": "error", "message": "Failed to send mail."}), 500

        flash("Mail Sent Successfully", 'success')
        return jsonify({"status": "success", "message": "Mail sent successfully."})

    return jsonify({"status": "error", "message": "Email and message body are required."}), 400

if __name__ == '__main__':
    app.run(debug=True)

import smtplib
from email.message import EmailMessage

def send_email(slots):
    # Create an email message object
    msg = EmailMessage()
    # Set the sender, receiver, subject and body of the email
    msg['From'] = 'your_email_address'
    msg['To'] = slots['Email']['value']['interpretedValue']
    msg['Subject'] = 'Your hotel reservation confirmation'
    msg.set_content(f"Hello {slots['Name']['value']['interpretedValue']},\n\nThank you for booking a {slots['RoomType']['value']['interpretedValue']} room at our hotel in {slots['Location']['value']['interpretedValue']} for {slots['Nights']['value']['interpretedValue']} nights starting from {slots['CheckInDate']['value']['interpretedValue']}. We look forward to welcoming you soon.\n\nBest regards,\nYour hotel team")
    # Create a SMTP object and connect to the server
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    # Start the TLS encryption
    smtp.starttls()
    # Log in to the server with your email and password
    smtp.login('your_email_address', 'your_password')
    # Send the email
    smtp.send_message(msg)
    # Close the connection
    smtp.quit()
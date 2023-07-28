from django.core.mail import send_mail

def send_email_receipt(form_data):
    # Format the email content using the form data
    subject = 'Translation Request Receipt'
    message = f'Thank you for your translation request!\n\n' \
              f'Here are the details of your request:\n' \
              f'First Name: {form_data["first_name"]}\n' \
              f'Last Name: {form_data["last_name"]}\n' \
              f'Email: {form_data["email"]}\n' \
              f'Phone Number: {form_data["phone_number"]}\n' \
              # Include other relevant form fields here

    # Send the email
    send_mail(subject, message, 'info@example.com', [form_data['email']])

def notify_admin():
    subject = "New Translation Request Submitted"
    message = "A new translation request has been submitted on the website."
    recipient_list = ["info@mokreyol.com"]  # Replace with the admin's email address

    # Using Django's built-in send_mail function
    send_mail(subject, message, "info@mokreyol.com", recipient_list)


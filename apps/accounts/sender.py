from django.core.mail import send_mail


def send_verification_email(user):
    verification_link = f"http://localhost:8000/api/v1/verify-email/?email={user.email}&code={user.verification_code}"
    message = f"Hi {user.first_name},\n\nPlease click the following link to verify your email address: {verification_link}\n\nThank you!"
    send_mail("Email Verification", message, "your_email@example.com", [user.email])

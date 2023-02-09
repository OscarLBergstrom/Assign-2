import smtplib, ssl
from email.message import EmailMessage

def notify_build_test(user_email, result, commit_id):
    """
    Sends an email to user_email about the results of a build and the running of tests
    """
    message = generate_build_test_message(user_email, result, commit_id)
    send_email(message)

def generate_build_test_message(user_email, result, commit_id):
    """
    Returns a ready to send EmailMessage object with the results of the build and tests. 
    """
    server_email = "mailingtesing@gmail.com"
    subject = "Result from group13CI"
    body = "Here are the results for commit " + commit_id + " :\n"
    test_code = result[0]
    install_code = result[1]
    build_code = result[2]
    body += "Test: "
    if test_code == 0:
        body += "All test passed"
    if test_code == 1:
        body += "One or more test cases failed"
    if test_code == 2:
        body += "Excecution was interupted by user"
    if test_code == 3:
        body += "The program crashed when running the tests"
    if test_code == 4:
        body += "The config file is incorectly configured"
    if test_code == 5:
        body += "No tests where found"
    body += "\nInstall: "
    if install_code == 0:
        body += "Install successfull"
    else:
        body += "Something went wrong in the installation step"
    body += "\nBuild: "
    if build_code == 0:
        body += "Build successfull"
    else:
        body += "Something went wrong in the build step"
    

    message = EmailMessage()
    message["From"] = server_email
    message["To"] = user_email
    message["Subject"] = subject
    message.set_content(body)
    return message

def send_email(message):
    """
    Sends a email message from our mail mailingtesing@gmail.com.
    """
    user_email = message["To"]
    server_email = "mailingtesing@gmail.com"
    password = "rfpopdglcqwdacxw"

    smtp_server = "smtp.gmail.com"
    port = 465
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(server_email, password)
        server.sendmail(server_email, user_email, message.as_string())
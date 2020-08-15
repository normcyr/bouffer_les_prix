#!/usr/bin/env python3

import yaml, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path


def load_config(config_file, text_file):

    with open(config_file, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    username = cfg["login"]["username"]
    password = cfg["login"]["password"]
    smtp_server = cfg["server"]["address"]
    smtp_port = cfg["server"]["port"]
    auth = cfg["server"]["authentification"]

    from_address = cfg["addresses"]["from_address"]
    to_address = cfg["addresses"]["to_address"]

    subject = cfg["msg_info"]["subject"]

    with open(text_file, "r") as txtfile:
        announcement = txtfile.read()

    return (
        username,
        password,
        smtp_server,
        smtp_port,
        auth,
        from_address,
        to_address,
        subject,
        announcement,
    )


def build_message(announcement, subject, from_address, to_address):

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = from_address
    msg["To"] = to_address

    body = announcement
    msg.attach(MIMEText(body, "html"))
    msg.add_header("Content-Type", "text")

    return msg


def confirm_sending(msg, announcement):

    print("You are about to send the following message:\n")
    print("------")
    print("From: {}".format(msg["From"]))
    print("To: {}".format(msg["To"]))
    print("Subject: {}\n".format(msg["Subject"]))
    print(announcement)
    print("------\n")

    answer = input("If everything is correct, are you ready to send it? (Y/n) ")
    print("\n")

    if answer == "Y":
        confirmation = True
    elif answer == "y":
        confirmation = True
    elif answer == "yes":
        confirmation = True
    elif answer == "Yes":
        confirmation = True
    elif answer == "YES":
        confirmation = True
    elif answer == "":
        confirmation = True
    else:
        confirmation = False
        print("The message will not be sent.")

    return confirmation


def send_message(
    username, password, smtp_server, smtp_port, auth, msg, from_address, to_address
):

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()

    if auth == True:
        server.starttls()
        server.login(username, password)

    send_mail_status = server.sendmail(from_address, to_address, msg.as_string())

    if send_mail_status != {}:
        print(
            "There was a problem sending an email. Error: {}.".format(send_mail_status)
        )

    server.quit()


def main():

    basepath = Path(__file__).parent.resolve()
    config_file = str(Path(basepath / "config.yml"))
    text_file = str(Path(basepath / "announcement.txt"))

    (
        username,
        password,
        smtp_server,
        smtp_port,
        auth,
        from_address,
        to_address,
        subject,
        announcement,
    ) = load_config(config_file, text_file)
    msg = build_message(announcement, subject, from_address, to_address)

    # confirmation = confirm_sending(msg, announcement)
    # if confirmation:
    # send_message(username, password, smtp_server, smtp_port, auth, msg, from_address, to_address)
    # print('The message was sent to {}.'.format(msg['To']))

    send_message(
        username, password, smtp_server, smtp_port, auth, msg, from_address, to_address
    )


if __name__ == "__main__":
    main()

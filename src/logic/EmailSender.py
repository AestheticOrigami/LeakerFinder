from email.message import EmailMessage
import smtplib
from src.logic.Security import getinfo


def sendEmail(dict, subject):
    sender = getinfo("mailSender")
    password = getinfo("mailPassword")

    messagelist = []

    for to, wtext in dict.items():

        message = EmailMessage()
        message['From'] = sender
        message['To'] = to
        message['Subject'] = subject
        message.set_content(wtext)

        messagelist.append(message)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()

        server.login(sender, password)

        for message in messagelist:
            server.send_message(message)

        server.quit()
def test():
    dict = {"tesitriennale793+test1@gmail.com": "testo 1", "tesitriennale793+6@gmail.com": "testo 2",
            "tesitriennale793+test2@gmail.com": "testo 3", "tesitriennale793+7@gmail.com": "testo 4",
            "tesitriennale793+test3@gmail.com": "testo 5", "tesitriennale793+8@gmail.com": "testo 6",
            "tesitriennale793+test4@gmail.com": "testo 7", "tesitriennale793+9@gmail.com": "testo 8",
            "tesitriennale793+test5@gmail.com": "testo 9", "tesitriennale793+10@gmail.com": "testo 10", }
    sendEmail(dict, "prova")


if __name__ == "__main__":
    test()

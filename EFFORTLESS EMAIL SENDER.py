import os
from email.message import EmailMessage
import smtplib
import ssl
from openai import OpenAI

client = OpenAI(base_url="https://openrouter.ai/api/v1",api_key="api key here") # Or use os.getenv("OPENAI_API_KEY")
system_prompt = "You are an assistant that helps generate email subjects and bodies."
while True:
    sender_email = input("sender email here:")
    receiver_email = input("receiver email here:")
    email_password = input('email password here:')#use app possword from google account
    user=input("Enter subject: ")
    user1=input("Enter body: ")
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Write a professional email subject for: {user}"},
        {"role": "user", "content": f"Write a professional email body for: {user1}"}
    ]
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages
    )
    print("\nGenerated Subject:", response.choices[0].message.content.split("\n")[0])
    print("\nGenerated Email Body:\n", "\n".join(response.choices[0].message.content.split("\n")[1:]))
    a=input("send email y/n:")
    if a=='y':
        subject=response.choices[0].message.content
        subject=subject.split("\n")[0]
        body = "\n".join(response.choices[0].message.content.split("\n")[1:])
        msg = EmailMessage()
        msg['Subject']=subject
        msg['From'] =sender_email
        msg['To'] =receiver_email
        msg.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, email_password)
            smtp.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!\n")
    if a=='n':
        print('why')
        user2=input("Enter modifications: ")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"previous subject: {subject}"},
            {"role": "user", "content": f"previous body: {body}"},
            {"role": "user", "content": f"Modify the previous email subject to include: {user2}"},
            {"role": "user", "content": f"Modify the previous email body to include: {user2}"}]
        
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=messages
        )
        print("\nModified Subject:", response.choices[0].message.content.split("\n")[0])
        print("\nModified Email Body:\n", "\n".join(response.choices[0].message.content.split("\n")[1:]))
        b=input("send modified email y/n:")
        if b=='y':
            subject=response.choices[0].message.content
            subject=subject.split("\n")[0]
            body = "\n".join(response.choices[0].message.content.split("\n")[1:])
            msg = EmailMessage()
            msg['Subject']=subject
            msg['From'] =sender_email
            msg['To'] =receiver_email
            msg.set_content(body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(sender_email, email_password)
                smtp.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully!\n")

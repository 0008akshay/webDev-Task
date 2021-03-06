from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField,validators

class ContactForm(Form):
  name = TextField("Name", [validators.Required("Please enter your name...")])
  email = TextField("Email",[validators.Required("Please enter your Email....")])
  subject = TextField("Subject",[validators.Required("Please enter your subject...")])
  message = TextAreaField("Message",[validators.Required("Please enter your message..")])
  submit = SubmitField("Send")
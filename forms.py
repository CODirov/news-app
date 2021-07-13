from wtforms import Form, StringField, PasswordField, validators

class UserRegister(Form):
    fullname = StringField("Fulllname", [validators.length(min=2,max=50)])

    username = StringField("Username", [validators.length(min=4, max=25), validators.DataRequired()])

    password = PasswordField("")
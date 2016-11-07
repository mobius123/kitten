import wtforms as wtf

class login_form(wtf.Form):
    ConsumerKey = wtf.TextField(
        label='ConsumerKey', validators=[wtf.validators.Required()])
    ConsumerSecret = wtf.PasswordField(
        label='ConsumerSecret', validators=[wtf.validators.Required()])

    def validate(self):
        if not wtf.Form.validate(self):
            return False

        user = self.get_user()

        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        return True

    def get_user(self):
        return db.session.query(User).filter_by(
            username=self.username.data).first()
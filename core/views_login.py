# views_login.py
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        # sessiyaga yozamiz
        self.request.session['welcome_username'] = self.request.user.username
        return response

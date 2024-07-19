from django.contrib.auth.mixins import LoginRequiredMixin


class LoginPatientRequiredMixin(LoginRequiredMixin):
    """
    Mixin for views that require a patient to be logged in.

    If the user is not logged in, they are redirected to the login page.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.patient:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

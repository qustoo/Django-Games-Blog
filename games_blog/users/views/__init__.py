from .auth_views import UserLoginView, UserLogoutView, UserRegistrationView
from .profile_view import UserProfileUpdateView, UserProfileDetailView
from .feedback_view import FeedbackCreateView
from .email_confirm_view import EmailConfirmationSendView, EmailConfirmationSuccessView, EmailConfirmationFailedView, \
    ConfirmUserEmailView
from .reset_password_view import UserPasswordResetView, UserPasswordResetDoneView, UserPasswordResetConfirmView, \
    UserPasswordResetCompleteView
from .change_password_view import ChangePasswordView

__all__ = [
    "UserLoginView",
    "UserLogoutView",
    "UserRegistrationView",
    "UserProfileDetailView",
    "UserProfileUpdateView",
    "FeedbackCreateView",
    "EmailConfirmationSendView",
    "EmailConfirmationSuccessView",
    "EmailConfirmationFailedView",
    "ConfirmUserEmailView",
    "UserPasswordResetView",
    "UserPasswordResetDoneView",
    "UserPasswordResetConfirmView",
    "UserPasswordResetCompleteView",
    "ChangePasswordView",
]

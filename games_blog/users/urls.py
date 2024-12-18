from django.urls import path
from users.views import *
app_name = "users"

urlpatterns = [
    # Basic operations
    path(
        "login/", UserLoginView.as_view(redirect_authenticated_user=True), name="login"
    ),
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    # Reset password
    path("reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path(
        "reset/done/", UserPasswordResetDoneView.as_view(), name="password_reset_done"
    ),
    path(
        "reset/<str:uidb64>/<str:token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete/",
        UserPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

    # Change password
    path("password_change/", ChangePasswordView.as_view(), name="password_change"),
    # Feedback
    path("feedback/", FeedbackCreateView.as_view(), name="feedback"),
    # Edit/view profile
    path("edit/<slug:slug>", UserProfileUpdateView.as_view(), name="profile_edit"),
    path("detail/<slug:slug>/", UserProfileDetailView.as_view(), name="profile_detail"),
    # Email Confirmation
    path(
        "email-confirmation-send",
        EmailConfirmationSendView.as_view(),
        name="email_confirmation_send",
    ),
    path(
        "confirm-email/<str:uidb64>/<str:token>/",
        ConfirmUserEmailView.as_view(),
        name="confirm_email",
    ),
    path(
        "email-confirmation-success",
        EmailConfirmationSuccessView.as_view(),
        name="email_confirmation_success",
    ),
    path(
        "email-confirmation-failed",
        EmailConfirmationFailedView.as_view(),
        name="email_confirmation_failed",
    ),
    # Feedback
]

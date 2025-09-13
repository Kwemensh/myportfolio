# myApp/views.py
# myApp/views.py
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect   # ✅ correct import
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .forms import ContactForm


# Change this to your real email (receiver)
OWNER_EMAIL = getattr(settings, "PORTFOLIO_OWNER_EMAIL", None) or getattr(settings, "DEFAULT_FROM_EMAIL", None)
SITE_NAME = "Anne Clemence Ocampo — Portfolio"


def index(request: HttpRequest) -> HttpResponse:
    """
    Renders the single-page portfolio (home, work, services, about, contact).
    """
    return render(request, "home.html")   # we'll use your existing home.html for now


@require_POST
@csrf_protect
def contact_submit(request: HttpRequest) -> JsonResponse:
    """
    Handles the contact form submission via AJAX.
    Sends one email to you (owner) and a confirmation to the user.
    """
    form = ContactForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)

    data = form.cleaned_data

    # --- Email to owner ---
    subject_owner = f"📥 New inquiry from {data['full_name']} — {SITE_NAME}"
    body_owner_txt = render_to_string("emails/email_owner.txt", {"data": data, "site": SITE_NAME})
    body_owner_html = render_to_string("emails/email_owner.html", {"data": data, "site": SITE_NAME})

    owner_msg = EmailMultiAlternatives(
        subject_owner,
        body_owner_txt,
        settings.DEFAULT_FROM_EMAIL,
        [OWNER_EMAIL or settings.DEFAULT_FROM_EMAIL],
        reply_to=[data["email"]],
    )
    owner_msg.attach_alternative(body_owner_html, "text/html")
    owner_msg.send(fail_silently=False)

    # --- Confirmation to sender ---
    subject_user = f"✅ We got your message — {SITE_NAME}"
    body_user_txt = render_to_string("emails/email_user.txt", {"data": data, "site": SITE_NAME})
    body_user_html = render_to_string("emails/email_user.html", {"data": data, "site": SITE_NAME})

    user_msg = EmailMultiAlternatives(
        subject_user,
        body_user_txt,
        settings.DEFAULT_FROM_EMAIL,
        [data["email"]],
    )
    user_msg.attach_alternative(body_user_html, "text/html")
    user_msg.send(fail_silently=False)

    return JsonResponse({"ok": True})

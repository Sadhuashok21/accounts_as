from django.shortcuts import render, redirect
from django.http import HttpResponse
from shared_lib.sfs_core.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils import timezone
from shared_lib.utils import random, insertions
from django.urls import reverse
from urllib.parse import urlencode
from django.views import View
from . import utils


def logout(request):
    if request.user.is_authenticated:
        del request.session['user_id']
        
    return redirect('signin')



class SignUp(View):
    def get(self, request):
    
        insertions.insert_activity(random.get_client_ip(request), utils.version, "create-account", request.session.get('user_id', "anonymus"))
        return render(request, "create_account.html")

    # def get(self, request):
    #     print("SESSION KEY:", request.session.session_key)
    #     print("SAF:", request.session.get("saf"))

    #     return render(request, "skiltrix.html")
    
    def post(self, request):
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        name = request.POST.get('full_name', '')
        confirm_password = request.POST.get('con_password', '')
        redirect1 = request.GET.get('redirect', '')

        if email and password and name and confirm_password:
            if password == confirm_password:
                if AllUsers.objects.filter(email=email).exists():
                    messages.error(request, "An account with this email already exists.")
                else:
                    new_user = AllUsers(
                        email=email, 
                        name=name,
                        username = random.unique_id(),
                        lastname = "",
                        status="approved",
                        created_at=timezone.now(),
                        platform="website",
                        platform_name="sfs_blueprints",
                        type="manual",
                        user_id=random.unique_id(),
                        ip=request.META.get('REMOTE_ADDR', '')
                    )

                    new_user.set_password(password)
                    new_user.save()
                    insertions.insert_activity(random.get_client_ip(request), utils.version, "account-created", new_user.user_id)
          
                    url = reverse('signin')
                    if redirect1:
                        query_string = urlencode({'redirect': redirect1})
                        return redirect(f'{url}?{query_string}')
                    else:
                        return redirect(url)
            else:
                messages.error(request, "Passwords do not match.")
        else:
            messages.error(request, "All fields are required. *")

        return render(request, "create_account.html")


class SignIn(View):
    def get(self, request):



        # from django.core.mail import send_mail

     
        # """   send_mail(
        #     subject="Test Email",
        #     message="Hello from Django!",
        #     from_email="noreply@ascentracoresolutions.com",
        #     recipient_list=["ssimulator954@gmail.com"],
        #     fail_silently=False,
        # ) """

        # import imaplib
        # import email
        # from email.header import decode_header

        # MAIL_SERVER = "mail.ascentracoresolutions.com"
        # USERNAME = "noreply"          # or contact@ascentracoresolutions.com
        # PASSWORD = "Ashokkumar21"

        # mail = imaplib.IMAP4_SSL(MAIL_SERVER, 993)

        # mail.login(USERNAME, PASSWORD)

        # mail.select("INBOX")

        # status, messages = mail.search(None, "ALL")

        # mail_ids = messages[0].split()

        # for mail_id in mail_ids:

        #     status, msg_data = mail.fetch(mail_id, "(RFC822)")

        #     for response in msg_data:
        #         if not isinstance(response, tuple):
        #             continue

        #         msg = email.message_from_bytes(response[1])

        #         # Decode Subject
        #         subject, encoding = decode_header(msg["Subject"])[0]
        #         if isinstance(subject, bytes):
        #             subject = subject.decode(encoding or "utf-8", errors="ignore")

        #         print("=" * 80)
        #         print("ID:", mail_id.decode())
        #         print("From:", msg.get("From"))
        #         print("To:", msg.get("To"))
        #         print("CC:", msg.get("Cc"))
        #         print("BCC:", msg.get("Bcc"))
        #         print("Subject:", subject)
        #         print("Date:", msg.get("Date"))

        #         body = ""

        #         if msg.is_multipart():

        #             for part in msg.walk():

        #                 content_type = part.get_content_type()
        #                 disposition = str(part.get("Content-Disposition"))

        #                 if "attachment" in disposition:
        #                     continue

        #                 if content_type == "text/plain":
        #                     charset = part.get_content_charset() or "utf-8"
        #                     body = part.get_payload(decode=True).decode(
        #                         charset,
        #                         errors="ignore"
        #                     )
        #                     break

        #             if not body:
        #                 for part in msg.walk():
        #                     if part.get_content_type() == "text/html":
        #                         charset = part.get_content_charset() or "utf-8"
        #                         body = part.get_payload(decode=True).decode(
        #                             charset,
        #                             errors="ignore"
        #                         )
        #                         break

        #         else:
        #             charset = msg.get_content_charset() or "utf-8"
        #             body = msg.get_payload(decode=True).decode(
        #                 charset,
        #                 errors="ignore"
        #             )

        #         print("\nBODY:\n")
        #         print(body)
        #         print("=" * 80)





        type = request.GET.get('type', '')
        re = request.GET.get('redirect', '')

        if type:
            if type == 'sfs-blueprints':
                print ('sfs-blueprints')
                return render(request, "index.html")

        insertions.insert_activity(random.get_client_ip(request), utils.version, "sign-in", request.session.get('user_id', "anonymus"))
        return render(request, "index.html")

    def post(self, request):
        redirect1 = request.GET.get('redirect', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        type = request.GET.get('type', '')

        if type:
            pass

        if request.user.is_authenticated:
            return HttpResponse("already")

        if email and password:
            user = authenticate(request, email=email, password=password)
            
            if user:
                login(request, user)
                if redirect1:
                    insertions.insert_activity(random.get_client_ip(request), utils.version, "logged-in-redirect", user.user_id)
                    return redirect(redirect1)
                else:
                    
                    insertions.insert_activity(random.get_client_ip(request), utils.version, "logged-in", user.user_id)
                    return redirect('https://www.ascentracoresolutions.com')
            else:
                messages.error(request, "Invalid email or password.")

        return render(request, "index.html")


class DeleteAccount(View):
    def get(self, request):
        insertions.insert_activity(random.get_client_ip(request), utils.version, "delete-account", request.session.get('user_id', "anonymus"))
        return render(request, "delete_account.html")
    
    def post(self, request):
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if email and password:
            user = AllUsers.objects.filter(email=email, password=password, status="approved").first()

            if user:
                user.status = "deleted"
                user.save()
                insertions.insert_activity(random.get_client_ip(request), utils.version, "account-deleted", user.user_id)
                messages.success(request, "Your account has been deleted.")
            else:            
                messages.error(request, "Invalid email or password.")        

        return render(request, "delete_account.html")


class ForgotPassword(View):
    def get(self, request):
        insertions.insert_activity(random.get_client_ip(request), utils.version, "forgot-password", request.session.get('user_id', "anonymus"))
        return render(request, "forgot_password.html")

    def post(self, request):
        email = request.POST.get('email', '')

        if email:
            user = AllUsers.objects.filter(email=email, status="approved").first()
            if user:
                insertions.insert_activity(random.get_client_ip(request), utils.version, "forgot-password-request", user.user_id)
                messages.success(request, "Password reset instructions have been sent to your email.")
            else:
                messages.error(request, "No account found with that email address.")

        return render(request, "forgot_password.html")


class VerifyOTP(View):
    def get(self, request):
        insertions.insert_activity(random.get_client_ip(request), utils.version, "verify-otp", request.session.get('user_id', "anonymus"))
        return render(request, "verify_otp.html")

    def post(self, request):
        email = request.POST.get('email', '')
        otp = request.POST.get('otp', '')

        if email and otp:
            user = AllUsers.objects.filter(email=email, status="approved").first()
            if user and user.otp == otp:
                messages.success(request, "OTP verified successfully.")
                # You can redirect to a password reset page or dashboard here
            else:
                messages.error(request, "Invalid email or OTP.")
        else:
            messages.error(request, "Email and OTP are required.")

        return render(request, "verify_otp.html")



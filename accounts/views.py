from django.shortcuts import render, redirect
from django.http import HttpResponse
from shared_lib.sfs_core.models import *
from django.contrib import messages
from django.utils import timezone
from shared_lib.utils import random, insertions
from django.urls import reverse
from urllib.parse import urlencode
from django.views import View
from . import utils



def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        
    return redirect('signin')




class SignUp(View):
    def get(self, request):
        insertions.insert_activity(random.get_client_ip(request), utils.version, "create-account", request.session.get('user_id', "anonymus"))
        return render(request, "create_account.html")
    
    def post(self, request):
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        name = request.POST.get('full_name', '')
        confirm_password = request.POST.get('con_password', '')
        redirect = request.GET.get('redirect', '')

        if email and password and name and confirm_password:
            if password == confirm_password:
                if AllUsers.objects.filter(email=email).exists():
                    messages.error(request, "An account with this email already exists.")
                else:
                    new_user = AllUsers.objects.create(
                        email=email, 
                        password=password, 
                        name=name, 
                        status="approved",
                        time=timezone.now(),
                        platform="website",
                        platform_name="sfs_blueprints",
                        user_type="user",
                        type="manual",
                        user_id=random.unique_id(),
                        profile="",
                        ip=request.META.get('REMOTE_ADDR', '')
                    )

                    insertions.insert_activity(random.get_client_ip(request), utils.version, "account-created", new_user.user_id)
          
                    url = reverse('signin')
                    if redirect:
                        query_string = urlencode({'redirect': redirect})
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

        insertions.insert_activity(random.get_client_ip(request), utils.version, "sign-in", request.session.get('user_id', "anonymus"))
        return render(request, "index.html")

    def post(self, request):
        redirect1 = request.GET.get('redirect', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if 'user_id' in request.session:
            return HttpResponse("already")

        if email and password:
            user = AllUsers.objects.filter(email=email, password=password, status="approved").first()

            if user:

                request.session['user_id'] = user.user_id
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



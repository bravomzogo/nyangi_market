import random
import string
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models_password_reset import PasswordResetCode
from .models import Profile

def password_reset_choice(request):
    """
    Display the password reset method choice page (WhatsApp or Email)
    If the user has a WhatsApp number and has WhatsApp recovery enabled,
    automatically redirect to WhatsApp recovery.
    """
    # Check if user provided their username or email in the query parameter
    username_or_email = request.GET.get('identifier', '')
    
    if username_or_email:
        # Try to find the user by username or email
        try:
            # First try to find by username
            user = User.objects.filter(username=username_or_email).first()
            
            # If not found by username, try email
            if not user:
                user = User.objects.filter(email=username_or_email).first()
                
            # If user found and has WhatsApp recovery enabled with a phone number, redirect to WhatsApp recovery
            if user and hasattr(user, 'profile') and user.profile.use_whatsapp_for_recovery and user.profile.phone_number:
                # Store username in session for the WhatsApp flow
                request.session['reset_username'] = user.username
                return redirect('password_reset_whatsapp')
                
        except Exception:
            # If any error occurs, just show the choice page
            pass
            
    return render(request, 'myapp/password_reset_choose.html')

def password_reset_whatsapp(request):
    """
    Handle WhatsApp-based password reset requests
    """
    # Check if username is in session (from the identifier form)
    username = request.session.get('reset_username', '')
    prefill_phone = ''
    
    # If username is in session, try to get the user's phone number
    if username:
        try:
            user = User.objects.get(username=username)
            if hasattr(user, 'profile') and user.profile.phone_number:
                prefill_phone = user.profile.phone_number
        except User.DoesNotExist:
            pass
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        
        # Clean the phone number (remove spaces, ensure it has country code)
        phone_number = ''.join(phone_number.split())
        if not phone_number.startswith('+'):
            messages.error(request, 'Please enter a valid phone number with country code (e.g., +255XXXXXXXXX)')
            return render(request, 'myapp/password_reset_whatsapp.html', {'prefill_phone': prefill_phone})
        
        # Find the user with this phone number
        try:
            profile = Profile.objects.get(phone_number=phone_number)
            user = profile.user
            
            # Generate a verification code
            code = ''.join(random.choices(string.digits, k=6))
            expires_at = timezone.now() + timedelta(minutes=15)
            
            # Save the code
            reset_code = PasswordResetCode.objects.create(
                user=user,
                code=code,
                expires_at=expires_at
            )
            
            # Here you would integrate with WhatsApp API to send the code
            # For demonstration, we'll just show a message
            
            # In a real implementation, you would send the code via WhatsApp API
            # Example: send_whatsapp_message(phone_number, f"Your verification code is: {code}")
            
            messages.success(request, f"A verification code has been sent to your WhatsApp number. The code is: {code}")
            
            # Store the phone number in session for the verification step
            request.session['reset_phone_number'] = phone_number
            
            return redirect('password_reset_whatsapp_verify')
            
        except Profile.DoesNotExist:
            messages.error(request, 'No account found with this WhatsApp number.')
    
    return render(request, 'myapp/password_reset_whatsapp.html', {'prefill_phone': prefill_phone})

def password_reset_whatsapp_verify(request):
    """
    Verify the WhatsApp verification code
    """
    phone_number = request.session.get('reset_phone_number')
    
    if not phone_number:
        messages.error(request, 'Session expired. Please try again.')
        return redirect('password_reset_whatsapp')
    
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        
        try:
            profile = Profile.objects.get(phone_number=phone_number)
            user = profile.user
            
            # Find the most recent unused code for this user
            reset_code = PasswordResetCode.objects.filter(
                user=user,
                is_used=False,
                expires_at__gt=timezone.now()
            ).latest('created_at')
            
            if reset_code.code == verification_code:
                # Mark the code as used
                reset_code.is_used = True
                reset_code.save()
                
                # Store user ID in session for the reset step
                request.session['reset_user_id'] = user.id
                
                return redirect('password_reset_whatsapp_confirm')
            else:
                messages.error(request, 'Invalid verification code. Please try again.')
        
        except (Profile.DoesNotExist, PasswordResetCode.DoesNotExist):
            messages.error(request, 'Invalid verification code or expired session. Please try again.')
    
    return render(request, 'myapp/password_reset_whatsapp_verify.html', {'phone_number': phone_number})

def password_reset_whatsapp_confirm(request):
    """
    Set a new password after WhatsApp verification
    """
    user_id = request.session.get('reset_user_id')
    
    if not user_id:
        messages.error(request, 'Session expired. Please try again.')
        return redirect('password_reset_whatsapp')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found. Please try again.')
        return redirect('password_reset_whatsapp')
    
    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if new_password1 != new_password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'myapp/password_reset_whatsapp_confirm.html')
        
        if len(new_password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'myapp/password_reset_whatsapp_confirm.html')
        
        # Set the new password
        user.set_password(new_password1)
        user.save()
        
        # Clear session data
        if 'reset_user_id' in request.session:
            del request.session['reset_user_id']
        if 'reset_phone_number' in request.session:
            del request.session['reset_phone_number']
        
        messages.success(request, 'Your password has been reset successfully.')
        return redirect('password_reset_complete')
    
    return render(request, 'myapp/password_reset_whatsapp_confirm.html')

def password_reset_email_form(request):
    """
    Handle email-based password reset requests
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, 'myapp/password_reset_email_form.html')
        
        try:
            # Find user by email
            user = User.objects.get(email=email)
            
            # Generate a reset code
            code = ''.join(random.choices(string.digits + string.ascii_uppercase, k=8))
            expires_at = timezone.now() + timedelta(hours=1)  # Code expires in 1 hour
            
            # Save the code
            reset_code = PasswordResetCode.objects.create(
                user=user,
                code=code,
                expires_at=expires_at
            )
            
            # Send email with reset code
            from django.core.mail import send_mail
            from django.conf import settings
            
            subject = 'Password Reset Code - Nyangi Marketplace'
            message = f"""
Hello {user.username},

You requested a password reset for your Nyangi Marketplace account.

Your password reset code is: {code}

This code will expire in 1 hour.

If you didn't request this password reset, please ignore this email.

Best regards,
Nyangi Marketplace Team
"""
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                # Store email in session for the next step
                request.session['reset_email'] = email
                messages.success(request, f'A reset code has been sent to {email}')
                return redirect('password_reset_email_verify')
                
            except Exception as e:
                messages.error(request, 'Failed to send email. Please try again later.')
                return render(request, 'myapp/password_reset_email_form.html')
            
        except User.DoesNotExist:
            # Don't reveal that the email doesn't exist for security reasons
            messages.info(request, f'If an account with email {email} exists, a reset code has been sent.')
            return render(request, 'myapp/password_reset_email_form.html')
    
    return render(request, 'myapp/password_reset_email_form.html')

def password_reset_email_verify(request):
    """
    Handle email verification code input
    """
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, 'Session expired. Please start the password reset process again.')
        return redirect('password_reset_choice')
    
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        
        if not code:
            messages.error(request, 'Please enter the verification code.')
            return render(request, 'myapp/password_reset_email_verify.html', {'email': email})
        
        try:
            # Find the user and valid reset code
            user = User.objects.get(email=email)
            reset_code = PasswordResetCode.objects.filter(
                user=user,
                code=code,
                expires_at__gt=timezone.now(),
                is_used=False
            ).first()
            
            if reset_code:
                # Mark code as used and store user ID in session
                reset_code.is_used = True
                reset_code.save()
                
                request.session['reset_user_id'] = user.id
                return redirect('password_reset_email_confirm')
            else:
                messages.error(request, 'Invalid or expired verification code.')
                
        except User.DoesNotExist:
            messages.error(request, 'Invalid session. Please start over.')
            return redirect('password_reset_choice')
    
    return render(request, 'myapp/password_reset_email_verify.html', {'email': email})

def password_reset_email_confirm(request):
    """
    Handle new password confirmation for email reset
    """
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, 'Session expired. Please start the password reset process again.')
        return redirect('password_reset_choice')
    
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if not password1 or not password2:
            messages.error(request, 'Please enter both password fields.')
            return render(request, 'myapp/password_reset_email_confirm.html')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'myapp/password_reset_email_confirm.html')
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'myapp/password_reset_email_confirm.html')
        
        try:
            user = User.objects.get(id=user_id)
            user.set_password(password1)
            user.save()
            
            # Clean up session data
            if 'reset_email' in request.session:
                del request.session['reset_email']
            if 'reset_user_id' in request.session:
                del request.session['reset_user_id']
            
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('password_reset_complete')
            
        except User.DoesNotExist:
            messages.error(request, 'Invalid session. Please start over.')
            return redirect('password_reset_choice')
    
    return render(request, 'myapp/password_reset_email_confirm.html')

def password_reset_complete_view(request):
    """
    Show success message after password reset
    """
    # Clear all reset-related session data
    keys_to_clear = ['reset_phone_number', 'reset_user_id', 'reset_username']
    for key in keys_to_clear:
        if key in request.session:
            del request.session[key]
            
    return render(request, 'myapp/password_reset_complete.html')

def resend_whatsapp_code(request):
    """
    API endpoint to resend a WhatsApp verification code
    """
    if request.method == 'POST':
        phone_number = request.session.get('reset_phone_number')
        
        if not phone_number:
            return JsonResponse({'success': False, 'error': 'Session expired'})
        
        try:
            profile = Profile.objects.get(phone_number=phone_number)
            user = profile.user
            
            # Generate a new verification code
            code = ''.join(random.choices(string.digits, k=6))
            expires_at = timezone.now() + timedelta(minutes=15)
            
            # Save the code
            reset_code = PasswordResetCode.objects.create(
                user=user,
                code=code,
                expires_at=expires_at
            )
            
            # Here you would integrate with WhatsApp API to send the code
            # For demonstration, we'll just show a success response
            
            return JsonResponse({'success': True, 'message': f'New code sent. For demo purposes, the code is: {code}'})
            
        except Profile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

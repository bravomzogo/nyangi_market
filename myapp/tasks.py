from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import logging
import io
from .pdf_utils import generate_pdf
from django.template.loader import get_template

logger = logging.getLogger(__name__)

def generate_receipt_pdf(payment, receipt):
    """
    Generate a PDF receipt for a payment.
    """
    try:
        # Get the PDF template
        template = get_template('myapp/email/receipt_pdf.html')
        
        # Render the template with context
        context = {
            'payment': payment,
            'receipt': receipt,
            'order': payment.order
        }
        html_string = template.render(context)
        
        # Generate PDF
        pdf_bytes = generate_pdf(html_string)
        if not pdf_bytes:
            return None
        pdf_file = io.BytesIO(pdf_bytes)
        return pdf_file
    except Exception as e:
        logger.error(f"Error generating PDF receipt for payment {payment.id}: {str(e)}")
        return None

def send_payment_approved_emails_with_pdf(payment_id):
    """
    Send payment approval emails with PDF receipts attached.
    This replaces the old email function with PDF attachment functionality.
    """
    from .models import Payment, Receipt
    
    try:
        payment = Payment.objects.get(id=payment_id)
        
        # Ensure receipt exists
        receipt, created = Receipt.objects.get_or_create(
            payment=payment,
            defaults={
                'order': payment.order,
                'transaction_id': f"PAY-{payment.id}"
            }
        )
        
        # Generate PDF receipt
        pdf_file = generate_receipt_pdf(payment, receipt)
        
        if not pdf_file:
            logger.error(f"Failed to generate PDF for payment {payment_id}")
            return False
        
        # Send email to buyer
        try:
            buyer_context = {
                'user': payment.user,
                'order': payment.order,
                'payment': payment,
                'receipt': receipt
            }
            buyer_msg_html = render_to_string('myapp/email/payment_approved_buyer.html', buyer_context)
            
            # Create email message
            buyer_email = EmailMessage(
                subject='Payment Approved - Receipt Attached',
                body='Your payment has been approved. Please find your receipt attached.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[payment.user.email],
            )
            buyer_email.attach(
                f'receipt_{receipt.transaction_id}.pdf',
                pdf_file.getvalue(),
                'application/pdf'
            )
            buyer_email.content_subtype = 'html'
            buyer_email.body = buyer_msg_html
            buyer_email.send(fail_silently=True)
            
            logger.info(f"Buyer email with PDF sent for payment {payment_id}")
        except Exception as e:
            logger.error(f"Error sending buyer email for payment {payment_id}: {str(e)}")

        # Reset PDF file for reuse
        pdf_file.seek(0)

        # Send emails to sellers with PDF receipts
        for item in payment.order.items.all():
            try:
                seller = item.product.seller
                if not seller.user.email:
                    logger.warning(f"No email address for seller {seller.id}")
                    continue
                    
                seller_context = {
                    'seller': seller,
                    'order': payment.order,
                    'item': item,
                    'payment': payment,
                    'receipt': receipt
                }
                seller_msg_html = render_to_string('myapp/email/payment_approved_seller.html', seller_context)
                
                # Create email message for seller
                seller_email = EmailMessage(
                    subject='Payment Received - Order Confirmation',
                    body='A new payment has been approved for your product.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[seller.user.email],
                )
                
                # Attach PDF receipt
                pdf_file.seek(0)  # Reset file pointer
                seller_email.attach(
                    f'receipt_{receipt.transaction_id}.pdf',
                    pdf_file.getvalue(),
                    'application/pdf'
                )
                seller_email.content_subtype = 'html'
                seller_email.body = seller_msg_html
                seller_email.send(fail_silently=True)
                
                logger.info(f"Seller email with PDF sent for payment {payment_id}, item {item.id}")
            except Exception as e:
                logger.error(f"Error sending seller email for payment {payment_id}, item {item.id}: {str(e)}")
    
        return True
        
    except Payment.DoesNotExist:
        logger.error(f"Payment with ID {payment_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error processing payment approval emails for payment {payment_id}: {str(e)}")
        return False

def approve_payment_without_emails(payment, user):
    """
    Approve a payment without sending any notification emails.
    This is used when sellers approve payments directly.
    """
    from django.utils import timezone
    from .models import Receipt
    
    try:
        # Update payment status
        payment.status = 'APPROVED'
        payment.approved_at = timezone.now()
        payment.approved_by = user
        payment.save()

        # Generate receipt
        receipt, created = Receipt.objects.get_or_create(
            payment=payment,
            defaults={
                'order': payment.order,
                'transaction_id': f"PAY-{payment.id}"
            }
        )
        
        logger.info(f"Payment {payment.id} approved by seller {user.username} without sending emails")
        return True
    except Exception as e:
        logger.error(f"Error approving payment {payment.id} without emails: {str(e)}")
        return False

def reject_payment_without_emails(payment, user):
    """
    Reject a payment without sending any notification emails.
    This is used when sellers reject payments directly.
    """
    from django.utils import timezone
    
    try:
        # Update payment status
        payment.status = 'REJECTED'
        payment.seller_reviewed_at = timezone.now()
        payment.save()
        
        logger.info(f"Payment {payment.id} rejected by seller {user.username} without sending emails")
        return True
    except Exception as e:
        logger.error(f"Error rejecting payment {payment.id} without emails: {str(e)}")
        return False

def send_payment_approved_emails_with_pdf(payment_id):
    """
    Send payment approval emails with PDF receipts attached.
    This replaces the old email function with PDF attachment functionality.
    """
    from .models import Payment, Receipt
    
    try:
        payment = Payment.objects.get(id=payment_id)
        
        # Ensure receipt exists
        receipt, created = Receipt.objects.get_or_create(
            payment=payment,
            defaults={
                'order': payment.order,
                'transaction_id': f"PAY-{payment.id}"
            }
        )
        
        # Generate PDF receipt
        pdf_file = generate_receipt_pdf(payment, receipt)
        
        if not pdf_file:
            logger.error(f"Failed to generate PDF for payment {payment_id}")
            return False
        
        # Send email to buyer
        try:
            buyer_context = {
                'user': payment.user,
                'order': payment.order,
                'payment': payment,
                'receipt': receipt
            }
            buyer_msg_html = render_to_string('myapp/email/payment_approved_buyer.html', buyer_context)
            
            # Create email message
            buyer_email = EmailMessage(
                subject='Payment Approved - Receipt Attached',
                body='Your payment has been approved. Please find your receipt attached.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[payment.user.email],
            )
            buyer_email.attach(
                f'receipt_{receipt.transaction_id}.pdf',
                pdf_file.getvalue(),
                'application/pdf'
            )
            buyer_email.content_subtype = 'html'
            buyer_email.body = buyer_msg_html
            buyer_email.send(fail_silently=True)
            
            logger.info(f"Buyer email with PDF sent for payment {payment_id}")
        except Exception as e:
            logger.error(f"Error sending buyer email for payment {payment_id}: {str(e)}")

        # Reset PDF file for reuse
        pdf_file.seek(0)

        # Send emails to sellers with PDF receipts
        for item in payment.order.items.all():
            try:
                seller = item.product.seller
                if not seller.user.email:
                    logger.warning(f"No email address for seller {seller.id}")
                    continue
                    
                seller_context = {
                    'seller': seller,
                    'order': payment.order,
                    'item': item,
                    'payment': payment,
                    'receipt': receipt
                }
                seller_msg_html = render_to_string('myapp/email/payment_approved_seller.html', seller_context)
                
                # Create email message for seller
                seller_email = EmailMessage(
                    subject='Payment Received - Order Confirmation',
                    body='A new payment has been approved for your product.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[seller.user.email],
                )
                
                # Attach PDF receipt
                pdf_file.seek(0)  # Reset file pointer
                seller_email.attach(
                    f'receipt_{receipt.transaction_id}.pdf',
                    pdf_file.getvalue(),
                    'application/pdf'
                )
                seller_email.content_subtype = 'html'
                seller_email.body = seller_msg_html
                seller_email.send(fail_silently=True)
                
                logger.info(f"Seller email with PDF sent for payment {payment_id}, item {item.id}")
            except Exception as e:
                logger.error(f"Error sending seller email for payment {payment_id}, item {item.id}: {str(e)}")
    
        return True
        
    except Payment.DoesNotExist:
        logger.error(f"Payment with ID {payment_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error processing payment approval emails for payment {payment_id}: {str(e)}")
        return False

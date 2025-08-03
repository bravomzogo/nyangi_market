from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_payment_approved_emails(payment_id):
    """
    Send payment approval emails asynchronously.
    This function can be called by a background task processor or directly.
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
        
        # Send email to buyer
        try:
            buyer_context = {
                'user': payment.user,
                'order': payment.order,
                'payment': payment,
                'receipt_url': f"/receipt/{receipt.id}/"
            }
            buyer_msg_html = render_to_string('myapp/email/payment_approved_buyer.html', buyer_context)
            send_mail(
                'Payment Approved - Your Receipt',
                'Your payment has been approved. Please find your receipt attached.',
                settings.DEFAULT_FROM_EMAIL,
                [payment.user.email],
                html_message=buyer_msg_html,
                fail_silently=True
            )
            logger.info(f"Buyer email sent for payment {payment_id}")
        except Exception as e:
            logger.error(f"Error sending buyer email for payment {payment_id}: {str(e)}")

        # Send email to sellers
        for item in payment.order.items.all():
            try:
                seller = item.product.seller
                seller_context = {
                    'seller': seller,
                    'order': payment.order,
                    'item': item,
                    'payment': payment
                }
                seller_msg_html = render_to_string('myapp/email/payment_approved_seller.html', seller_context)
                send_mail(
                    'New Payment Received',
                    'A new payment has been approved for your product.',
                    settings.DEFAULT_FROM_EMAIL,
                    [seller.user.email],
                    html_message=seller_msg_html,
                    fail_silently=True
                )
                logger.info(f"Seller email sent for payment {payment_id}, item {item.id}")
            except Exception as e:
                logger.error(f"Error sending seller email for payment {payment_id}, item {item.id}: {str(e)}")
    
    except Payment.DoesNotExist:
        logger.error(f"Payment with ID {payment_id} not found")
    except Exception as e:
        logger.error(f"Error processing payment approval emails for payment {payment_id}: {str(e)}")

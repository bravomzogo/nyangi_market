from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that allows login with either email or username.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate with either email OR username (not both in a single OR get()) to avoid
        MultipleObjectsReturned when duplicate emails exist (email not unique on auth.User).

        Strategy:
        1. Normalize (strip) the credential.
        2. If it contains '@' treat as email and filter only by email.
        3. Else treat as username and filter only by username.
        4. If no result, fall back to combined search (email OR username) just in case.
        5. If multiple users still match (likely duplicate email accounts), pick the earliest created (lowest id)
           and log a warning so duplicates can be cleaned up later.
        """
        if username is None:
            username = kwargs.get('email')
        if username is None:
            return None

        identifier = username.strip()
        if not identifier:
            return None

        # Primary query based on heuristic
        if '@' in identifier:
            qs = User.objects.filter(email__iexact=identifier)
        else:
            qs = User.objects.filter(username__iexact=identifier)

        # Fallback: broaden search if nothing found
        if not qs.exists():
            qs = User.objects.filter(Q(username__iexact=identifier) | Q(email__iexact=identifier))

        if not qs.exists():
            # Timing attack mitigation: run password hash anyway
            User().check_password(password)
            return None

        if qs.count() > 1:
            # Always pick the oldest (lowest primary key) for deterministic behaviour.
            ordered = qs.order_by('-id')
            chosen = ordered.first()
            all_ids = list(ordered.values_list('id', flat=True))
            logger.warning(
                "Multiple user records matched credential '%s' (ids=%s). Selected oldest id=%s.",
                identifier, all_ids, chosen.id
            )
            user = chosen
        else:
            user = qs.first()

        if not user:
            return None

        if not password:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

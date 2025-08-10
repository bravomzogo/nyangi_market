import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

@require_POST
def check_username_availability(request):
    """
    AJAX endpoint to check if a username is available.
    Returns JSON response with availability status.
    """
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        
        # Validate username length
        if len(username) < 3:
            return JsonResponse({'available': False, 'error': 'Username too short'})
            
        # Check if username already exists
        username_exists = User.objects.filter(username__iexact=username).exists()
        
        return JsonResponse({'available': not username_exists})
    except Exception as e:
        return JsonResponse({'available': False, 'error': str(e)}, status=400)

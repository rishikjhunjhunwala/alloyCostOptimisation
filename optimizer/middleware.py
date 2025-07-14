from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class OrganizationMiddleware(MiddlewareMixin):
    """
    Middleware to ensure users have organization access and provide organization context.
    """
    
    def process_request(self, request):
        """
        Process request to add organization context and check access.
        """
        # Skip organization check for these URLs
        excluded_paths = [
            '/admin/',
            '/login/',
            '/logout/',
            '/static/',
            '/media/',
        ]
        
        # Check if current path should be excluded
        if any(request.path.startswith(path) for path in excluded_paths):
            return None
        
        # Skip for unauthenticated users (let login redirect handle it)
        if not request.user.is_authenticated:
            return None
        
        # Check if user has a profile with organization
        if not hasattr(request.user, 'profile') or not request.user.profile.organization:
            messages.error(
                request, 
                'Your account is not associated with an organization. Please contact your administrator.'
            )
            return redirect('login')
        
        # Add organization to request for easy access
        request.organization = request.user.profile.organization
        
        return None

    def process_template_response(self, request, response):
        """
        Add organization context to template responses.
        """
        if hasattr(request, 'organization') and hasattr(response, 'context_data'):
            if response.context_data is None:
                response.context_data = {}
            response.context_data['current_organization'] = request.organization
        
        return response
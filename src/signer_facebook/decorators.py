import re
import facebook

from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured


def require_add(next=None):
    """
    Decorator for Django view that requires an added facebook application.
    The FacebookMiddleware must be installed.
    
    Redirecting after installation:
        To use the 'next' parameter to redirect to a specific page after login, a callable gets the 
        request object and should return a path relative to the Post-add URL.  
    """
    def decorator(view):
        def newview(request, *args, **kwargs):
            next = newview.next
            try:
                fb = request.facebook
            except:
                raise ImproperlyConfigured('Make sure you have the Facebook middleware installed.')
            
            next = callable(next) and next(request) or ''

            if not fb.check_session(request):
                if fb.added:
                    if request.method == 'GET' and fb.app_name:
                        return fb.redirect('%s%s' % (fb.get_app_url(), next))
                    return fb.redirect(fb.get_login_url(next=next))
                else:
                    return fb.redirect(fb.get_add_url(next=next))
            if not fb.added:
                return fb.redirect(fb.get_add_url(next=next))

            return view(request, *args, **kwargs)
        newview.next = next
        return newview
    return decorator


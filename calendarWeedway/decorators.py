from django.shortcuts import redirect
from django.urls import reverse

def google_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'credentials' not in request.session:

            login_url = reverse('calendar_init')
            return redirect(f"{login_url}?next={request.path}")
        
        return view_func(request, *args, **kwargs)

    return _wrapped_view

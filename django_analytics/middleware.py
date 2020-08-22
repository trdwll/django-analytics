from .models import GlobalPageHit, Visitor, VisitorPageHit
from django.db.models import F
from django.urls import reverse
from django.conf import settings

from ipware import get_client_ip
import ipinfo
import bleach

class PageViewsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the requested url isn't in the admin panel
        if not reverse('admin:index') in request.path or reverse('admin:index') + 'login/' in request.path or request.path == reverse('admin:index'):
            
            requested_url = bleach.clean(request.path)

            # Create the GlobalPageHit
            page_hit, page_hit_created = GlobalPageHit.objects.get_or_create(page_url=requested_url)
            page_hit.hit_count = F('hit_count') + 1
            page_hit.save()

            # Create the Visitor
            visitor_ip = get_client_ip(request)
            visitor, visitor_created = Visitor.objects.get_or_create(ip_address=visitor_ip[0]) 

            # if the ip is not localhost then do a lookup of the country for the ip
            if visitor_ip[0] not in ('localhost', '127.0.0.1'):
                handler = ipinfo.getHandler(settings.IPINFO_API_KEY)
                details = handler.getDetails(str(visitor_ip[0]))
                if details.country_name is not None:
                    visitor.ip_country = details.country_name
            
            visitor.user_agent = request.META['HTTP_USER_AGENT']
            visitor.save()

            # Create the VisitorPageHit
            visitor_page_hit, visitor_page_hit_created = VisitorPageHit.objects.get_or_create(page_url=requested_url, visitor=visitor)
            visitor_page_hit.hit_count = F('hit_count') + 1
            if not request.META['HTTP_USER_AGENT'] in visitor_page_hit.user_agent:
                visitor_page_hit.user_agent += '\n'+request.META['HTTP_USER_AGENT']
            visitor_page_hit.save() 

        return self.get_response(request)

        
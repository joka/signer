# -*- coding: utf-8 -*-

from django.conf import settings

def currentpage(request):

    return {
        'page_url': request.build_absolute_uri(),
        # 'page_url': '%s%s'%(settings.BASE_URL, request.get_full_path()),
        }


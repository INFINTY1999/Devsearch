from .models import profile,skill
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def paginateprofile(request,profiles,result):
    
    page = request.GET.get('page')
    paginators = Paginator(profiles,result)  

    try:
        profiles = paginators.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginators.page(page)
    except EmptyPage:
        page = paginators.num_pages
        profiles = paginators.page(page)
    
    leftindex = (int(page) -1)
    rightindex = (int(page) + 2)

    if leftindex < 1 :
        leftindex = 1

    if rightindex -1 > paginators.num_pages:
        rightindex = paginators.num_pages + 1

    custom_range = range(leftindex,rightindex)

    return (custom_range,profiles)


def searchprofiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    skills = skill.objects.filter(name__iexact=search_query)

    print('search:',search_query)
         
    profiles = profile.objects.distinct().filter(
        Q(name__icontains=search_query)|
        Q(short_intro__icontains=search_query)|
        Q(skill__in=skills)
        )
    return profiles ,search_query 
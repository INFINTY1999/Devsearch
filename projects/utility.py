from users.models import profile
from django.db.models import Q
from .models import project,Tag,Review
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def paginateprojects(request,projec,result):
    
    page = request.GET.get('page')
    paginators = Paginator(projec,result)  
        
    try:
        projec = paginators.page(page)
    except PageNotAnInteger:
        page = 1
        projec = paginators.page(page)
    except EmptyPage:
        page = paginators.num_pages
        projec = paginators.page(page)
    
    leftindex = (int(page) -1)
    rightindex = (int(page) + 2)

    if leftindex < 1 :
        leftindex = 1
        rightindex = (int(page) + 3)

    if rightindex -1 > paginators.num_pages:
        rightindex = paginators.num_pages + 1
        leftindex = (int(page) -2 )

    custom_range = range(leftindex,rightindex)

    return (custom_range,projec)

def searchproject(request):

    search_project = ''
    
    if request.GET.get('search_project'):
        search_project = request.GET.get('search_project')

    profil = profile.objects.filter(name__icontains=search_project)
    tags = Tag.objects.filter(name__icontains=search_project)
    
    projec = project.objects.distinct().filter(
        Q(Title__icontains = search_project)|
        Q(owner__in = profil)|
        Q(Tags__in = tags)
    )
    return(search_project,projec)

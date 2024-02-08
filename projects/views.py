from django.shortcuts import redirect, render
from .models import Project
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators  import login_required
from .forms import ProjectForm

projectsList = [
    {
        'id':'1',
        'title':'Ecommerce website',
        'description':'Fully functional ecommerce website'
    },
    {
        'id':'2',
        'title':'Portfolio website',
        'description':'Checkout to see my portfolio'
    },
    {
        'id':'3',
        'title':'Social Netowork',
        'description':'Awesome open source project, i am still working on'
    }
]

def projects(response):
    authenticated = True
    projects = Project.objects.all()
    context = {
        'auth':authenticated,
        'projects':projects
    }
    return render(response,'projects/projects.html',context)

def project(response,pk):
    projectObj = Project.objects.get(id=pk)
    #tags = projectObj.tags.all()
    """
    projectObj = None
    for i in projectsList:
        if i['id'] == pk:
            projectObj = i
    """
    return render(response,'projects/single-project.html',{'project':projectObj,
    #'tags':tags
    })

@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form':form}
    return render(request, "projects/project_form.html",context)

@login_required(login_url='login')
def updateProject(request,pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form':form}
    return render(request, "projects/project_form.html",context)

@login_required(login_url='login')
def deleteProject(request,pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('projects')
    context = {'project':project}
    return render(request, "projects/delete_project.html",context)
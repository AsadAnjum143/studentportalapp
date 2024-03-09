from django.shortcuts import render, redirect
from . models import Notes, Homework, Todo
from . forms import NotesForm, HomeworkForm, SearchForm, TodoForm, ConversionForm, ConversionLengthForm,ConversionMassForm, UserRegistrationForm
from django.contrib import messages
from django.views.generic import DetailView, UpdateView
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'portalapp/home.html')

@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes Added from {request.user.username} sucessfully!")
        form = NotesForm()
    else:  
        form = NotesForm()
        
    notes = Notes.objects.filter(user=request.user) #this notes is going to notes_details.html also from DB
    return render(request, 'portalapp/notes.html',locals())

@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


class NotesDetailView(DetailView):
    model = Notes

  
class NotesUpdateView(UpdateView):
    model = Notes
    
@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request,f'Homework Added from {request.user.username}!!')
            form = HomeworkForm()
        
    else:
        form = HomeworkForm()
    data = Homework.objects.filter(user= request.user)
    if len(data) == 0:
        homework_done = True
    else:
        homework_done = False
    return render(request, 'portalapp/homework.html',locals())

@login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request,pk):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')


def youtube(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit = 100)
        result_list = []
        for i in video.result()['result']:
            
            #print(video.result())
            #output for above print,  {'result': [{'type': 'video', 'id': 'bmfA5xhGNJQ', 'title': 'Ishq Murshid - Episode 21 [𝐂𝐂] - 25 F  eb 24 - Sponsored By Khurshid Fans, Master Paints & Mothercare', 'publishedTime': '12 days ago', 'duration': '34:04', 'viewCount': {'text': '32,464,335 views', 'short': '32M views'}, 'thumbnails': [{'url': 'https://i.ytimg.com/vi/bmfA5xhGNJQ/hq720.jpg?sqp=-oaymwEcCOgCEMoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLAiW4UYG5jCoFdLz9SP35ek6ofxwg', 'width': 360, 'height': 202}, {'url': 'https://i.ytimg.com/vi/bmfA5xhGNJQ/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLB69Dv9SRGwiqU6x4JZutIOGnEWJQ', 'width': 720, 'height': 404}], 'richThumbnail': {'url': 'https://i.ytimg.com/an_webp/bmfA5xhGNJQ/mqdefault_6s.webp?du=3000&sqp=COjNr68G&rs=AOn4CLC_MdxTOL_zCXr8669_afcIn8wloQ', 'width': 320, 'height': 180}, 'descriptionSnippet': [{'text': 'Ishq Murshid', 'bold': True}, {'text': ' - Episode 21 [CC] - 25 Feb 24 - Sponsored By Khurshid Fans, Master Paints & Mothercare A journey filled with love,\xa0...'}], 'channel': {'name': 'HUM TV', 'id': 'UCEeEQxm6qc_qaTE7qTV5aLQ', 'thumbnails': [{'url': 'https://yt3.ggpht.com/OZT5Uprp0zQxZv7_Co0WQ8KHJEGnjpWWUgeDSANdjWOduVacF_g-qeTWXbq_PJ4hRlhBXp8m=s68-c-k-c0x00ffffff-no-rj', 'width': 68, 'height': 68}], 'link': 'https://www.youtube.com/channel/UCEeEQxm6qc_qaTE7qTV5aLQ'}, 'accessibility': {'title': 'Ishq Murshid - Episode 21 [𝐂𝐂] - 25 Feb 24 - Sponsored By Khurshid Fans, Mast  er Paints & Mothercare by HUM TV 32,464,335 views 12 days ago 34 minutes', 'duration': '34 minutes, 4 seconds'}, 'link': 'https://www.youtube.com/watch?v=bmfA5xhGNJQ', 'shelfTitle': None}]}
            #print()
            #print(video.result()['result'])
            #output for above in the form of list, [{'type': 'video', 'id': 'bmfA5xhGNJQ', 'title': 'Ishq Murshid - Episode 21 [𝐂𝐂] - 25 Feb 24 - Spo  nsored By Khurshid Fans, Master Paints & Mothercare', 'publishedTime': '12 days ago', 'duration': '34:04', 'viewCount': {'text': '32,465,383 views', 'short': '32M views'}, 'thumbnails': [{'url': 'https://i.ytimg.com/vi/bmfA5xhGNJQ/hq720.jpg?sqp=-oaymwEcCOgCEMoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLAiW4UYG5jCoFdLz9SP35ek6ofxwg', 'width': 360, 'height': 202}, {'url': 'https://i.ytimg.com/vi/bmfA5xhGNJQ/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLB69Dv9SRGwiqU6x4JZutIOGnEWJQ', 'width': 720, 'height': 404}], 'richThumbnail': {'url': 'https://i.ytimg.com/an_webp/bmfA5xhGNJQ/mqdefault_6s.webp?du=3000&sqp=COjNr68G&rs=AOn4CLC_MdxTOL_zCXr8669_afcIn8wloQ', 'width': 320, 'height': 180}, 'descriptionSnippet': [{'text': 'Ishq Murshid', 'bold': True}, {'text': ' - Episode 21 [CC] - 25 Feb 24 - Sponsored By Khurshid Fans, Master Paints & Mothercare A journey filled with love,\xa0...'}], 'channel': {'name': 'HUM TV', 'id': 'UCEeEQxm6qc_qaTE7qTV5aLQ', 'thumbnails': [{'url': 'https://yt3.ggpht.com/OZT5Uprp0zQxZv7_Co0WQ8KHJEGnjpWWUgeDSANdjWOduVacF_g-qeTWXbq_PJ4hRlhBXp8m=s68-c-k-c0x00ffffff-no-rj', 'width': 68, 'height': 68}], 'link': 'https://www.youtube.com/channel/UCEeEQxm6qc_qaTE7qTV5aLQ'}, 'accessibility': {'title': 'Ishq Murshid - Episode 21 [𝐂𝐂] - 25 Feb 24 - Sponsored By Khurshid Fans, Master Paints &   Mothercare by HUM TV 32,465,383 views 12 days ago 34 minutes', 'duration': '34 minutes, 4 seconds'}, 'link': 'https://www.youtube.com/watch?v=bmfA5xhGNJQ', 'shelfTitle': None}]
           
            result_dict = {
                'input':'text',
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc = desc + j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
        return render(request,'portalapp/youtube.html',locals())
    else:
        form = SearchForm()
    return render(request, 'portalapp/youtube.html',locals())

@login_required
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:  #without try block this is the error we get --> IntegrityError at /todo/
                                                            # NOT NULL constraint failed: portalapp_todo.user_id
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request,f"Todo Added from {request.user.username}!!")
            form = TodoForm()           
    else:
        form = TodoForm()
    data = Todo.objects.filter(user = request.user)
    if len(data) == 0:
        todo_done = True
    else:
        todo_done = False
    return render(request,'portalapp/todo.html',locals())

@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

@login_required
def update_todo(request, pk=None):
    mark_as_completed = Todo.objects.get(id=pk)
    if mark_as_completed.is_finished == True:
        mark_as_completed.is_finished = False
    else:
        mark_as_completed.is_finished = True
    mark_as_completed.save()
    return redirect('todo')


def book(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text #This will return json response
        response = requests.get(url)
        answer = response.json() #converting into dictionary
        print(answer)
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)
        return render(request,'portalapp/books.html',locals()) #in context we have to pass result_list, here locals() is using so not passing
    else:
        form = SearchForm()
    return render(request, 'portalapp/books.html',locals())

def dictionary(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text #This will return json response
        response = requests.get(url)
        answer = response.json() #converting into dictionary
        print(answer)
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context = {
                'form':form,
                'input':'',
            }
        return render(request, 'portalapp/dictionary.html',context)
        
    else:
        form = SearchForm()
    context = {'form':form}
    return render(request, 'portalapp/dictionary.html',context)

def wiki(request):
    if request.method == "POST":
        text = request.POST['text']
        form = SearchForm(request.POST)
        search = wikipedia.page(text)
        title = search.title,
        link = search.url,
        details = search.summary
        return render(request, 'portalapp/wiki.html',locals())
    else:
        form = SearchForm()
    return render(request, 'portalapp/wiki.html',locals())

def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form': measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >=0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form': measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >=0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
    else:
        form = ConversionForm()
        context = {
            'form':form,
            'input':False
        }
    return render(request, 'portalapp/conversion.html',context)

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Created for {username}!!")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, 'portalapp/register.html',locals())

@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished = False, user = request.user)
    todos = Todo.objects.filter(is_finished = False, user = request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
        
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
        
    return render(request, 'portalapp/profile.html',locals())
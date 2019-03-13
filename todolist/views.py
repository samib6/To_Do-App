from django.shortcuts import render,redirect
from django.contrib import messages,auth
from .models import TodoList, Category
import datetime
from django.core.mail import EmailMessage
from django.utils.datastructures import MultiValueDictKeyError

def index(request): #the index view
    print('inside index')
    todos = TodoList.objects.all()#quering all todos with the object manager
    categories = Category.objects.all() #getting all categories with object manager
    context = {"todos": todos, "categories":categories};
    tododate =TodoList.objects.all().values_list('due_date',flat=True)
    for td in tododate:
        print('entered td')
        print(td)
        if td == datetime.date.today():
            text = 'its time for you to complete your task for today'
            email = EmailMessage('Reminder',text,to=['sameekshabhatia6@gmail.com'])
            print('sent')
            email.send()
        else:
            print('not sent')

    if request.method == "POST": #checking if the request method is a POST

        if "taskAdd" in request.POST: #checking if there is a request to add a todo
            title = request.POST["description"] #title
            date = str(request.POST["date"]) #date
            category = request.POST["category_select"] #category

            content = title + " -- " + date + " " + category #content
            Todo = TodoList(title=title, content=content, due_date=date, category=Category.objects.get(name=category))
            Todo.save() #saving the todo
            return redirect("/") #reloading the page

        if "taskDelete" in request.POST: #checking if there is a request to delete a todo
            try:
                checkedlist = request.POST["checkedbox"] #checked todos to be deleted
                for todo_id in checkedlist:
                    todo = TodoList.objects.get(id=int(todo_id)) #getting todo id
                    todo.delete() #deleting tode
            except MultiValueDictKeyError:
                checkedlist = False






    return render(request, "index.html", context)

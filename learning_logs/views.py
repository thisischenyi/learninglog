from django.shortcuts import render
from .models import Topic, Entry
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """learning logs homepage"""
    return render(request, 'learning_logs/index.html')

def help(request):
    """learning logs help page"""
    return render(request, 'learning_logs/help.html')

def topics(request):
    """list all topics"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics':topics}
    return render(request,'learning_logs/topics.html',context)

def topic(request,topic_id):
    """list entries for one topic"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request,'learning_logs/topic.html',context)

def new_topic(request):
    """user add new topic"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id):
    """add an entry to the topic"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid:
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    """edit existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
    if request.method != 'POST':
        #use current entry content to fill the form when fist request
        form = EntryForm(instance=entry)
    else:
        #for POST request, process the data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))
        
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)

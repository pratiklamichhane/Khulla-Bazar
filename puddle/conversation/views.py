from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from .forms import ConversationMessageForm
from .models import Conversation
from django.contrib.auth.decorators import login_required

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from .forms import ConversationMessageForm
from .models import Conversation
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard:index')

    # Check if a conversation for this item already exists, or create a new one
    conversation, created = Conversation.objects.get_or_create(item=item)
    
    if not conversation.members.filter(id=request.user.id).exists():
        conversation.members.add(request.user)
        conversation.members.add(item.created_by)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {'form': form})

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations  # Pass the variable, not the string
    })

@login_required
def detail(request, pk):
    try:
        conversation = Conversation.objects.get(pk=pk, members=request.user)
    except Conversation.DoesNotExist:
        return redirect('conversation:inbox')
    
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()
            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()  # Assign the form object here

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })
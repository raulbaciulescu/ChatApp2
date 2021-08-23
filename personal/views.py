from django.shortcuts import render

# Create your views here.
from public_chat.forms import ComposeForm


def home(request):
    #return render(request, 'personal/home.html', {})
    context = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ComposeForm(request.POST)
            if form.is_valid():
                context['user'] = request.user
                # ChatMessage.objects.create(user=request.user, thread=thread, message=message)
        else:
            form = ComposeForm()

        context['form'] = form
        context['user'] = request.user
    return render(request, 'public_chat/room.html', {})
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from markdown2 import Markdown
from .models import Note
from .forms import NewNote
from xhtml2pdf import pisa
# from cStringIO import StringIO

def index(request):
    if 'username' not in request.session:
        return HttpResponseRedirect('../users')
    data = [ i for i in Note.objects.all() if i.owner == request.session['username']]
    context = dict()
    context['username'] = request.session['username']
    context['data'] = data
    temp = loader.get_template('notes/index.html')
    return HttpResponse(temp.render(context, request))


def new_note(request):
    if request.method == 'POST' and 'b2' in request.POST :
        form = NewNote(request.POST)
        if form.is_valid():
            new = Note()
            new.owner = request.session['username']
            new.head = form.cleaned_data["heading"]
            new.content = form.cleaned_data["content"]
            con = Markdown()
            new.md = con.convert(new.content)
            new.save()
            return HttpResponseRedirect("./")
    if request.method == 'POST' and 'b1' in request.POST :
        form = NewNote(request.POST)
        if form.is_valid():
            con=Markdown()
            request.session['temp'] = con.convert(form.cleaned_data['content'])

            return HttpResponseRedirect('preview')
    data = [i for i in Note.objects.all() if i.owner == request.session['username']]

    context = dict()
    context['data'] = data
    context['form'] = NewNote()
    context['username'] = request.session['username']
    temp = loader.get_template('notes/newnote.html')
    return HttpResponse(temp.render(context, request))


def preview(request):
    context=dict()
    context['note'] = request.session['temp']
    #request.session['temp'] = ''
    temp = loader.get_template('notes/preview.html')
    return HttpResponse(temp.render(context, request))

def view(request, note_id):
    try:

        note = Note.objects.filter(id=note_id)[0]
    except:
        return HttpResponse('404 Thats an Error!!<br><hr>', status=404)
    if note.owner!=request.session['username']:
        return HttpResponse('Unauthorized', status=401)
    context = dict()
    context['head'] = note.head
    context['body'] = note.md
    context['note_id'] = note_id
    context['username'] = request.session['username']
    temp = loader.get_template('notes/view.html')
    return HttpResponse(temp.render(context,request))


def edit(request, note_id):
    if request.method == 'POST' and 'b2' in request.POST:
        try:

            note = Note.objects.filter(id=note_id)[0]

        except:

            return HttpResponse('404 Thats an Error!!<br><hr>', status=404)
        if note.owner != request.session['username']:
            return HttpResponse('Unauthorized', status=401)
        form = NewNote(request.POST)
        if form.is_valid():
            note.head = form.cleaned_data['heading']
            note.content = form.cleaned_data['content']
            con = Markdown()
            note.md = con.convert(note.content)
            note.save()
            return HttpResponseRedirect("/")
    if request.method == 'POST' and 'b1' in request.POST :
        form = NewNote(request.POST)
        if form.is_valid():
            con=Markdown()
            request.session['temp'] = con.convert(form.cleaned_data['content'])
            return HttpResponseRedirect('preview')

    try:

        note = Note.objects.filter(id=note_id)[0]

    except:
        return HttpResponse('404 Thats an Error!!<br><hr>', status=404)
    if note.owner!=request.session['username']:
        return HttpResponse('Unauthorized', status=401)
    data = dict()
    data['heading'] = note.head
    data['content'] = note.content

    form = NewNote(data)
    context = dict()
    context['form'] = form
    context['username'] = request.session['username']
    temp = loader.get_template('notes/edit.html')
    return HttpResponse(temp.render(context, request))


def delete(request, note_id):
    try:

        note = Note.objects.filter(id=note_id)[0]

    except:
        return HttpResponse('404 Thats an Error!!<br><hr>', status=404)
    if note.owner!=request.session['username']:
        return HttpResponse('Unauthorized', status=401)
    Note.objects.filter(id=note_id).delete()
    return HttpResponseRedirect('./')


def download(request, note_id):
    try:
        note = Note.objects.filter(id=note_id)[0]
    except:
        return HttpResponse('404 Thats an Error!!<br><hr>', status=404)
    if note.owner != request.session['username']:
        return HttpResponse('Unauthorized', status=401)
    # pdf = StringIO()
    # pisa.CreatePDF(StringIO((note.md).encode('utf-8')), pdf)
    # resp = pdf.getvalue()
    # pdf.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ScribbleMD.pdf"'
    # response.write(resp)
    return response

def logout(request):
    request.session.pop('username')
    return HttpResponseRedirect('./users')

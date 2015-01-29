from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from app.forms import DocumentForm
from app.models import Document
from django.views.generic.edit import UpdateView, DeleteView
from django.db import transaction
import reversion
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.db.models import Q
from django.conf import settings

# Create your views here.

def home(request):
    query = Document.objects.all()
    in_draft = query.filter(status='draft').order_by('measure_type', 'measure_number')
    pending = query.filter(status='review').order_by('measure_type', 'measure_number')
    final = query.filter(status='published').order_by('-publish_date')[:5]
    return render(request,'home.html', {'draft':in_draft, 'pending':pending, 'final':final})

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Rss201rev2Feed

class LatestEntriesFeed(Feed):
    title = "Fiscal Impact Statements -- Council of the District of Columbia"
    link = "https://fiscalimpact.herokuapp.com/"
    description = "Fiscal Impact Statements for the Council of the District of Columbia."

    feed_type = Rss201rev2Feed

    def items(self):
        return Document.objects.order_by('-publish_date')[:20]

    def item_title(self, item):
        return item.short_title

    def item_description(self, item):
        return item.content

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return item.get_public_url()



###
# Create a new Document
###

def view_documents(request):
    documents = Document.objects.all().order_by('-publish_date').filter(status='published')
    return render(request, 'view.html', {'documents': documents})

def print_documents(request, pk):
    document = Document.objects.get(slug=pk)
    return render(request, 'print.html', {'document':document, 'stamp_url':settings.STAMP_URL})

def published_query(request):
    data = Document.objects.all().values('slug', 'office', 'measure_number', 'measure_type', 'short_title', 'content', 'publish_date')
    # Allow full-text search against content/short_title
    if request.GET.__contains__('q'):
        q = request.GET['q']
        query = Q(content__icontains=q) | Q(short_title__icontains=q)
        data = data.filter(query)
    data = data.filter(status="published")
    return HttpResponse(json.dumps(list(data), cls=DjangoJSONEncoder),content_type='application/json')

def search(request):
    if request.GET.__contains__('q'):   
        q = request.GET.get('q') 
        data = Document.objects.all()#.values('slug', 'office', 'measure_number', 'measure_type', 'short_title', 'content', 'publish_date')
        query = Q(content__icontains=q) | Q(short_title__icontains=q)
        data = data.filter(query)
        data = data.filter(status="published")
        return render(request, 'search.html', {'results': data})
    return render(request, 'search.html', {})

@login_required
@reversion.create_revision()
def new_document(request):
    form = DocumentForm()
    if request.method == "POST":
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.save()
            if request.POST.get('status') == 'published' and request.user.has_perm('app.can_publish'):
                document.publish()
            elif request.POST.get('status') == 'published':
                document.status = 'review'
            document.attorney = request.user
            document.save()
            return redirect('home')
        return render(request,'app/new_document.html', {'form':form, 'errors':form.errors})
    return render(request,'app/new_document.html', {'form':form})

class DocumentUpdate(UpdateView):
    model = Document
    form_class = DocumentForm
    success_url = '/'
    
    @reversion.create_revision()
    def form_valid(self, form):
        self.document = form.save()
        if self.request.POST.get('status') == 'published' and self.request.user.has_perm('app.can_publish'):
            self.document.publish()
        elif self.request.POST.get('status') == 'published':
            self.document.status = 'review'
        self.document.save()
        return super(DocumentUpdate, self).form_valid(form)

class DocumentDelete(DeleteView):
    model = Document
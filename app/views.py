from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from app.forms import LegalSufficiencyForm
from app.models import LegalSufficiency
from django.views.generic.edit import UpdateView, DeleteView
# Create your views here.

def home(request):
    query = LegalSufficiency.objects.all()
    in_draft = query.filter(status='draft')
    pending = query.filter(status='review')
    final = query.filter(status='published')[:5]
    return render(request,'home.html', {'draft':in_draft, 'pending':pending, 'final':final})

###
# Create a new Document
###

def view_sufficiencies(request):
    sufficiencies = LegalSufficiency.objects.all().filter(status='published')
    return render(request, 'view.html', {'sufficiencies':sufficiencies})

def print_sufficiencies(request, pk):
    sufficiency = LegalSufficiency.objects.get(id=pk)
    return render(request, 'print.html', {'sufficiency':sufficiency})

@login_required
def new_legal_sufficiency(request):
    form = LegalSufficiencyForm()
    if request.method == "POST":
        form = LegalSufficiencyForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.attorney = request.user
            document.save()
            return redirect('home')
        return render(request,'app/new_legal_sufficiency.html', {'form':form, 'errors':form.errors})
    return render(request,'app/new_legal_sufficiency.html', {'form':form})

class LegalSufficiencyUpdate(UpdateView):
    model = LegalSufficiency
    form_class = LegalSufficiencyForm
    success_url = '/'

    def form_valid(self, form):
        self.document = form.save(commit=False)
        if self.request.POST.get('status') == 'published' and self.request.user.has_perm('app.legal_sufficiency_can_publish'):
            self.document.publish()
        else:
            self.document.status = 'review'
        self.document.save()
        return super(LegalSufficiencyUpdate, self).form_valid(form)

@login_required
class LegalSufficiencyDelete(DeleteView):
    model = LegalSufficiency
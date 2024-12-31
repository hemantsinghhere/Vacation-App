from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import DreamVacation, Category, Comment
from django.db import models  
from django.contrib.auth.forms import UserCreationForm

@login_required
def home(request):
    categories = Category.objects.all()
    # Get top vacation based on interactions
    top_vacation = DreamVacation.objects.annotate(
        interaction_count=models.Count('comments') + 
        models.Sum('comments__upvotes')
    ).order_by('-interaction_count').first()
    
    return render(request, 'home.html', {
        'categories': categories,
        'top_vacation': top_vacation
    })

@login_required
def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    vacations = DreamVacation.objects.filter(category=category)\
        .annotate(
            interaction_count=models.Count('comments') + 
            models.Sum('comments__upvotes')
        ).order_by('-interaction_count')
    
    return render(request, 'category.html', {
        'category': category,
        'vacations': vacations
    })

@login_required
def create_vacation(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_name = request.POST.get('category')
        image = request.FILES.get('image')
        
        # Get or create the category
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={'slug': category_name.lower().replace(' ', '-')}
        )
        
        vacation = DreamVacation.objects.create(
            title=title,
            description=description,
            category=category,
            image=image,
            user=request.user
        )
        return redirect('vacation_detail', pk=vacation.pk)  # Make sure to use pk here
    
    return render(request, 'create_vacation.html')

@login_required
def add_comment(request, vacation_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        vacation = get_object_or_404(DreamVacation, pk=vacation_id)
        content = request.POST.get('content')
        
        comment = Comment.objects.create(
            vacation=vacation,
            user=request.user,
            content=content
        )
        
        return JsonResponse({
            'id': comment.id,
            'content': comment.content,
            'user': comment.user.username,
            'upvotes': comment.upvotes,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def upvote_comment(request, comment_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.upvotes += 1
        comment.save()
        
        return JsonResponse({
            'upvotes': comment.upvotes
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def search_vacations(request):
    query = request.GET.get('q', '')
    if query:
        vacations = DreamVacation.objects.filter(title__icontains=query)
        results = [{
            'id': v.id,
            'title': v.title,
            'description': v.description,
            'image_url': v.image.url if v.image else '',
            'category': v.category.name
        } for v in vacations]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def vacation_detail(request, pk):
    vacation = get_object_or_404(DreamVacation, pk=pk)
    return render(request, 'vacation_detail.html', {
        'vacation': vacation
    })
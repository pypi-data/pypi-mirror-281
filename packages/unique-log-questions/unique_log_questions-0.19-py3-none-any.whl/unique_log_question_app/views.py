from django.shortcuts import render,redirect,get_object_or_404
from app1.models import ChatSession,SimilarQuestion


from django.shortcuts import render,redirect,get_object_or_404

from .forms import ChatSessionForm, SimilarQuestionForm

from .decorators import api_key_required 
from django.http import HttpResponse



@api_key_required
def display_unique_questions(request):
    chat_sessions = ChatSession.objects.all()
    
    context = {
        'chat_sessions': chat_sessions
    }
    return render(request, 'unique_questions.html', context)


def display_log_questions(request):
    
    similar_questions = SimilarQuestion.objects.all()

    context = {
        
        'similar_questions': similar_questions
    }
    return render(request, 'log_questions.html', context)


@api_key_required
def delete_chat_session(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id)
    if request.method == 'POST':
        session.delete()
        return redirect('display_unique_questions')
    return HttpResponse(status=405)

@api_key_required
def delete_log_question(request, question_id):
    question = get_object_or_404(SimilarQuestion, id=question_id)
    if request.method == 'POST':
        question.delete()
        return redirect('display_log_answers')
    return HttpResponse(status=405)


@api_key_required
def edit_chat_session(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id)
    if request.method == 'POST':
        form = ChatSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('display_unique_questions')
    else:
        form = ChatSessionForm(instance=session)
    return render(request, 'edit_chat_sessions.html', {'form': form})

@api_key_required
def edit_similar_question(request, question_id):
    question = get_object_or_404(SimilarQuestion, id=question_id)
    if request.method == 'POST':
        form = SimilarQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('display_log_questions')
    else:
        form = SimilarQuestionForm(instance=question)
    return render(request, 'edit_similar_questions.html', {'form': form})



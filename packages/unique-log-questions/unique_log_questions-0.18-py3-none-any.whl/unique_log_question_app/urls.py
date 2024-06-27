from django.urls import path
from unique_log_question_app.views import display_unique_questions, display_log_questions,delete_log_question,delete_chat_session,edit_chat_session,edit_similar_question

urlpatterns = [
    path('unique_questions/', display_unique_questions, name='display_unique_questions'),
    path('log_questions/', display_log_questions, name='display_log_questions'),
    path('delete_unique/<int:session_id>/', delete_chat_session, name='delete_chat_session'),
    path('delete_log/<int:question_id>/', delete_log_question, name='qna_delete_log'),
    path('log_questions/', display_log_questions, name='display_log_answers'),
    path('edit_chat_session/<int:session_id>/', edit_chat_session, name='edit_chat_session'),
    path('edit_similar_question/<int:question_id>/', edit_similar_question, name='edit_similar_question'),
]
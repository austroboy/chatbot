from django.contrib import admin
from .models import KnowledgeBase, Conversation, Message

@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('question', 'language', 'category', 'created_at')
    search_fields = ('question', 'answer')
    list_filter = ('language', 'category')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'started_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'is_user', 'timestamp', 'language_detected')
    list_filter = ('is_user', 'language_detected')
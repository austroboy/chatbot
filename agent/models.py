from django.db import models
from django.contrib.auth.models import User

class KnowledgeBase(models.Model):
    """
    Stores all Q/A pairs or document chunks.
    """
    question = models.TextField(help_text="Typical question or search text")
    answer = models.TextField(help_text="Corresponding answer")
    language = models.CharField(max_length=10, choices=[
        ('bn', 'Bangla'),
        ('en', 'English'),
        ('banglish', 'Banglish'),
    ], default='en')
    category = models.CharField(max_length=100, blank=True, help_text="e.g., Sales, Support, Pricing")
    embedding = models.JSONField(null=True, blank=True, help_text="Precomputed embedding vector (list of floats)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question[:50]

class Conversation(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_id = models.CharField(max_length=100, db_index=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    is_user = models.BooleanField(default=True)  # True if from user, False if bot
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    language_detected = models.CharField(max_length=10, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    feedback = models.BooleanField(null=True, blank=True)  # True = thumbs up, False = thumbs down

    class Meta:
        ordering = ['timestamp']
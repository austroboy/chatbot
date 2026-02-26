import os
from django.core.management.base import BaseCommand
from agent.models import KnowledgeBase
from agent.nlp_utils import get_embedding

class Command(BaseCommand):
    help = 'Generate embeddings for all KnowledgeBase entries'

    def handle(self, *args, **options):
        entries = KnowledgeBase.objects.all()
        for entry in entries:
            if not entry.embedding:   # skip if already computed
                self.stdout.write(f'Processing: {entry.question[:50]}...')
                emb = get_embedding(entry.question)   # use question as search key; can also combine with answer
                entry.embedding = emb.tolist()
                entry.save()
        self.stdout.write(self.style.SUCCESS('Successfully indexed all entries'))
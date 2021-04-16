from django.db import models
from django.db.models import Count

class ThreadManager(models.Manager):
    def get_or_create_personal_thread(self, user1, user2):
        threads = self.get_queryset().filter(thread_type='personal')
        threads = threads.filter(users__in=[user1.id, user2.id]).distinct()
        threads = threads.annotate(u_count=Count('users')).filter(u_count=2)

        if threads.exists():
            return threads.first()
        else:
            thread = self.create(thread_type='personal')
            thread.users.add(user1.id)
            thread.users.add(user2.id)
            return thread
    
    def by_user(self, user):
        return self.get_queryset().filter(users__in=[user])

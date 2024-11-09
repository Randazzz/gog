import uuid
from datetime import timedelta

from celery import Celery, shared_task
from django.utils.timezone import now

from apps.users.models import EmailVerification, User


@shared_task
def send_email_verification(user_id):
    user = User.objects.get(id=user_id)
    expires_at = now() + timedelta(days=2)
    record = EmailVerification.objects.create(user=user, code=uuid.uuid4(), expires_at=expires_at)
    record.send_verification_email()

from app.core.celery_app import celery

@celery.task
def send_notification(user_id: int, title: str, body: str):
    # Placeholder: integrate email/push providers
    print(f"Send notification to {user_id}: {title} - {body}")

from blog.models import Article
from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template import Context, Template


logger = get_task_logger(__name__)
REPORT_TEMPLATE = """ 
                        Here's how you did till now: 
                        {% for post in posts %} 
                        "{{ post.title }}": viewed {{ post.views }} times | 
                        {% endfor %} 
                    """


@shared_task
def send_view_count_report():
    for user in User.objects.all():
        template = Template(REPORT_TEMPLATE)
        user_articles = Article.published.filter(author=user)
        send_mail(
            "Your Django_celery Project Activity",
            template.render(context=Context({"articles": user_articles})),
            "admin@localhost.ru",
            [user.email],
            fail_silently=False,
        )
        logger.info("Send view count report to admin email.")


@shared_task(
    bind=True,
    name="set_article_published_status",
    max_retries=3,
    default_retry_delay=10,
)
def publish_article_scheduled(self, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        article.status = Article.ArticleStatus.PUBLISHED
        article.save()
        logger.info("Article status successfully set to published.")
        return "Article status set to published."
    except Article.DoesNotExist as article_does_not_exist_exc:
        logger.info("Article not found. Retry after 1 min.")
        raise self.retry(exc=article_does_not_exist_exc)


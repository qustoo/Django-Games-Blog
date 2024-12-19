from blog.models import Rating
from django.http import HttpResponseForbidden, JsonResponse
from django.views.generic import View


class RatingCreateView(View):
    model = Rating

    def post(self, request, *args, **kwargs):
        article_id = request.POST.get("article_id")
        value = int(request.POST.get("value"))
        x_forwarded = self.request.META.get("HTTP_X_FORWARDED_FOR")
        ip_address = (
            x_forwarded.split(",")[0]
            if x_forwarded
            else self.request.META.get("REMOTE_ADDR")
        )
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You aren't authenticated")
        user = request.user
        rating_instance, created_status = Rating.objects.get_or_create(
            article_id=article_id,
            ip_address=ip_address,
            defaults={"value": value, "user": user},
        )
        # if found rating instance
        if not created_status:
            # same value 1 == 1
            if rating_instance.value == value:
                return JsonResponse(
                    data={
                        "status": "deleted",
                        "rating_sum": rating_instance.article.get_sum_rating(),
                    }
                )
            else:
                rating_instance.value = value
                rating_instance.user = user
                rating_instance.save()
                return JsonResponse(
                    data={
                        "status": "updated",
                        "rating_sum": rating_instance.article.get_sum_rating(),
                    }
                )
        # rating is created instance
        return JsonResponse(
            {
                "status": "created",
                "rating_sum": rating_instance.article.get_sum_rating(),
            }
        )

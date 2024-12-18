from chat.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

# Create your views here.


class HomeChatListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "chat/home_chat_list.html"
    context_object_name = "groups"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user  #
        return context


@login_required
def group_chat_view(request, uuid):
    """Представление для группы, где все сообщения и события отправляются на интерфейс"""

    group = get_object_or_404(Group, uuid=uuid)
    if request.user not in group.members.all():
        return HttpResponseForbidden(
            "You are not a member of this group.\
                                       Kindly use the join button"
        )

    messages = group.group_messages.all()
    events = group.group_events.all()
    """ События - это сообщения, которые указывают
    Что пользователь присоединился к группе или покинул ее.
    Они будут отправлены автоматически, когда пользователь присоединится к группе или покинет ее.
    """

    # Сортируем по метке времени так, чтобы они были перечислены по порядку
    message_and_event_list = [*messages, *events]
    sorted_message_event_list = sorted(
        message_and_event_list, key=lambda x: x.created_at
    )

    group_members = group.members.all()

    context = {
        "message_and_event_list": sorted_message_event_list,
        "group_members": group_members,
    }

    return render(request, template_name="chat/group_chat.html", context=context)

import pytest
from rest_framework import status

from chats.models import Chat
from users.tests.fixtures import authorized_user, second_user


@pytest.mark.django_db
def test_create_chat(authorized_user, second_user):
    client = authorized_user['client']
    user = authorized_user['user']

    data_for_chat_start = {"user": {"login": user.login},
                           "companion": {"login": second_user.login},
                           "message_set": []}
    create_chat_response = client.post('/chats/start/', data_for_chat_start, format="json")

    assert create_chat_response.status_code == status.HTTP_201_CREATED
    created_chat = Chat.objects.get(pk=1)

    get_chat_response = client.get(f'/chats/{created_chat.id}/')

    assert get_chat_response.status_code == status.HTTP_200_OK

    get_all_chats_response = client.get('/chats/')

    assert len(get_all_chats_response.data) == 1




from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from model_bakery import baker

class TestCreateAuthToken:

    def test_pre_save(self, mocker):
        User = get_user_model()
        instance = baker.prepare(User)

        mock = mocker.patch(
            'bonds.signals.Token.objects.create'
        )

        post_save.send(User, instance=instance, created=True)

        mock.assert_called_with(user=instance)

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secret"
        )
        cls.post = Post.objects.create(
            title="Título",
            body="Contenido",
            author=cls.user,
        )

    def test_post_model(self):
        self.assertEqual(self.post.body, "Contenido")
        self.assertEqual(self.post.title, "Título")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)

    def test_post_listview(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contenido")
        self.assertTemplateUsed(response, "home.html")

    def test_post_detailview(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        no_response = self.client.get("/post/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Título")
        self.assertTemplateUsed(response, "post_detail.html")

    def test_post_createview(self):
        response = self.client.post(
            reverse("post_new"),
            {
                "title": "Nuevo título",
                "body": "Cuerpo",
                "author": self.user.id,
            },
        )
        self.assertEqual(Post.objects.last().title, "Nuevo título")
        self.assertEqual(Post.objects.last().body, "Cuerpo")
        self.assertEqual(response.status_code, 302)

    def test_post_updateview(self):
        response = self.client.post(
            reverse("post_edit", args="1"), {"title": "Título actualizado",
            "body": "Contenido actualizado",}
        )
        self.assertEqual(Post.objects.last().title, "Título actualizado")
        self.assertEqual(Post.objects.last().body, "Contenido actualizado")
        self.assertEqual(response.status_code, 302)

    def test_post_deleteview(self):
        response = self.client.post(reverse("post_delete", args="1"))
        self.assertEqual(response.status_code, 302)

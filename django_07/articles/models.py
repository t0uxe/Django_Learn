from django.db import models
from django.conf import settings
from django.urls import reverse


class Article(models.Model):
    titulo = models.CharField(max_length=255)
    cuerpo = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    articulo = models.ForeignKey(Article, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=140)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.comentario

    def get_absolute_url(self):
        return reverse("article_list")

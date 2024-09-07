from django.db import models


class Idea(models.Model):
    user = models.ForeignKey(
        "user.User", verbose_name="Пользователь", related_name="ideas", on_delete=models.SET_NULL, null=True
    )

    CATEGORIES = [
        ("errors", "Ошибка в работе"),
        ("correction", "Исправление"),
        ("modernization", "Улучшение"),
        ("new_feature", "Новая возможность"),
    ]

    category = models.CharField(max_length=100, verbose_name="категория", choices=CATEGORIES)

    STATUSES = [
        ("new", "Новое"),
        ("in_pregress", "В работе"),
        ("planned", "Запланировано"),
        ("done", "Реализовано"),
        ("reject", "Отклонено"),
        ("repeat", "Повтор"),
    ]

    status = models.CharField(max_length=100, verbose_name="статус", choices=CATEGORIES, default="new")

    finishe_date = models.DateField(null=True)

    created_at = models.DateField(auto_now_add=True)

    title = models.CharField(max_length=500, verbose_name="Тема")
    description = models.CharField(max_length=5000, verbose_name="Описание")

    class Meta:
        verbose_name = "Предложение"
        verbose_name_plural = "Предложения"

    def __str__(self):
        return f"{str(self.user)} - {self.title}"


class Like(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True)
    idea = models.ForeignKey("user.Idea", related_name="likes", on_delete=models.CASCADE)


def get_upload_to_idea_screen(instance, filename):
    return f"images/{instance.idea_id}/{filename}"


class IdeaScreen(models.Model):
    screen = models.ImageField(upload_to=get_upload_to_idea_screen)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)

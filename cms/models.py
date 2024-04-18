from django.db import models


class Page(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=50)
    url = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ["url"]

    def __str__(self):
        return self.title


class Component(models.Model):
    name = models.CharField(verbose_name="название", max_length=50, null=True)
    page = models.ForeignKey(Page, related_name="components", verbose_name="Страница", on_delete=models.CASCADE)

    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "Компонент"
        verbose_name_plural = "Компоненты"
        ordering = ["my_order"]

    def __str__(self):
        return self.name


class BaseComponent(models.Model):
    template = models.CharField(verbose_name="html шаблон(например base.html)", max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.template


class ExampleComponent(BaseComponent):
    component = models.ForeignKey(Component, related_name="excomponent", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Заголовок", max_length=100)
    body = models.TextField(verbose_name="Основной текст", max_length=1000)
    image1 = models.ImageField(verbose_name="Первое изображение", upload_to="images/")
    image2 = models.ImageField(verbose_name="Второе изображение", upload_to="images/")

    def __str__(self):
        return str(self.component)


class Navbar(BaseComponent):
    component = models.ForeignKey(Component, related_name="navcomponent", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Заголовок", max_length=100)

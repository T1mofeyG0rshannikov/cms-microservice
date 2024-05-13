from ckeditor.fields import RichTextField
from django.db import models

from .common import BaseBlock
from .mixins import ButtonMixin, MainTextMixin, TitleMixin


class ContentBlock(BaseBlock, ButtonMixin, TitleMixin, MainTextMixin):
    image1 = models.ImageField(verbose_name="Первое изображение", upload_to="images/content/", null=True, blank=True)
    image2 = models.ImageField(verbose_name="Второе изображение", upload_to="images/content/", null=True, blank=True)

    class Meta:
        verbose_name = "Контентный блок"
        verbose_name_plural = "Контентные блоки"


class Navbar(BaseBlock):
    register_button_text = models.CharField(verbose_name="Текст кнопки регистрации", max_length=50, null=True)
    register_button_href = models.CharField(verbose_name="Сслыка кнопки регистрации", max_length=50, null=True)

    login_button_text = models.CharField(verbose_name="Текст кнопки входа", max_length=50, null=True)

    class Meta:
        verbose_name = "навбар"
        verbose_name_plural = "навбар`ы"


class Cover(BaseBlock, ButtonMixin, TitleMixin, MainTextMixin):
    image_desctop = models.ImageField(verbose_name="Картинка(десктоп)", upload_to="images/covers/")
    image_mobile = models.ImageField(verbose_name="Картинка(смартфон)", upload_to="images/covers/")
    second_button_text = models.CharField(verbose_name="Текст второй кнопки", max_length=20)
    second_button_ref = models.CharField(verbose_name="Ссылка для второй кнопки", max_length=20)

    class Meta:
        verbose_name = "Обложка"
        verbose_name_plural = "Обложки"


class FeaturesBlock(BaseBlock, ButtonMixin, TitleMixin):
    introductory_text = RichTextField(verbose_name="Вводный текст", max_length=300)

    class Meta:
        verbose_name = "Блок с фичами"
        verbose_name_plural = "Блоки с фичами"


class RegisterBlock(BaseBlock, TitleMixin):
    explanation_text = RichTextField(verbose_name="текст пояснений", max_length=1000, null=True, blank=True)
    warning_text = models.CharField(verbose_name="текст предупреждения", max_length=500)

    class Meta:
        verbose_name = "Блок регистрации"
        verbose_name_plural = "Блоки регистрации"


class SocialMediaBlock(BaseBlock, TitleMixin):
    text = RichTextField(verbose_name="Вводный текст", max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = "Блок подписок на соц сети"
        verbose_name_plural = "Блоки подписок на соц сети"


class QuestionsBlock(BaseBlock):
    class Meta:
        verbose_name = "Блок с вопросами"
        verbose_name_plural = "Блоки с вопросами"

from blocks.models.common import BaseBlock
from blocks.models.mixins import ButtonMixin, MainTextMixin, TitleMixin
from ckeditor.fields import RichTextField
from django.db import models


class ContentBlock(BaseBlock, ButtonMixin, TitleMixin, MainTextMixin):
    image1 = models.ImageField(verbose_name="Первое изображение", upload_to="images/content/", null=True, blank=True)
    image2 = models.ImageField(verbose_name="Второе изображение", upload_to="images/content/", null=True, blank=True)

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"


class Navbar(BaseBlock):
    register_button_text = models.CharField(verbose_name="Текст кнопки регистрации", max_length=50, null=True)
    register_button_href = models.CharField(verbose_name="Сслыка кнопки регистрации", max_length=50, null=True)

    login_button_text = models.CharField(verbose_name="Текст кнопки входа", max_length=50, null=True)

    class Meta:
        verbose_name = "навбар"
        verbose_name_plural = "навбары"


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
        verbose_name = "Особенности"
        verbose_name_plural = "Особенности"


class RegisterBlock(BaseBlock, TitleMixin):
    explanation_text = RichTextField(verbose_name="текст пояснений", max_length=1000, null=True, blank=True)
    warning_text = models.CharField(verbose_name="текст предупреждения", max_length=500)

    class Meta:
        verbose_name = "Регистрации"
        verbose_name_plural = "Регистрация"


class SocialMediaBlock(BaseBlock, TitleMixin):
    text = RichTextField(verbose_name="Вводный текст", max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = "Соцсети"
        verbose_name_plural = "Соцсети"


class QuestionsBlock(BaseBlock):
    class Meta:
        verbose_name = "Вопросы"
        verbose_name_plural = "Вопросы"


class StagesBlock(BaseBlock, TitleMixin, MainTextMixin):
    class Meta:
        verbose_name = "Этапы"
        verbose_name_plural = "Этапы"

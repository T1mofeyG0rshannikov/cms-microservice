from ckeditor.fields import RichTextField
from django.db import models

from .common import BaseBlock
from .mixins import ButtonMixin, TitleMixin


class ContentBlock(BaseBlock, ButtonMixin, TitleMixin):
    body = RichTextField(verbose_name="Основной текст", max_length=1000)
    image1 = models.ImageField(verbose_name="Первое изображение", upload_to="images/")
    image2 = models.ImageField(verbose_name="Второе изображение", upload_to="images/")

    class Meta:
        verbose_name = "Контентный блок"
        verbose_name_plural = "Контентные блоки"


class Navbar(BaseBlock):
    logo = models.ImageField(verbose_name="Лого", upload_to="images/logos/", null=True)
    logo_mobile = models.ImageField(verbose_name="Лого(смартфон)", upload_to="images/logos/", null=True)

    register_button_text = models.CharField(verbose_name="Текст кнопки регистрации", max_length=50, null=True)
    register_button_href = models.CharField(verbose_name="Сслыка кнопки регистрации", max_length=50, null=True)

    login_button_text = models.CharField(verbose_name="Текст кнопки входа", max_length=50, null=True)

    class Meta:
        verbose_name = "навбар"
        verbose_name_plural = "навбар`ы"


class Cover(BaseBlock, ButtonMixin, TitleMixin):
    text = RichTextField(verbose_name="Основной текст", max_length=500)
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

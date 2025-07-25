# Generated by Django 5.0 on 2025-07-19 08:55

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AdditionalCatalogBlock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="Имя")),
                ("ancor", models.CharField(blank=True, max_length=50, null=True, verbose_name="Якорь")),
                ("button_text", models.CharField(blank=True, max_length=20, null=True, verbose_name="Текст кнопки")),
                ("add_annotation", models.BooleanField(default=True, verbose_name="добавлять аннотацию к карточке")),
                ("add_button", models.BooleanField(default=True, verbose_name="добавлять кнопку к карточке")),
            ],
            options={
                "verbose_name": "Мини витрина",
                "verbose_name_plural": "Мини витрины",
            },
        ),
        migrations.CreateModel(
            name="Block",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("my_order", models.PositiveIntegerField(default=0)),
                ("block_id", models.PositiveIntegerField(null=True)),
            ],
            options={
                "verbose_name": "Блок",
                "verbose_name_plural": "Блоки",
                "ordering": ["my_order"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CatalogBlock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="Имя")),
                ("ancor", models.CharField(blank=True, max_length=50, null=True, verbose_name="Якорь")),
                ("title", models.CharField(blank=True, max_length=100, null=True, verbose_name="Заголовок")),
                ("button_text", models.CharField(blank=True, max_length=20, null=True, verbose_name="Текст кнопки")),
                (
                    "button_ref",
                    models.CharField(blank=True, max_length=20, null=True, verbose_name="Ссылка для кнопки"),
                ),
                (
                    "introductory_text",
                    ckeditor.fields.RichTextField(max_length=1000, null=True, verbose_name="Введение"),
                ),
                (
                    "add_exclusive",
                    models.BooleanField(
                        help_text="нужно ли добавлять карточку приватного продукта", null=True, verbose_name="Эксклюзив"
                    ),
                ),
                ("add_category", models.BooleanField(null=True, verbose_name="Показывать категорию")),
            ],
            options={
                "verbose_name": "каталог",
                "verbose_name_plural": "каталог",
            },
        ),
        migrations.CreateModel(
            name="CatalogProduct",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("my_order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["my_order"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CatalogProductType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("my_order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["my_order"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ContentBlock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="Имя")),
                ("ancor", models.CharField(blank=True, max_length=50, null=True, verbose_name="Якорь")),
                ("text", ckeditor.fields.RichTextField(max_length=1000, verbose_name="Основной текст")),
                ("title", models.CharField(blank=True, max_length=100, null=True, verbose_name="Заголовок")),
                ("button_text", models.CharField(blank=True, max_length=20, null=True, verbose_name="Текст кнопки")),
                (
                    "button_ref",
                    models.CharField(blank=True, max_length=20, null=True, verbose_name="Ссылка для кнопки"),
                ),
                (
                    "image1",
                    models.ImageField(
                        blank=True, null=True, upload_to="images/content/", verbose_name="Первое изображение"
                    ),
                ),
                (
                    "image2",
                    models.ImageField(
                        blank=True, null=True, upload_to="images/content/", verbose_name="Второе изображение"
                    ),
                ),
            ],
            options={
                "verbose_name": "Контент",
                "verbose_name_plural": "Контент",
            },
        ),
        migrations.CreateModel(
            name="Cover",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="Имя")),
                ("ancor", models.CharField(blank=True, max_length=50, null=True, verbose_name="Якорь")),
                ("text", ckeditor.fields.RichTextField(max_length=1000, verbose_name="Основной текст")),
                ("title", models.CharField(blank=True, max_length=100, null=True, verbose_name="Заголовок")),
                ("button_text", models.CharField(blank=True, max_length=20, null=True, verbose_name="Текст кнопки")),
                (
                    "button_ref",
                    models.CharField(blank=True, max_length=20, null=True, verbose_name="Ссылка для кнопки"),
                ),
                ("image_desctop", models.ImageField(upload_to="images/covers/", verbose_name="Картинка(десктоп)")),
                ("image_mobile", models.ImageField(upload_to="images/covers/", verbose_name="Картинка(смартфон)")),
                ("second_button_text", models.CharField(max_length=20, verbose_name="Текст второй кнопки")),
                ("second_button_ref", models.CharField(max_length=20, verbose_name="Ссылка для второй кнопки")),
            ],
            options={
                "verbose_name": "Обложка",
                "verbose_name_plural": "Обложки",
            },
        ),
        migrations.CreateModel(
            name="Feature",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(blank=True, max_length=100, null=True, verbose_name="Заголовок")),
                ("icon", models.ImageField(upload_to="images/features", verbose_name="Иконка")),
                ("description", models.TextField(verbose_name="Пояснение")),
                ("ref", models.CharField(blank=True, max_length=500, null=True, verbose_name="ссылка")),
            ],
        ),
        migrations.CreateModel(
            name="FeaturesBlock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="Имя")),
                ("ancor", models.CharField(blank=True, max_length=50, null=True, verbose_name="Якорь")),
                ("title", models.CharField(blank=True, max_length=100, null=True, verbose_name="Заголовок")),
                ("button_text", models.CharField(blank=True, max_length=20, null=True, verbose_name="Текст кнопки")),
                (
                    "button_ref",
                    models.CharField(blank=True, max_length=20, null=True, verbose_name="Ссылка для кнопки"),
                ),
                (
                    "introductory_text",
                    ckeditor.fields.RichTextField(blank=True, max_length=300, null=True, verbose_name="Вводный текст"),
                ),
            ],
            options={
                "verbose_name": "Особенности",
                "verbose_name_plural": "Особенности",
            },
        ),
        migrations.CreateModel(
            name="Footer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="Имя")),
                ("ancor", models.CharField(blank=True, max_length=50, null=True, verbose_name="Якорь")),
                ("text1", ckeditor.fields.RichTextField(max_length=1000)),
                ("text2", ckeditor.fields.RichTextField(max_length=1000)),
                ("text3", ckeditor.fields.RichTextField(max_length=1000)),
            ],
            options={
                "verbose_name": "Футер",
                "verbose_name_plural": "Футер",
            },
        ),
        migrations.CreateModel(
            name="FooterMenuItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("button_text", models.CharField(blank=True, max_length=20, null=True, verbose_name="Текст кнопки")),
                (
                    "button_ref",
                    models.CharField(blank=True, max_length=20, null=True, verbose_name="Ссылка для кнопки"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Landing",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=50, verbose_name="Заголовок")),
                ("url", models.CharField(blank=True, max_length=50, null=True)),
                ("logo", models.ImageField(blank=True, null=True, upload_to="images/logo", verbose_name="Лого")),
                ("name", models.CharField(max_length=50, verbose_name="Название")),
            ],
        ),
        migrations.CreateModel(
            name="LandingBlock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("my_order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name": "Блок",
                "verbose_name_plural": "Блоки",
                "ordering": ["my_order"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MainPageCatalogBlock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="Имя")),
                ("ancor", models.CharField(blank=True, max_length=50, null=True, verbose_name="Якорь")),
                ("title", models.CharField(blank=True, max_length=100, null=True, verbose_name="Заголовок")),
                (
                    "introductory_text",
                    ckeditor.fields.RichTextField(max_length=1000, null=True, verbose_name="Введение"),
                ),
                ("button_text", models.CharField(blank=True, max_length=20, null=True, verbose_name="Текст кнопки")),
            ],
            options={
                "verbose_name": "Витрина",
                "verbose_name_plural": "Витрина",
            },
        ),
        migrations.CreateModel(
            name="Navbar",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="Имя")),
                ("ancor", models.CharField(blank=True, max_length=50, null=True, verbose_name="Якорь")),
                (
                    "register_button_text",
                    models.CharField(max_length=50, null=True, verbose_name="Текст кнопки регистрации"),
                ),
                (
                    "register_button_href",
                    models.CharField(max_length=50, null=True, verbose_name="Сслыка кнопки регистрации"),
                ),
                ("login_button_text", models.CharField(max_length=50, null=True, verbose_name="Текст кнопки входа")),
            ],
            options={
                "verbose_name": "навбар",
                "verbose_name_plural": "навбары",
            },
        ),
        migrations.CreateModel(
            name="NavMenuItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("button_text", models.CharField(blank=True, max_length=20, null=True, verbose_name="Текст кнопки")),
                (
                    "button_ref",
                    models.CharField(blank=True, max_length=20, null=True, verbose_name="Ссылка для кнопки"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Page",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=50, verbose_name="Заголовок")),
                ("url", models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                "verbose_name": "Страница",
                "verbose_name_plural": "Страницы",
                "ordering": ["url"],
            },
        ),
        migrations.CreateModel(
            name="PromoCatalog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="Имя")),
                ("ancor", models.CharField(blank=True, max_length=50, null=True, verbose_name="Якорь")),
                ("title", models.CharField(blank=True, max_length=100, null=True, verbose_name="Заголовок")),
            ],
            options={
                "verbose_name": "Промо",
                "verbose_name_plural": "Промо",
            },
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(blank=True, max_length=100, null=True, verbose_name="Заголовок")),
                ("text", ckeditor.fields.RichTextField(max_length=1500, verbose_name="текст вопроса")),
            ],
            options={
                "verbose_name": "Вопрос",
                "verbose_name_plural": "Вопросы",
            },
        ),
        migrations.CreateModel(
            name="QuestionsBlock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="Имя")),
                ("ancor", models.CharField(blank=True, max_length=50, null=True, verbose_name="Якорь")),
            ],
            options={
                "verbose_name": "Вопросы",
                "verbose_name_plural": "Вопросы",
            },
        ),
        migrations.CreateModel(
            name="RegisterBlock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="Имя")),
                ("ancor", models.CharField(blank=True, max_length=50, null=True, verbose_name="Якорь")),
                ("title", models.CharField(blank=True, max_length=100, null=True, verbose_name="Заголовок")),
                (
                    "explanation_text",
                    ckeditor.fields.RichTextField(
                        blank=True, max_length=1000, null=True, verbose_name="текст пояснений"
                    ),
                ),
                ("warning_text", models.CharField(max_length=500, verbose_name="текст предупреждения")),
            ],
            options={
                "verbose_name": "Регистрации",
                "verbose_name_plural": "Регистрация",
            },
        ),
        migrations.CreateModel(
            name="SocialMediaBlock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="Имя")),
                ("ancor", models.CharField(blank=True, max_length=50, null=True, verbose_name="Якорь")),
                ("title", models.CharField(blank=True, max_length=100, null=True, verbose_name="Заголовок")),
                (
                    "text",
                    ckeditor.fields.RichTextField(blank=True, max_length=1000, null=True, verbose_name="Вводный текст"),
                ),
            ],
            options={
                "verbose_name": "Соцсети",
                "verbose_name_plural": "Соцсети",
            },
        ),
        migrations.CreateModel(
            name="SocialMediaButton",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ref", models.CharField(max_length=500, verbose_name="Ссылка на соц. сети")),
            ],
            options={
                "verbose_name": "Социальная сеть",
                "verbose_name_plural": "Социальные сети",
            },
        ),
        migrations.CreateModel(
            name="Stage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(blank=True, max_length=100, null=True, verbose_name="Заголовок")),
                ("text", ckeditor.fields.RichTextField(max_length=1500, verbose_name="текст этапа")),
                ("period", models.CharField(max_length=200, verbose_name="срок этапа")),
                ("num", models.PositiveIntegerField(verbose_name="порядок")),
            ],
            options={
                "verbose_name": "Этап",
                "verbose_name_plural": "Этапы",
            },
        ),
        migrations.CreateModel(
            name="StagesBlock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="Имя")),
                ("ancor", models.CharField(blank=True, max_length=50, null=True, verbose_name="Якорь")),
                ("text", ckeditor.fields.RichTextField(max_length=1000, verbose_name="Основной текст")),
                ("title", models.CharField(blank=True, max_length=100, null=True, verbose_name="Заголовок")),
            ],
            options={
                "verbose_name": "Этапы",
                "verbose_name_plural": "Этапы",
            },
        ),
        migrations.CreateModel(
            name="Template",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, verbose_name="Название шаблона")),
                ("file", models.CharField(max_length=50, verbose_name="Название файла (например base.html)")),
            ],
            options={
                "verbose_name": "шаблон",
                "verbose_name_plural": "шаблоны",
            },
        ),
        migrations.CreateModel(
            name="AdditionalCatalogProductType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("my_order", models.PositiveIntegerField(default=0)),
                (
                    "block",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="blocks.additionalcatalogblock"),
                ),
            ],
            options={
                "ordering": ["my_order"],
                "abstract": False,
            },
        ),
    ]

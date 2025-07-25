# Generated by Django 5.0 on 2025-07-19 08:55

import ckeditor.fields
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("blocks", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="CatalogPageTemplate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=50, verbose_name="Заголовок")),
            ],
            options={
                "verbose_name": "каталог",
                "verbose_name_plural": "каталог",
            },
        ),
        migrations.CreateModel(
            name="ExclusiveCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("button_text", models.CharField(blank=True, max_length=20, null=True, verbose_name="Текст кнопки")),
                (
                    "button_ref",
                    models.CharField(blank=True, max_length=20, null=True, verbose_name="Ссылка для кнопки"),
                ),
                ("image", models.ImageField(upload_to="images/exclusive", verbose_name="картинка")),
                ("bonus", models.CharField(max_length=50, verbose_name="бонус")),
                ("annotation", models.TextField(max_length=700, null=True, verbose_name="аннотация")),
            ],
            options={
                "verbose_name": "Карточка Эксклюзив",
                "verbose_name_plural": "Карточка Эксклюзив",
            },
        ),
        migrations.CreateModel(
            name="Offer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, null=True, verbose_name="Название")),
                ("annotation", models.TextField(max_length=300, verbose_name="Аннотация")),
                ("description", ckeditor.fields.RichTextField(max_length=5000, verbose_name="Описание")),
                (
                    "banner",
                    models.ImageField(blank=True, null=True, upload_to="products/banners/", verbose_name="Баннер"),
                ),
                ("promote", models.DateField(blank=True, null=True, verbose_name="Продвигать до")),
                ("promotion", models.BooleanField(verbose_name="Акция")),
                ("start_promotion", models.DateField(blank=True, null=True, verbose_name="Начало акции")),
                ("end_promotion", models.DateField(blank=True, null=True, verbose_name="Окончание акции")),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("Черновик", "Черновик"), ("Архив", "Архив"), ("Опубликовано", "Опубликовано")],
                        default="Новое",
                        max_length=50,
                        verbose_name="статус",
                    ),
                ),
                (
                    "terms_of_the_promotion",
                    models.URLField(blank=True, max_length=1000, null=True, verbose_name="условия акции"),
                ),
                (
                    "partner_program",
                    models.CharField(
                        choices=[
                            ("Приведи друга", "Приведи друга"),
                            ("CPA сеть", "CPA сеть"),
                            ("Друзья/CPA", "Друзья/CPA"),
                            ("Только админ", "Только админ"),
                            ("Нет", "Нет"),
                        ],
                        max_length=100,
                        null=True,
                        verbose_name="Партнерская программа",
                    ),
                ),
                (
                    "verification_of_registration",
                    models.BooleanField(default=False, verbose_name="Верификация оформления"),
                ),
            ],
            options={
                "verbose_name": "оффер",
                "verbose_name_plural": "офферы",
                "db_table": "offers_offer",
                "ordering": ["end_promotion"],
            },
        ),
        migrations.CreateModel(
            name="OrganizationType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Тип организации",
                "verbose_name_plural": "Типы организаций",
                "db_table": "catalog_organizationtype",
            },
        ),
        migrations.CreateModel(
            name="ProductCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Категория")),
                ("short", models.CharField(max_length=100, null=True, verbose_name="Сокращение")),
            ],
            options={
                "verbose_name": "Категория продуктов",
                "verbose_name_plural": "Категории продуктов",
            },
        ),
        migrations.CreateModel(
            name="Block",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("my_order", models.PositiveIntegerField(default=0)),
                ("block_id", models.PositiveIntegerField(null=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="catalog_content_type",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blocks",
                        to="catalog.catalogpagetemplate",
                        verbose_name="Страница",
                    ),
                ),
            ],
            options={
                "verbose_name": "Блок",
                "verbose_name_plural": "Блоки",
                "ordering": ["my_order"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Link",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.URLField(max_length=300, verbose_name="ссылка")),
                (
                    "percent",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="процент",
                    ),
                ),
                ("info", models.CharField(blank=True, max_length=300, null=True, verbose_name="Инфо")),
                (
                    "offer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="links", to="catalog.offer"
                    ),
                ),
            ],
            options={
                "verbose_name": "ссылки",
                "db_table": "offers_link",
            },
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
                ("logo", models.ImageField(upload_to="organizations/logos/", verbose_name="Лого")),
                ("site", models.URLField(max_length=500, verbose_name="сайт")),
                (
                    "admin_hint",
                    ckeditor.fields.RichTextField(blank=True, max_length=1500, null=True, verbose_name="пояснение"),
                ),
                (
                    "partner_program",
                    models.CharField(blank=True, max_length=100, null=True, verbose_name="Партнерская программа"),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="catalog.organizationtype", verbose_name="Тип"
                    ),
                ),
            ],
            options={
                "verbose_name": "Организация",
                "verbose_name_plural": "Организации",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("cover", models.ImageField(upload_to="products/covers", verbose_name="Обложка")),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
                (
                    "status",
                    models.CharField(
                        choices=[("Черновик", "Черновик"), ("Архив", "Архив"), ("Опубликовано", "Опубликовано")],
                        default="Новое",
                        max_length=50,
                        verbose_name="статус",
                    ),
                ),
                (
                    "private",
                    models.BooleanField(verbose_name="Приватный(виден только зарегистрированным пользователям)"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "partner_annotation",
                    models.TextField(blank=True, max_length=1000, null=True, verbose_name="Партнерская аннотация"),
                ),
                (
                    "partner_bonus",
                    models.CharField(blank=True, max_length=1000, null=True, verbose_name="Партнерский бонус"),
                ),
                (
                    "partner_description",
                    ckeditor.fields.RichTextField(
                        blank=True, max_length=5000, null=True, verbose_name="Партнерское описание"
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="catalog.organization",
                        verbose_name="организация",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="catalog.productcategory",
                        verbose_name="категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "продукт/акция",
                "verbose_name_plural": "продукты/акции",
            },
        ),
        migrations.AddField(
            model_name="offer",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="offers",
                to="catalog.product",
                verbose_name="Продукт",
            ),
        ),
        migrations.CreateModel(
            name="ProductType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[("Опубликовано", "Опубликовано"), ("Скрыто", "Скрыто")],
                        max_length=100,
                        null=True,
                        verbose_name="статус",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="Название")),
                ("slug", models.SlugField(blank=True, max_length=200, null=True, unique=True, verbose_name="URL")),
                ("title", models.CharField(max_length=100, verbose_name="Заголовок")),
                ("image", models.ImageField(null=True, upload_to="organizations/covers", verbose_name="Этикетка")),
                ("description", ckeditor.fields.RichTextField(max_length=1000, verbose_name="Аннотация")),
                ("profit", models.CharField(max_length=500, null=True, verbose_name="Выгода")),
                (
                    "cover",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="blocks.cover",
                        verbose_name="блок обложки",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тип продукта/акции",
                "verbose_name_plural": "Типы продукта/акции",
            },
        ),
        migrations.CreateModel(
            name="OfferTypeRelation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("profit", models.CharField(max_length=500, verbose_name="Выгода")),
                (
                    "offer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="types",
                        to="catalog.offer",
                        verbose_name="Тип продукта",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="catalog.producttype",
                        verbose_name="продукт",
                    ),
                ),
            ],
        ),
    ]

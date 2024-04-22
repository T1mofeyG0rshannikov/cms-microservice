from .mixins import TextColorMinin, ThicknessOfTextMixin, SizeOfTextMixin, SizeOfTextMobileMixin, InvertedTextColorMixin, FontMixin, ThicknessOfTextMobileMixin


class HeaderText(FontMixin, SizeOfTextMixin, SizeOfTextMobileMixin, ThicknessOfTextMixin, ThicknessOfTextMobileMixin, TextColorMinin, InvertedTextColorMixin):
    class Meta:
        verbose_name = u"Заголовок"
        verbose_name_plural = u"Заголовок"
        
class SubheaderText(FontMixin, SizeOfTextMixin, SizeOfTextMobileMixin, ThicknessOfTextMixin, ThicknessOfTextMobileMixin, TextColorMinin, InvertedTextColorMixin):
    class Meta:
        verbose_name = u"Подзаголовок"
        verbose_name_plural = u"Подзаголовок"

class MainText(FontMixin, SizeOfTextMixin, SizeOfTextMobileMixin, ThicknessOfTextMixin, ThicknessOfTextMobileMixin, TextColorMinin, InvertedTextColorMixin):
    class Meta:
        verbose_name = u"Основной текст"
        verbose_name_plural = u"Основной текст"
        
class ExplanationText(FontMixin, SizeOfTextMixin, SizeOfTextMobileMixin, ThicknessOfTextMixin, ThicknessOfTextMobileMixin, TextColorMinin, InvertedTextColorMixin):
    class Meta:
        verbose_name = u"Текст пояснний"
        verbose_name_plural = u"Текст пояснний"
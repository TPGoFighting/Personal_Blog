from django import template
import markdown
from django.utils.safestring import mark_safe

# 核心修复：删除 atexit 的导入，确保 register 是 Django 的 Library 对象
register = template.Library()


@register.filter(name="markdown")  # 改为 "markdown"，这样 HTML 里才能用 |markdown
def markdown_to_html(markdown_text):
    if not markdown_text:
        return ""

    html_content = markdown.markdown(
        markdown_text, extensions=["extra", "codehilite", "fenced_code"]
    )
    return mark_safe(html_content)

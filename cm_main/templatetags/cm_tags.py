# based on https://stackoverflow.com/questions/17178525/django-how-to-include-a-view-from-within-a-template#56476932
# this view and tag allows including a view into another view. see template/cm_main/base.html as an example
# TODO: deliver this as a reusable piece of code
import os
from django.template import Library, Node, Variable, TemplateSyntaxError
from django.conf import settings
from django.urls import reverse, resolve, NoReverseMatch

register = Library()


class ViewNode(Node):
    def __init__(self, url_or_view, args, kwargs):
        self.url_or_view = url_or_view
        self.args = args
        self.kwargs = kwargs
        self.init = False

    def _resolve_args(self, context):
        # for an unknown reason, the first time, the args are not resolved
        if self.init:
            resolved_args = self.args
            resolved_kwargs = self.kwargs
        else:
            resolved_args = [] if self.args else None
            for arg in self.args:
                resolved_args.append(Variable(arg).resolve(context))
            resolved_kwargs = {} if self.kwargs else None

            for k, v in self.kwargs.items():
                resolved_kwargs[k] = Variable(v).resolve(context)
            self.init = True
        return resolved_args, resolved_kwargs

    def render(self, context):
        if 'request' not in context:
            raise TemplateSyntaxError("No request has been made.")

        url_or_view = Variable(self.url_or_view).resolve(context)
        resolved_args, resolved_kwargs = self._resolve_args(context)
        try:
            view, args, kwargs = resolve(reverse(url_or_view, args=resolved_args, kwargs=resolved_kwargs))
        except NoReverseMatch:
            view, args, kwargs = resolve(url_or_view)

        try:
            if callable(view):
                self.args += args
                self.kwargs.update(**kwargs)
                return (view(context['request'], *self.args, **self.kwargs)
                        .rendered_content)
            raise "%r is not callable" % view
        except Exception:
            if settings.DEBUG:
                raise
        return None


@register.tag(name='get_view')
def get_view(parser, token):
    args, kwargs, tokens = [], {}, token.split_contents()
    if len(tokens) < 2:
        raise TemplateSyntaxError(
            f"{token.contents.split()[0]} tag requires one or more arguments")

    for t in tokens[2:]:
        kw = t.find("=")
        args.append(t) if kw == -1 else kwargs.update({str(t[:kw]): t[kw+1:]})
    # print(kwargs)

    return ViewNode(tokens[1], args, kwargs)


@register.simple_tag
def title(title_s):
    return f"{settings.SITE_NAME} - {title_s}"


@register.inclusion_tag("cm_main/paginate_template.html")
def paginate(page, no_per_page=False):
    # print("page=", page)
    return {
        "page_urls": page.page_links,
        "page_range": page.page_range,
        "first_page_url": page.first_page_link,
        "last_page_url": page.last_page_link,
        "prev_page_url": page.page_links[page.number-page.first-2] if page.has_previous() else None,
        "next_page_url": page.page_links[page.number-page.first] if page.has_next() else None,
        "current_page": page.number,
        "possible_per_pages": page.possible_per_pages,
        "page_size": page.paginator.per_page,
        "num_pages": page.num_pages,
        "no_per_page": no_per_page
    }


def find_static_file(url):
    # Extract the path of the static file from its URL
    static_path = url.replace(settings.STATIC_URL, '')
    # get application
    application = static_path.split('/')[0]
    # Builds the full path of the file
    full_path = os.path.join(settings.STATIC_ROOT, static_path)
    # check if the file exists
    if os.path.exists(full_path):
        return full_path
    else:  # if not, try to find it in the application static folder
        full_path = os.path.join(settings.BASE_DIR, application, 'static', static_path)
        if os.path.exists(full_path):
            return full_path
        else:
            return None


@register.inclusion_tag("cm_main/inline_css.html")
def inline_css(css_url):
    css_path = find_static_file(css_url)
    if css_path is None:
        raise TemplateSyntaxError(f"The file {css_url} does not exist.")
    with open(css_path, "r") as f:
        css = f.read()
    return {'css': css}

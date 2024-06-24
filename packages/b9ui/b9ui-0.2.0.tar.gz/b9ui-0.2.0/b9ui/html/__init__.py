from ludic.html import (
    Element, 
    aside, 
    br,
    body,
    footer, 
    form,
    h1,
    h2,
    h3, 
    h4,
    h5,
    h6,
    hr,
    head, 
    header,
    img, 
    input,
    link,
    main, 
    option,
    p, 
    pre,
    select,
    script, 
    small,
    time,
    title
)
from ludic.types import AnyChildren, ComplexChildren, ElementStrict
from b9ui.attrs import ButtonAttrs, DivAttrs, HtmlTagAttrs, LiAttrs, UlAttrs

from ..attrs import GlobalAttrs


class html(ElementStrict[head, body, HtmlTagAttrs]):
    html_header = "<!doctype html>"
    html_name = "html"


class button(Element[AnyChildren, ButtonAttrs]):
    html_name = "button"    


class div(Element[AnyChildren, DivAttrs]):
    html_name = "div"


class li(Element[AnyChildren, LiAttrs]):
    html_name = "li"


class nav(Element[AnyChildren, GlobalAttrs]):
    html_name = "nav"    


class span(Element[AnyChildren, GlobalAttrs]):
    html_name = "span"


class ul(Element[ComplexChildren, UlAttrs]):
    html_name = "ul"

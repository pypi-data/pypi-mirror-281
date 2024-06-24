from typing import override
from ludic.attrs import ImgAttrs
from ludic.html import img
from ludic.types import AnyChildren, Component


class Image(Component[AnyChildren, ImgAttrs]):
    @override
    def render(self) -> img:
        return img(
            *self.children,
            **self.attrs
        )
    
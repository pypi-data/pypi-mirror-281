"""Subpackage."""

from typing import TYPE_CHECKING as __tc


if __tc:
    from mastapy._private.utility.logging._1858 import Logger
    from mastapy._private.utility.logging._1859 import Message
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.logging._1858": ["Logger"],
        "_private.utility.logging._1859": ["Message"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Logger",
    "Message",
)

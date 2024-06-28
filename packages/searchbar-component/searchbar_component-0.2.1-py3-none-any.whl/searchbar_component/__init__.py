import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "searchbar_component",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("searchbar_component", path=build_dir)

def searchbar(placeholder="Search...", key=None, suggestions=None, return_selection_only=True, show_clear_button=True, show_plus_button=True, style_overrides=None):
    component_value = _component_func(
        placeholder=placeholder,
        suggestions=suggestions,
        return_selection_only=return_selection_only,
        show_clear_button=show_clear_button,
        show_plus_button=show_plus_button,
        style_overrides=style_overrides,
        key=key,
        default=None
    )
    return component_value

__all__ = ["searchbar"]
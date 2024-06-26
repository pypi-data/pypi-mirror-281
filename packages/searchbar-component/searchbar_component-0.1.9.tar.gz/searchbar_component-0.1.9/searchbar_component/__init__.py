import os
import streamlit as st
import streamlit.components.v1 as components
from typing import Any, Callable, List

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

def _process_search(search_function: Callable[[str], List[Any]], searchterm: str, **kwargs) -> List[Any]:
    return search_function(searchterm, **kwargs)

def searchbar(
    search_function: Callable[[str], List[Any]],
    placeholder: str = "Search ...",
    label: str | None = None,
    default: Any = None,
    default_options: List[Any] | None = None,
    clear_on_submit: bool = False,
    rerun_on_update: bool = True,
    key: str = "searchbar",
    **kwargs
) -> Any:
    if key not in st.session_state:
        st.session_state[key] = {
            "result": default,
            "options": default_options or [],
        }

    component_value = _component_func(
        search_function=lambda x: _process_search(search_function, x, **kwargs),
        placeholder=placeholder,
        label=label,
        default=default,
        options=st.session_state[key]["options"],
        clear_on_submit=clear_on_submit,
        key=key,
    )

    if component_value is not None:
        interaction, value = component_value["interaction"], component_value["value"]

        if interaction == "search":
            st.session_state[key]["options"] = _process_search(search_function, value, **kwargs)
            if rerun_on_update:
                st.experimental_rerun()

        elif interaction == "submit":
            st.session_state[key]["result"] = value
            if clear_on_submit:
                st.session_state[key]["options"] = []

        elif interaction == "reset":
            st.session_state[key]["result"] = default
            st.session_state[key]["options"] = default_options or []

    return st.session_state[key]["result"]

if not _RELEASE:
    import streamlit as st

    def demo_search_function(query: str) -> List[str]:
        return [f"{query} result {i}" for i in range(5)]

    st.title("Searchbar Component Demo")

    result = searchbar(
        search_function=demo_search_function,
        placeholder="Type to search...",
        label="Demo Searchbar",
        default="",
        clear_on_submit=True,
        key="demo_searchbar"
    )

    st.write(f"You selected: {result}")
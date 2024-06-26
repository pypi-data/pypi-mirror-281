import importlib.util
from typing import List, Set

from fix_imports.predefined import predefined_imports


def collection_imports() -> List[str]:
    from collections import __all__

    return __all__


def typing() -> List[str]:
    from typing import __all__

    return __all__


def is_package(name: str) -> str | None:
    package_specs = importlib.util.find_spec(name)

    try:
        importlib.util.module_from_spec(package_specs)  # type: ignore
        return f"import {name}"
    except Exception:
        return None


def import_string(mod_set: Set[str]) -> str:
    typings = set(typing())
    collections = set(collection_imports())
    predefined_keys = set(predefined_imports.keys())

    typings_imports = []
    collections_imports = []
    predefined_imports_list = []
    other_imports = []

    for mod in mod_set:
        if mod in typings:
            typings_imports.append(mod)
        elif mod in collections:
            collections_imports.append(mod)
        elif mod in predefined_keys:
            predefined_imports_list.append(predefined_imports[mod])
        else:
            package_import = is_package(mod)
            if package_import:
                other_imports.append(package_import)

    typings_str = (
        "from typing import " + ", ".join(typings_imports) if typings_imports else ""
    )
    collections_str = (
        "from collections import " + ", ".join(collections_imports)
        if collections_imports
        else ""
    )
    predefined_str = "\n".join(predefined_imports_list)
    other_str = "\n".join(other_imports)

    return "\n".join(
        filter(None, [typings_str, collections_str, predefined_str, other_str])
    )

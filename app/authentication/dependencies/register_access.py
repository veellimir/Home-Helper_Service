from collections.abc import Iterable
from typing import Any

from fastapi import Depends
from fastapi.dependencies.utils import get_parameterless_sub_dependant
from fastapi.routing import APIRoute, iter_route_contexts

from app.authentication.dependencies.authorization import require_role
from app.users.domain.enums import UserRoleEnum


ACCESS_RULES: dict[tuple[str, str], UserRoleEnum] = {
    ("GET", "/api/v1/users/list"): UserRoleEnum.ADMIN,
}


def register_access_rules(
    routes: Iterable[Any],
    access_rules: dict[tuple[str, str], UserRoleEnum],
) -> None:
    registered_rules: set[tuple[str, str]] = set()

    for context in iter_route_contexts(routes):
        route = context.route

        if not isinstance(route, APIRoute):
            continue

        for method in context.methods or set():
            key = (method, context.path)

            if key not in access_rules:
                continue

            required_role = access_rules[key]

            dependant = get_parameterless_sub_dependant(
                depends=Depends(
                    require_role(required_role),
                ),
                path=context.path,
            )

            effective_route = context._effective_route

            effective_route.dependant.dependencies.append(
                dependant,
            )

            registered_rules.add(key)

            print(
                f"ACCESS: {method} {context.path} "
                f"-> {required_role.value}",
                flush=True,
            )

    missing_rules = set(access_rules) - registered_rules

    if missing_rules:
        missing = ", ".join(
            f"{method} {path}"
            for method, path in sorted(missing_rules)
        )

        raise RuntimeError(
            f"Для следующих маршрутов не найден endpoint: {missing}",
        )
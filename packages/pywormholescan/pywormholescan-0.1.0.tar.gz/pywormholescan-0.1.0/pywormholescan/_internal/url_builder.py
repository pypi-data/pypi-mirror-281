__all__ = ["build_url"]


def build_url(path: str, **kwargs) -> str:
    """
    Builds the complete URL for an API endpoint with path and/or query interpolation.

    Args:
        path: The API endpoint path with placeholders for parameters (e.g., /api/v1/governor/limit).
        kwargs: Keyword arguments to be interpolated into the path placeholders.

    Returns:
        The complete URL string.
    """
    query_params = ""
    if "kwargs" in kwargs.keys():
        queries = "?"
        for k, v in kwargs["kwargs"].items():
            k = _convert_to_camel_case(k)
            queries += f"{k}={v}&"
        query_params += queries[:-1]

    url = path + query_params if query_params else path
    return url


def _convert_to_camel_case(query: str) -> str:
    """
    Takes a query in snake_case and converts it to camelCase.

    Args:
        query (str): Query param to convert.
    """
    splitted_query = query.split("_")
    return f"{splitted_query[0]}" + "".join(
        [splitted_query[i].title() for i in range(len(splitted_query)) if i != 0]
    )

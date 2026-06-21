from mcp_server.tools import compare_setlists


def execute(
    show_date_a: str,
    show_date_b: str
):

    result = compare_setlists(
        show_date_a,
        show_date_b
    )

    answer = (
        f"The two shows share "
        f"{len(result['shared_songs'])} songs "
        f"with a similarity score of "
        f"{result['similarity']}."
    )

    result["skill"] = "setlist-similarity"
    result["answer"] = answer

    return result
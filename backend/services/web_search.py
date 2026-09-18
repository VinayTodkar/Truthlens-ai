from ddgs import DDGS


def search_web(
    query: str,
    max_results: int = 8
):

    results = []

    try:

        with DDGS() as ddgs:

            search_results = ddgs.text(
                query,
                max_results=max_results
            )

            for result in search_results:

                results.append(
                    {
                        "title": result.get(
                            "title",
                            ""
                        ),
                        "url": result.get(
                            "href",
                            ""
                        ),
                        "snippet": result.get(
                            "body",
                            ""
                        )
                    }
                )

    except Exception as error:

        print(
            f"Search provider unavailable: {error}"
        )

        return []

    return results
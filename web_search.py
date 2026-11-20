import os

from tavily import TavilyClient

TRUSTED_DOMAINS = {
    "richest": [
        "forbes.com",
        "bloomberg.com"
    ],

    "raspberry pi": [
        "raspberrypi.com",
        "tomshardware.com"
    ],

    "python": [
        "python.org",
        "realpython.com"
    ],

    "cloud": [
        "aws.amazon.com",
        "cloud.google.com",
        "learn.microsoft.com"
    ]
}


def get_preferred_domains(query):

    query = query.lower()

    for keyword, domains in TRUSTED_DOMAINS.items():

        if keyword in query:
            return domains

    return []


def search_web(query):
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return None

    try:

        preferred_domains = get_preferred_domains(
            query
        )

        response = TavilyClient(api_key=api_key).search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=True,
            include_raw_content=False,
            include_domains=preferred_domains
            if preferred_domains else None
        )

        return response

    except Exception as e:

        print(
            "Tavily Search Error:",
            type(e).__name__
        )

        return None

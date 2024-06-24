import asyncio
import json
import logging
import os
from collections import defaultdict
from typing import Callable, Dict, List, Optional, Tuple, Union

import aiohttp
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

from khoj.routers.helpers import (
    extract_relevant_info,
    generate_online_subqueries,
    infer_webpage_urls,
)
from khoj.utils.helpers import is_internet_connected, is_none_or_empty, timer
from khoj.utils.rawconfig import LocationData

logger = logging.getLogger(__name__)

SERPER_DEV_API_KEY = os.getenv("SERPER_DEV_API_KEY")
SERPER_DEV_URL = "https://google.serper.dev/search"

OLOSTEP_API_KEY = os.getenv("OLOSTEP_API_KEY")
OLOSTEP_API_URL = "https://agent.olostep.com/olostep-p2p-incomingAPI"
OLOSTEP_QUERY_PARAMS = {
    "timeout": 35,  # seconds
    "waitBeforeScraping": 1,  # seconds
    "saveHtml": "False",
    "saveMarkdown": "True",
    "removeCSSselectors": "default",
    "htmlTransformer": "none",
    "removeImages": "True",
    "fastLane": "True",
    # Similar to Stripe's API, the expand parameters avoid the need to make a second API call
    # to retrieve the dataset (from the dataset API) if you only need the markdown or html.
    "expandMarkdown": "True",
    "expandHtml": "False",
}
MAX_WEBPAGES_TO_READ = 1


async def search_online(
    query: str,
    conversation_history: dict,
    location: LocationData,
    send_status_func: Optional[Callable] = None,
    custom_filters: List[str] = [],
):
    query += " ".join(custom_filters)
    if not online_search_enabled():
        logger.warn("SERPER_DEV_API_KEY is not set")
        return {}
    if not is_internet_connected():
        logger.warn("Cannot search online as not connected to internet")
        return {}

    # Breakdown the query into subqueries to get the correct answer
    subqueries = await generate_online_subqueries(query, conversation_history, location)
    response_dict = {}

    for subquery in subqueries:
        if send_status_func:
            await send_status_func(f"**🌐 Searching the Internet for**: {subquery}")
        logger.info(f"🌐 Searching the Internet for '{subquery}'")
        response_dict[subquery] = search_with_google(subquery)

    # Gather distinct web pages from organic search results of each subquery without an instant answer
    webpage_links = {
        organic["link"]: subquery
        for subquery in response_dict
        for organic in response_dict[subquery].get("organic", [])[:MAX_WEBPAGES_TO_READ]
        if "answerBox" not in response_dict[subquery]
    }

    # Read, extract relevant info from the retrieved web pages
    if webpage_links:
        logger.info(f"🌐👀 Reading web pages at: {list(webpage_links)}")
        if send_status_func:
            webpage_links_str = "\n- " + "\n- ".join(list(webpage_links))
            await send_status_func(f"**📖 Reading web pages**: {webpage_links_str}")
    tasks = [read_webpage_and_extract_content(subquery, link) for link, subquery in webpage_links.items()]
    results = await asyncio.gather(*tasks)

    # Collect extracted info from the retrieved web pages
    for subquery, webpage_extract, url in results:
        if webpage_extract is not None:
            response_dict[subquery]["webpages"] = {"link": url, "snippet": webpage_extract}

    return response_dict


def search_with_google(subquery: str):
    payload = json.dumps({"q": subquery})
    headers = {"X-API-KEY": SERPER_DEV_API_KEY, "Content-Type": "application/json"}

    response = requests.request("POST", SERPER_DEV_URL, headers=headers, data=payload)

    if response.status_code != 200:
        logger.error(response.text)
        return {}

    json_response = response.json()
    extraction_fields = ["organic", "answerBox", "peopleAlsoAsk", "knowledgeGraph"]
    extracted_search_result = {
        field: json_response[field] for field in extraction_fields if not is_none_or_empty(json_response.get(field))
    }

    return extracted_search_result


async def read_webpages(
    query: str, conversation_history: dict, location: LocationData, send_status_func: Optional[Callable] = None
):
    "Infer web pages to read from the query and extract relevant information from them"
    logger.info(f"Inferring web pages to read")
    if send_status_func:
        await send_status_func(f"**🧐 Inferring web pages to read**")
    urls = await infer_webpage_urls(query, conversation_history, location)

    logger.info(f"Reading web pages at: {urls}")
    if send_status_func:
        webpage_links_str = "\n- " + "\n- ".join(list(urls))
        await send_status_func(f"**📖 Reading web pages**: {webpage_links_str}")
    tasks = [read_webpage_and_extract_content(query, url) for url in urls]
    results = await asyncio.gather(*tasks)

    response: Dict[str, Dict] = defaultdict(dict)
    response[query]["webpages"] = [
        {"query": q, "link": url, "snippet": web_extract} for q, web_extract, url in results if web_extract is not None
    ]
    return response


async def read_webpage_and_extract_content(subquery: str, url: str) -> Tuple[str, Union[None, str], str]:
    try:
        with timer(f"Reading web page at '{url}' took", logger):
            content = await read_webpage_with_olostep(url) if OLOSTEP_API_KEY else await read_webpage_at_url(url)
        with timer(f"Extracting relevant information from web page at '{url}' took", logger):
            extracted_info = await extract_relevant_info(subquery, content)
        return subquery, extracted_info, url
    except Exception as e:
        logger.error(f"Failed to read web page at '{url}' with {e}")
        return subquery, None, url


async def read_webpage_at_url(web_url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(web_url, headers=headers, timeout=30) as response:
            response.raise_for_status()
            html = await response.text()
            parsed_html = BeautifulSoup(html, "html.parser")
            body = parsed_html.body.get_text(separator="\n", strip=True)
            return markdownify(body)


async def read_webpage_with_olostep(web_url: str) -> str:
    headers = {"Authorization": f"Bearer {OLOSTEP_API_KEY}"}
    web_scraping_params: Dict[str, Union[str, int, bool]] = OLOSTEP_QUERY_PARAMS.copy()  # type: ignore
    web_scraping_params["url"] = web_url

    async with aiohttp.ClientSession() as session:
        async with session.get(OLOSTEP_API_URL, params=web_scraping_params, headers=headers) as response:
            response.raise_for_status()
            response_json = await response.json()
            return response_json["markdown_content"]


def online_search_enabled():
    return SERPER_DEV_API_KEY is not None

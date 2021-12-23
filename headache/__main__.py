import os
import logging
from pythonjsonlogger import jsonlogger

from aiohttp import web


def configure_logging():
    logger = logging.getLogger()
    logHandler = logging.StreamHandler()    

    if os.getenv("HEADACHE_LOG_FORMATTER", "text").lower() == "json":
        formatter = jsonlogger.JsonFormatter()
        logHandler.setFormatter(formatter)

    logger.addHandler(logHandler)
    logger.setLevel(logging.DEBUG)



async def print_headers(request: web.BaseRequest) -> web.Response:
    headers = str()
    for k, v in request.headers.items():
        headers += f"{k}: {v}<br>"

    response = (
        "<html><head><title>Headache</title></head><body>"
        f"<p>Request URL: {request.url}<br>"
        f"Request method: {request.method}<br>"
        f"Remote client IP address: {request.remote}</p>"
        "<hr>"
        "<p>Request headers:</p>"
        f"<p>{headers}</p>"
        "</body></html>"
    )

    return web.Response(text=response,
                        content_type="text/html")


def main() -> None:
    configure_logging()
    app = web.Application()
    app.add_routes([web.get("/{tail:.*}", print_headers),
                    web.post("/{tail:.*}", print_headers)])

    web.run_app(app)


if __name__ == "__main__":
    main()

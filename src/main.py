from os import getenv

from dotenv import load_dotenv

from .dropbox import Dropbox
from .rss import Rss

if __name__ == "__main__":
    load_dotenv()

    dbx = Dropbox(token=getenv("DROPBOX_TOKEN", ""))

    rss = Rss(
        title=getenv("RSS_TITLE", ""),
        description=getenv("RSS_DESCRIPTION", ""),
        url=getenv("RSS_URL", ""),
        author=getenv("RSS_AUTHOR", ""),
        email=getenv("RSS_EMAIL", ""),
    )

    files = dbx.list_dir("/feed/dump")

    for file_metadata in files:
        path = file_metadata.path_lower
        metadata = dbx.get_metadata(path)
        date = metadata.client_modified
        if metadata.media_info:
            rss.add_image(
                title=metadata.name,
                description="---",
                date=date,
                url=dbx.generate_url(path),
                length=metadata.size,
                type="image/jpg",
            )
        else:
            rss.add_text(
                title=metadata.name,
                description="---",
                date=date,
                content=dbx.get_content(path),
            )

    rss.generate_xml(getenv("OUTPUT_PATH", ""))

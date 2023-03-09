import requests

from dropbox import Dropbox as _Dbx
from dropbox.files import FileMetadata, ListFolderResult
from dropbox.sharing import PathLinkMetadata


class Dropbox:
    __client: _Dbx

    def __init__(self: "Dropbox", token: str):
        self.__client = _Dbx(oauth2_access_token=token)

    def list_dir(self: "Dropbox", path: str) -> list[FileMetadata]:
        folder: ListFolderResult = self.__client.files_list_folder(path)
        return sorted(
            (
                file_metadata
                for file_metadata in folder.entries or []
                if file_metadata.name
            ),
            key=lambda x: x.client_modified,
        )

    def get_content(self: "Dropbox", path: str) -> str:
        url = self.generate_url(path)
        resp = requests.get(url)
        return resp.text

    def get_metadata(self: "Dropbox", path: str) -> FileMetadata:
        return self.__client.files_get_metadata(
            path,
            include_media_info=True,
        )

    def get_media_info(self: "Dropbox", path: str) -> None:
        return self.__client.file_pr

    def generate_url(
        self: "Dropbox",
        path: str,
    ) -> str:
        link: PathLinkMetadata = (
            self.__client.sharing_create_shared_link_with_settings(path)
        )
        return self.substitute_query_params(link.url)

    def substitute_query_params(self: "Dropbox", url: str) -> str:
        return url.replace("www", "dl").replace("?dl=0", "")

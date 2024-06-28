import pymongo
from beanie import Document
from pydantic import Field

from fa_common import File, get_settings
from fa_common.models import CamelModel, WorkflowProject


class ProjectDB(Document, WorkflowProject):
    dataset_links: list[str] = []
    tags: list[str] = []
    files: list[File] = []
    project_users: list[str] = []

    @staticmethod
    def _api_out_exclude() -> set[str]:
        """
        Fields to exclude from an API output
        """
        return set()

    class Settings:
        name = f"{get_settings().COLLECTION_PREFIX}project"
        indexes = [pymongo.IndexModel([("name", pymongo.TEXT), ("user_id", pymongo.TEXT)], name="name_text_index", unique=True)]

    def link_dataset(self, dataset_id: str):
        if dataset_id not in self.project_links:
            self.project_links.append(dataset_id)

    def unlink_dataset(self, dataset_id: str):
        if dataset_id in self.project_links:
            self.project_links.remove(dataset_id)


class CreateProject(CamelModel):
    name: str = Field(..., pattern="^[0-9a-zA-Z_]+$")
    tags: list[str] = []


class UpdateProject(CamelModel):
    tags: list[str] = []

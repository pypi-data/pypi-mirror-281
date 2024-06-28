from typing import List, Optional

from fa_common import AlreadyExistsError, NotFoundError
from fa_common import logger as LOG
from fa_common.config import get_settings
from fa_common.models import StorageLocation
from fa_common.routes.user.models import UserDB
from fa_common.storage import get_storage_client

from .models import ProjectDB


async def get_project(user_id: str, project_name: str, expected: bool = True) -> Optional[ProjectDB]:
    """[summary]

    Arguments:
        user_id {str} -- [description]
        project_name {str} -- [description]

    Keyword Arguments:
        expected {bool} -- [description] (default: {True})

    Raises:
        NotFoundError: When project is expected but does not exist
    """

    project = await ProjectDB.find(ProjectDB.user_id == user_id, ProjectDB.name == project_name).first_or_none()
    if expected and project is None:
        LOG.warning(f"Project for user: {user_id} with name: {project_name} does not exist but was expected")
        raise NotFoundError(f"Project: {project_name} does not exist")

    if project is not None and not isinstance(project, ProjectDB):
        raise ValueError(f"ProjectDB: {project_name} was found but its type is invalid.")
    return project


async def create_project(user: UserDB, project: dict) -> ProjectDB:
    project_name = project.get("name", None)
    if project_name is None:
        raise ValueError("No project name was given")

    project_obj = await get_project(user.sub, project_name, expected=False)

    if project_obj is None:
        storage = StorageLocation(
            bucket_name=get_settings().BUCKET_NAME,
            path_prefix=f"{get_settings().BUCKET_PROJECT_FOLDER}{user.sub}-{project_name}",
            description="Project file storage.",
        )
        # wp = await create_workflow_project(user.sub, project_name, storage=storage)

        project_obj = ProjectDB(
            user_id=user.sub,
            name=project_name,
            storage=storage,
            **project,
        )
        LOG.info(f"ProjectDB {project_obj.id}")
    else:
        raise AlreadyExistsError(f"ProjectDB with the name {project_obj.name} for this user already exists.")

    await project_obj.save()

    return project_obj


async def update_project(
    user: UserDB,
    project: dict,
) -> ProjectDB:
    name: str = project.get("name", "")
    if not name:
        raise ValueError("No project name was given")
    project_obj = await get_project(user.sub, name, expected=True)

    if project_obj is None:
        raise NotFoundError(f"Project {name} does not exist")

    update_project = project_obj.model_copy(update=project)
    await update_project.save()

    return update_project


async def delete(user_sub: str, project_name: str) -> bool:
    """Deletes all stored data for a given project

    Arguments:
        user_token {[str]} -- [user]
        project_name {[str]} -- [project]

    Returns:
        [bool] -- [True if a project was deleted false if it didn't exist]
    """

    project = await get_project(user_sub, project_name, expected=True)
    if project is None:
        raise NotFoundError(f"Project {project_name} does not exist")

    storage_client = get_storage_client()
    if project.storage is not None:
        try:
            await storage_client.delete_file(project.storage.bucket_name, project.storage.path_prefix, True)
            LOG.info(f"Deleted project folder {project.storage.storage_full_path}")
        except Exception as err:
            if await storage_client.folder_exists(project.storage.bucket_name, project.storage.path_prefix):
                raise err
    # @NOTE: Gitlab only should be required
    # try:
    #     await delete_workflow_project(user.sub, project_name)
    #     LOG.info(f"Deleted project workflow id: {user.sub} Branch: {project_name}")
    # except ValueError as err:
    #     LOG.warning(err)

    if project is not None:
        await project.delete()

        if await get_project(user_sub, project_name, expected=False) is None:
            return True

    return False


async def get_projects_for_user(user_sub: str) -> List[ProjectDB]:
    """[summary]

    Arguments:
        user_token {str} -- [description]

    Returns:
        [type] -- [description]
    """

    return await ProjectDB.find_all(ProjectDB.user_id == user_sub).to_list()


async def get_project_for_user(user_sub: str, project_id: str) -> ProjectDB:
    """[summary]

    Arguments:
        user_token {str} -- [description]

    Returns:
        [type] -- [description]
    """
    projects = await ProjectDB.find(ProjectDB.user_id == user_sub, ProjectDB.id == project_id).to_list()

    if projects is None or len(projects) < 1:
        raise NotFoundError(f"ProjectDB {project_id} could not be found")
    elif len(projects) > 1:
        raise RuntimeError(f"Multiple projects found with id: {project_id} for user {user_sub}")

    return projects[0]


async def delete_projects_for_user(user_sub: str) -> bool:
    """[summary]

    Arguments:
        user_token {str} -- [description]

    Returns:
        [type] -- [description]
    """
    projects = await get_projects_for_user(user_sub)

    if len(projects) > 0:
        for project in projects:
            await delete(user_sub, project.name)

    return True

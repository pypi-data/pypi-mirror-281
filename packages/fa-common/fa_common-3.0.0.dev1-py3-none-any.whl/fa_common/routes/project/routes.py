from typing import List

from fastapi import APIRouter, Depends, Path

from fa_common.exceptions import NotFoundError
from fa_common.models import Message
from fa_common.routes.user.models import UserDB
from fa_common.routes.user.service import get_current_app_user

from . import service
from .models import CreateProject, ProjectDB, UpdateProject

router = APIRouter()


@router.get("/", response_model=List[ProjectDB], response_model_exclude=ProjectDB._api_out_exclude())
async def list_projects(
    current_user: UserDB = Depends(get_current_app_user),
) -> List[ProjectDB]:
    """List Users projects"""
    projects = await service.get_projects_for_user(current_user.sub)

    return projects


@router.get("/{project_id}", response_model=ProjectDB, response_model_exclude=ProjectDB._api_out_exclude())  # type: ignore
async def get_project(
    project_name: str = Path(..., regex="^[0-9a-zA-Z_]+$"),
    current_user: UserDB = Depends(get_current_app_user),
) -> ProjectDB:
    """Gets a project given the project_name"""
    project = await service.get_project(current_user.sub, project_name, expected=True)

    return project  # type: ignore


@router.delete("/{project_name}", response_model=Message)
async def delete_project(
    project_name: str = Path(..., regex="^[0-9a-zA-Z_]+$"),
    current_user: UserDB = Depends(get_current_app_user),
) -> Message:
    """Deletes a project given the project_name"""

    delete_outcome = await service.delete(current_user.sub, project_name)

    if delete_outcome is False:
        raise NotFoundError()

    return Message(message=f"Deleted project {project_name}.")


@router.put("/", response_model=ProjectDB, response_model_exclude=ProjectDB._api_out_exclude())
async def create_project(
    project: CreateProject,
    current_user: UserDB = Depends(get_current_app_user),
) -> ProjectDB:
    new_project = await service.create_project(current_user, project.model_dump())

    return new_project


@router.patch("/", response_model=ProjectDB, response_model_exclude=ProjectDB._api_out_exclude())
async def update_project(
    project: UpdateProject,
    current_user: UserDB = Depends(get_current_app_user),
) -> ProjectDB:
    updated_project = await service.update_project(current_user, project.model_dump())

    return updated_project

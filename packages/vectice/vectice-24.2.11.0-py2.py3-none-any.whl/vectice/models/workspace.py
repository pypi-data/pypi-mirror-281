from __future__ import annotations

import logging
from textwrap import dedent
from typing import TYPE_CHECKING

from rich.table import Table

from vectice.models.project import Project
from vectice.utils.common_utils import temp_print
from vectice.utils.logging_utils import format_description

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.api import Client


_logger = logging.getLogger(__name__)


class Workspace:
    """Represent a Vectice Workspace.

    Workspaces are containers used to organize projects, assets, and
    users.

    Vectice users have access to a personal workspace and other
    workspaces so they can learn and collaborate with other users. An
    organization will have many workspaces, each with an Admin and
    Members with different privileges.

    Note that only an Org Admin can create a new workspace in the
    organization.

    You can get a workspace from your [`Connection`][vectice.Connection]
    object by calling `workspace()`:

    ```python
    import vectice

    connect = vectice.connect(...)
    workspace = connect.workspace("Iris workspace")
    ```

    Or you can get it directly when connecting to Vectice:

    ```python
    import vectice

    workspace = vectice.connect(..., workspace="Iris workspace")
    ```

    See [`Connection.connect`][vectice.Connection.connect] to learn
    how to connect to Vectice.
    """

    def __init__(self, id: str, name: str, description: str | None = None):
        self._id = id
        self._name = name
        self._description = description
        self._client: Client
        self._connection: Connection

    def __post_init__(self, client: Client, connection: Connection):
        self._client = client
        self._connection = connection

    def __eq__(self, other: object):
        if not isinstance(other, Workspace):
            return NotImplemented
        return self.id == other.id

    def __repr__(self):
        description = self._description if self._description else "None"
        return f"Workspace(name={self.name!r}, id={self._id}, description={description!r})"

    @property
    def id(self) -> str:
        """The workspace's id.

        Returns:
            The workspace's id.
        """
        return self._id

    @property
    def name(self) -> str:
        """The workspace's name.

        Returns:
            The workspace's name.
        """
        return self._name

    @property
    def description(self) -> str | None:
        """The workspace's description.

        Returns:
            The workspace's description.
        """
        return self._description

    @property
    def properties(self) -> dict:
        """The workspace's name and id.

        Returns:
            A dictionary containing the `name` and `id` items.
        """
        return {"name": self.name, "id": self.id}

    def project(self, project: str) -> Project:
        """Get a project.

        Parameters:
            project: The project name or id.

        Returns:
            The project.
        """
        item = self._client.get_project(project, self.id)
        logging_output = dedent(
            f"""
                Project {item.name!r} successfully retrieved.

                For quick access to the Project in the Vectice web app, visit:
                {self._client.auth.api_base_url}/browse/project/{item.id}"""
        ).lstrip()
        _logger.info(logging_output)
        project_object = Project(item.id, self, item.name, item.description)
        return project_object

    def list_projects(self) -> None:
        """Prints a list of projects belonging to the workspace in a tabular format, limited to the first 10 items. A link is provided to view the remaining projects.

        Returns:
            None
        """
        project_outputs = self._client.list_projects(self.id)
        rich_table = Table(expand=True, show_edge=False)

        rich_table.add_column("Project id", justify="left", no_wrap=True, min_width=4, max_width=10)
        rich_table.add_column("Name", justify="left", no_wrap=True, max_width=15)
        rich_table.add_column("Description", justify="left", no_wrap=True, max_width=50)

        for project in project_outputs.list:
            rich_table.add_row(project.id, project.name, format_description(project.description))

        description = dedent(
            f"""
        There are {project_outputs.total} projects in the workspace {self.name!r} and a maximum of 10 projects are displayed in the table below:
        """
        ).lstrip()
        tips = dedent(
            """
        To access a specific project, use \033[1mworkspace\033[0m.project(Project ID)"""
        ).lstrip()
        link = dedent(
            f"""
            For quick access to the list of projects in the Vectice web app, visit:
            {self._client.auth.api_base_url}/browse/workspace/{self.id}"""
        ).lstrip()

        temp_print(description)
        temp_print(table=rich_table)
        temp_print(tips)
        temp_print(link)

    @property
    def connection(self) -> Connection:
        """The Connection to which this workspace belongs.

        Returns:
            The Connection to which this workspace belongs.
        """
        return self._connection

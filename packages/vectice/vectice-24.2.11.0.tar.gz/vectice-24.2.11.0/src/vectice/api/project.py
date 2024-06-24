from __future__ import annotations

import re
from typing import TYPE_CHECKING

from gql import gql

from vectice.api.http_error_handlers import MissingReferenceError
from vectice.api.json.paged_response import PagedResponse
from vectice.utils.api_utils import PAGINATE_OUTPUT, get_page_input
from vectice.utils.vectice_ids_regex import PROJECT_VID_REG

if TYPE_CHECKING:
    from vectice.api.json.project import ProjectOutput

from gql.transport.exceptions import TransportQueryError

from vectice.api.gql_api import GqlApi, Parser

_RETURNS = """
            vecticeId
            name
            description
            workspace {
                vecticeId
                name
                description
                __typename
            }
            __typename
"""


_RETURNS_LIST = """
            vecticeId
            name
            description
            __typename
"""

_RETURNS_PAGE = PAGINATE_OUTPUT.format(_RETURNS_LIST)


class ProjectApi(GqlApi):
    def get_project(self, project: str, workspace: str | None) -> ProjectOutput:
        search_vectice_id = re.search(PROJECT_VID_REG, project)
        if search_vectice_id:
            gql_query = "getProjectById"
            variable_types = "$projectId:VecticeId!"
            variables = {"projectId": project}
            kw = "projectId:$projectId"
        else:
            if workspace is None:
                raise MissingReferenceError("workspace")
            gql_query = "getProjectByName"
            variable_types = "$name:String!,$workspaceId:VecticeId!"
            variables = {"name": project, "workspaceId": workspace}
            kw = "name:$name,workspaceId:$workspaceId"
        query = GqlApi.build_query(
            gql_query=gql_query, variable_types=variable_types, returns=_RETURNS, keyword_arguments=kw, query=True
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            project_output: ProjectOutput = Parser().parse_item(response[gql_query])
            return project_output
        except TransportQueryError as e:
            self._error_handler.handle_post_gql_error(e, "project", project)

    def list_projects(self, workspace: str) -> PagedResponse[ProjectOutput]:
        gql_query = "getProjectList"
        variable_types = "$page: PageIndexInput!,$workspaceId:VecticeId!"
        variables = {"page": get_page_input(), "workspaceId": workspace}
        kw = "page:$page,workspaceId:$workspaceId"
        query = GqlApi.build_query(
            gql_query=gql_query,
            variable_types=variable_types,
            returns=_RETURNS_PAGE,
            keyword_arguments=kw,
        )
        query_built = gql(query)
        try:
            response = self.execute(query_built, variables)
            project_output: PagedResponse[ProjectOutput] = Parser().parse_paged_response(response[gql_query])
            return project_output
        except TransportQueryError as e:
            self._error_handler.handle_post_gql_error(e, "projects", "list")

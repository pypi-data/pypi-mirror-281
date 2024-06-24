from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from vectice.api.json.phase import PhaseOutput, PhaseStatus
from vectice.services import PhaseService

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.api import Client
    from vectice.api.json.iteration import IterationStatus
    from vectice.models import Project, Workspace
    from vectice.models.iteration import Iteration


class Phase:
    """Represent a Vectice phase.

    Phases reflect the real-life phases of the project lifecycle
    (i.e., Business Understanding, Data Preparation, Modeling,
    Deployment, etc.).

    Phases let you document the goals, assets, and outcomes along with
    the status to organize the project, enforce best practices, allow
    consistency, and capture knowledge.

    To get a project's phase:

    ```python
    phase = project.phase("Business Understanding")
    ```

    Iterations can then be created for this phase.

    ```python
    my_origin_dataset = ...
    iteration = phase.create_iteration()
    iteration.log(my_origin_dataset)
    ```

    NOTE: **Phases are created in the Vectice App,
    iterations are created from the Vectice python API.**

    See the documentation of [Iterations][vectice.models.Iteration]
    for more information about iterations.
    """

    __slots__: ClassVar[list[str]] = [
        "_id",
        "_project",
        "_name",
        "_index",
        "_status",
        "_current_iteration",
        "_pointers",
        "_client",
        "_phase_service",
    ]

    def __init__(
        self,
        output: PhaseOutput,
        project: Project,
        client: Client,
    ):
        self._id = output.id
        self._project = project
        self._name = output.name
        self._index = output.index
        self._status = output.status
        self._client = client
        # TODO it seems useless, remove it
        self._current_iteration: Iteration | None = None
        # TODO this must be injected at phase creation so we have only one service instance, keeping like this for a 1st implementation
        self._phase_service = PhaseService(self._client)

    def __repr__(self):
        return f"Phase (name='{self.name}', id={self.id}, status='{self.status.name}')"

    def __eq__(self, other: object):
        if not isinstance(other, Phase):
            return NotImplemented
        return self.id == other.id

    @property
    def id(self) -> str:
        """The phase's id.

        Returns:
            The phase's id.
        """
        return self._id

    @id.setter
    def id(self, phase_id: str):
        """Set the phase's id.

        Parameters:
            phase_id: The phase id to set.
        """
        self._id = phase_id

    @property
    def name(self) -> str:
        """The phase's name.

        Returns:
            The phase's name.
        """
        return self._name

    @property
    def index(self) -> int:
        """The phase's index.

        Returns:
            The phase's index.
        """
        return self._index

    @property
    def status(self) -> PhaseStatus:
        """The phase's status.

        Returns:
            The phase's status.
        """
        return self._status

    @property
    def properties(self) -> dict[str, str | int]:
        """The phase's name, id, and index.

        Returns:
            A dictionary containing the `name`, `id`, and `index` items.
        """
        return {"name": self.name, "id": self.id, "index": self.index}

    @property
    def connection(self) -> Connection:
        """The connection to which this phase belongs.

        Returns:
            The connection to which this phase belongs.
        """
        return self._project.connection

    @property
    def workspace(self) -> Workspace:
        """The workspace to which this phase belongs.

        Returns:
            The workspace to which this phase belongs.
        """
        return self._project.workspace

    @property
    def project(self) -> Project:
        """The project to which this phase belongs.

        Returns:
            The project to which this phase belongs.
        """
        return self._project

    def list_iterations(self, only_mine: bool = False, statuses: list[IterationStatus] | None = None) -> None:
        """Prints a list of iterations belonging to the phase in a tabular format, limited to the last 10 items.

        Parameters:
            only_mine: Display only the iterations where the user is the owner.
            statuses: Filter iterations on specified statuses.

        Returns:
            None

        """
        return self._phase_service.list_iterations(phase=self, only_mine=only_mine, statuses=statuses)

    def create_or_get_current_iteration(self) -> Iteration | None:
        """Get or create an iteration.

        If your last updated iteration is writable (Not Started or In Progress), Vectice will return it.
        Otherwise, Vectice will create a new one and return it.
        If multiple writable iterations are found, Vectice will print a list of the iterations to complete or cancel.

        Returns:
            An iteration or None if Vectice could not determine which iteration to retrieve.
        """
        iteration = self._phase_service.create_or_get_current_iteration(phase=self)
        self._current_iteration = iteration
        return self._current_iteration

    def iteration(self, index: int | str) -> Iteration:
        """Get an iteration.

        Fetch and return an iteration by index or id.

        Parameters:
            index: The index or id of an existing iteration.

        Returns:
            An iteration.

        Raises:
            InvalidIdError: When index is a string and not matching 'ITR-[int]'
            IterationIdError: Iteration with specified id does not exist.
            IterationIndexError: Iteration with specified index does not exist.
        """
        iteration = self._phase_service.get_iteration_by_id_or_index(phase=self, index_or_id=index)
        self._current_iteration = iteration
        return self._current_iteration

    def create_iteration(self) -> Iteration:
        """Create a new iteration.

        Create and return an iteration.

        Returns:
            An iteration.
        """
        iteration = self._phase_service.create_iteration(phase=self)
        self._current_iteration = iteration
        return self._current_iteration

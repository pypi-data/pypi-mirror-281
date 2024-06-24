from __future__ import annotations

import logging
from io import BufferedReader, IOBase
from typing import TYPE_CHECKING

from PIL.Image import Image

from vectice.api.http_error_handlers import VecticeException
from vectice.api.json import AttachmentOutput, DatasetRegisterOutput, ModelRegisterOutput
from vectice.api.json.iteration import (
    IterationInput,
    IterationStepArtifactEntityMetadataInput,
    IterationStepArtifactInput,
    IterationStepArtifactType,
)
from vectice.utils.common_utils import (
    check_string_sanity,
    get_image_or_file_variables,
    get_notebook_path,
    get_script_path,
    set_dataset_attachments,
    set_model_attachments,
)
from vectice.utils.dataframe_utils import transform_table_to_metadata_dict

if TYPE_CHECKING:
    from vectice.api.client import Client
    from vectice.api.json.code_version import CodeVersion
    from vectice.models.dataset import Dataset
    from vectice.models.iteration import Iteration
    from vectice.models.model import Model
    from vectice.models.table import Table

_logger = logging.getLogger(__name__)

lineage_file_id = None
code_source_file = get_notebook_path() or get_script_path()


class IterationService:
    def __init__(self, iteration: Iteration, client: Client):
        self._client = client
        self._iteration = iteration

    def log_image_or_file(self, asset: str | IOBase | Image, section: str | None = None):
        _, filename = self._create_image_or_file_artifact(asset, section)
        return filename

    def log_comment(self, asset: int | float | str, section: str | None = None):
        if isinstance(asset, str):
            check_string_sanity(asset)
        artifact_inp: list[IterationStepArtifactInput] = [IterationStepArtifactInput(type="Comment", text=str(asset))]
        self._client.add_iteration_artifacts(iteration_id=self._iteration.id, artifacts=artifact_inp, section=section)

    def log_table(self, asset: Table, section: str | None = None):
        data = transform_table_to_metadata_dict(asset)
        entity_metadata = IterationStepArtifactEntityMetadataInput(name=asset.name, content={"data": data})

        artifact_inp: list[IterationStepArtifactInput] = [
            IterationStepArtifactInput(type="EntityMetadata", entityMetadata=entity_metadata)
        ]
        self._client.add_iteration_artifacts(iteration_id=self._iteration.id, artifacts=artifact_inp, section=section)

    def log_model(self, asset: Model, section: str | None = None):
        from vectice import code_file_capture

        global code_source_file

        code_version = self._get_code_version()
        model_data = self._client.register_model(
            model=asset,
            phase=self._iteration.phase,
            iteration=self._iteration,
            code_version=code_version,
            section=section,
        )
        if code_file_capture:
            if code_source_file:
                self._attach_code_file_to_lineage(model_data, code_source_file)
        attachments_output, success_pickle = set_model_attachments(self._client, asset, model_data.model_version)
        return model_data, attachments_output, success_pickle

    def log_dataset(self, asset: Dataset, section: str | None = None):
        from vectice import code_file_capture

        global code_source_file

        code_version = self._get_code_version()
        dataset_output = self._client.register_dataset_from_source(
            dataset=asset,
            iteration_id=self._iteration.id,
            code_version=code_version,
            section=section,
        )
        if code_file_capture:
            if code_source_file:
                self._attach_code_file_to_lineage(dataset_output, code_source_file)
        attachments_output = set_dataset_attachments(self._client, asset, dataset_output.dataset_version)
        return dataset_output, attachments_output

    def update(self, name: str | None = None):
        if name is not None:
            self._update_name(name)

    def _update_name(self, name: str):
        self._client.update_iteration(self._iteration.id, IterationInput(name=name))
        self._iteration.name = name
        _logger.info(f"Iteration {self._iteration.id!r} name successfully updated.")

    def _create_code_version_file_artifact(
        self, value: str | IOBase | Image, lineage_id: int
    ) -> AttachmentOutput | None:
        is_image_or_file, filename = get_image_or_file_variables(value)
        try:
            artifact, *_ = self._client.upsert_lineage_attachments(
                files=[("file", (filename, is_image_or_file))], lineage_id=lineage_id
            )
            if isinstance(is_image_or_file, BufferedReader):
                is_image_or_file.close()
            return AttachmentOutput(
                fileId=artifact.fileId,
                fileName=artifact.fileName,
                contentType=artifact.contentType,
                entityId=artifact.entityId,
                entityType=artifact.entityType,
            )
        except VecticeException as error:
            raise error
        except Exception:
            pass

    def _create_image_or_file_artifact(
        self, value: str | IOBase | Image, section: str | None = None
    ) -> tuple[IterationStepArtifactInput, str]:
        is_image_or_file, filename = get_image_or_file_variables(value)
        try:
            artifact, *_ = self._client.upsert_iteration_attachments(
                files=[("file", (filename, is_image_or_file))], iteration_id=self._iteration.id, step_name=section
            )
            if isinstance(is_image_or_file, BufferedReader):
                is_image_or_file.close()
            return (
                IterationStepArtifactInput(id=artifact.fileId, type=IterationStepArtifactType.EntityFile.name),
                filename,
            )
        except VecticeException as error:
            raise error
        except Exception as error:
            raise ValueError("Check the provided image.") from error

    def _get_code_version(self) -> CodeVersion | None:
        # TODO: cyclic imports
        from vectice import code_capture
        from vectice.models.code_version import capture_code_version, inform_if_git_repo

        if code_capture:
            return capture_code_version()
        else:
            inform_if_git_repo()
            return None

    def _attach_code_file_to_lineage(
        self, asset_output: DatasetRegisterOutput | ModelRegisterOutput, code_source_file: str
    ) -> None:
        global lineage_file_id

        try:
            lineage_id = None
            if hasattr(asset_output, "dataset_version"):
                lineage_id = asset_output.dataset_version.origin_id  # pyright: ignore[reportAttributeAccessIssue]
            if hasattr(asset_output, "model_version"):
                lineage_id = asset_output.model_version.origin_id  # pyright: ignore[reportAttributeAccessIssue]

            if lineage_id and lineage_file_id:
                self._client.attach_file_to_lineage(lineage_id, lineage_file_id)
            if lineage_id and lineage_file_id is None:
                attachment_output = self._create_code_version_file_artifact(code_source_file, lineage_id)
                lineage_file_id = attachment_output.fileId if attachment_output else None
        except Exception:
            pass

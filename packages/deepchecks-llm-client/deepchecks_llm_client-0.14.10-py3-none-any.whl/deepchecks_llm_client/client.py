import io
import logging
import time
import typing as t
from datetime import datetime

import pandas as pd
import pytz
from deepchecks_llm_client.api import API
from deepchecks_llm_client.data_types import (
    AnnotationType,
    ApplicationType,
    ApplicationVersionSchema,
    CustomPropertyType,
    EnvType,
    Interaction,
    InteractionCompleteEvents,
    LogInteractionType,
    PropertyColumnType,
    Step,
    Tag,
)
from deepchecks_llm_client.exceptions import DeepchecksLLMClientError
from deepchecks_llm_client.openai_instrumentor import OpenAIInstrumentor
from deepchecks_llm_client.utils import HandleExceptions, HandleGeneratorExceptions, convert_to_enum, get_timestamp

__all__ = ["dc_client", "DeepchecksLLMClient"]


logging.basicConfig()
logger = logging.getLogger(__name__)
init_logger = logging.Logger(__name__ + ".init")

DEFAULT_ENV_TYPE = EnvType.PROD


class DeepchecksLLMClient:
    def __init__(self):
        self._api: API = None
        self.app: t.Dict[str, t.Any] = None
        self.instrumentor: OpenAIInstrumentor = None
        self._initialized: bool = False
        self._log_level: int = logging.WARNING
        self.silent_mode: bool = True

    @HandleExceptions(init_logger)
    def init(
            self,
            host: str,
            api_token: str,
            app_name: t.Optional[str] = None,
            app_type: t.Optional[ApplicationType] = None,
            version_name: t.Optional[str] = None,
            version_description: t.Optional[str] = None,
            version_metadata: t.Optional[t.List[t.Dict[str, t.Any]]] = None,
            env_type: EnvType = DEFAULT_ENV_TYPE,
            auto_collect: bool = False,
            log_level: int = logging.WARNING,
            silent_mode: bool = False,
    ):
        """
        Connect to Deepchecks LLM Server

        Parameters
        ==========
        host : str
            Deepchecks host to communicate with
        api_token : str
            Deepchecks API Token (can be generated from the UI)
        app_name : str
            Application name to connect to
        app_type: ApplicationType
            Application type.
        version_name : str, default="0.0.1"
            Version name to connect to inside the application,
            if Version name does not exist SDK will create it automatically,
        version_description: str, defaults to ""
            Version description
        version_metadata: List[Dict[str, t.Any]] defaults to None
            Custom fields that will be added to created version in key: value pair format
        env_type : EnvType, default=EnvType.PROD
            could be EnvType.PROD (for "Production") or EnvType.EVAL (for "Evaluation")
        auto_collect : bool, default=False
            Auto collect calls to LLM Models
        silent_mode: bool, default=False
            If True, the SDK will print logs upon encountering errors rather than raising them
        log_level: int, default=logging.WARNING
            Set SDK loggers logging level

        Returns
        =======
        None
        """
        if self._initialized:
            logger.warning(
                "Deepchecks client was initialized already. "
                "We will ignore newly provided parameters"
            )
            return

        logger.setLevel(log_level)
        self._log_level = log_level
        self.silent_mode = silent_mode

        if self._api is None:
            if host is not None and api_token is not None:
                self._api = API.instantiate(host=host, token=api_token)
            else:
                raise DeepchecksLLMClientError("host/token parameters must be provided")

        if app_name:
            self.app = self._api.get_application(app_name)
            if self.app and app_type and app_type != self.app["kind"]:
                logger.warning(
                    f"Application: \"{app_name}\" already exist with app type: \"{self.app['kind']}\","
                    f" provided app type: {app_type} argument will be ignored",
                )
            elif not self.app and app_type and app_name:
                self.app = self.create_application(
                    application_name=app_name,
                    app_type=app_type,
                    versions=[
                        ApplicationVersionSchema(
                            name=version_name,
                            description=version_description,
                            custom=version_metadata,
                        )
                    ],
                )
            self.app_name = app_name
            self.version_name = version_name
        self.env_type = convert_to_enum(env_type, EnvType)

        self.instrumentor = None
        if auto_collect:
            self.instrumentor = OpenAIInstrumentor(self.api, log_level, auto_collect, silent_mode)
            self.instrumentor.perform_patch()
        self._initialized = True

    @property
    def initialized(self):
        return self._initialized

    @property
    def api(self) -> API:
        if self._api:
            return self._api
        raise DeepchecksLLMClientError("dc_client was not initialized correctly, please re-create it")

    @property
    @HandleExceptions(logger)
    def app_name(self):
        return self.api.app_name

    @app_name.setter
    @HandleExceptions(logger)
    def app_name(self, new_app_name: str):
        self.api.app_name = new_app_name
        self.app = self._api.get_application(new_app_name)
        if not self.app:
            raise DeepchecksLLMClientError(
                f"Application: \"{new_app_name}\", does not exist, please create it via the UI or create_application method"
            )

    @property
    @HandleExceptions(logger)
    def version_name(self):
        return self.api.version_name

    @version_name.setter
    @HandleExceptions(logger)
    def version_name(self, new_version_name: str):
        self.api.version_name = new_version_name

    @property
    @HandleExceptions(logger)
    def env_type(self):
        return self.api.env_type

    @env_type.setter
    @HandleExceptions(logger)
    def env_type(self, new_env_type: str):
        self.api.env_type = convert_to_enum(new_env_type, EnvType)

    @HandleExceptions(logger, return_self=True)
    def auto_collect(self, enabled: bool):
        if not self.instrumentor:
            self.instrumentor = OpenAIInstrumentor(
                api=self.api, log_level=self._log_level, auto_collect=enabled, silent_mode=self.silent_mode
            )
        else:
            self.instrumentor.auto_collect(auto_collect=enabled)

        if enabled is False:
            self.instrumentor.unwrap_patched_calls()
        if enabled is True:
            self.instrumentor.perform_patch()

        return self

    @HandleExceptions(logger, return_self=True)
    def set_tags(self, tags: t.Dict[Tag, str]):
        self.api.set_tags(tags)
        return self

    @HandleExceptions(logger)
    def create_application(
            self,
            application_name: str,
            app_type: ApplicationType,
            versions: t.Optional[t.List[ApplicationVersionSchema]] = None,
            description: t.Optional[str] = None,
    ):
        """Create a new application

        Parameters
        ----------
        application_name
            Name of the application
        app_type
            The type of application to create
        versions
            List of versions to create for the application
        description
            Description of the application

        Returns
        -------
            The response from the API
        """
        self.api.create_application(application_name=application_name, app_type=app_type, versions=versions, description=description)
        return self.api.get_application(app_name=application_name)

    @HandleExceptions(logger)
    def get_applications(self):
        """Get all applications as Application objects.

        Returns
        -------
        List[Application]
            List of applications
        """
        return self.api.get_applications()

    @HandleExceptions(logger)
    def get_versions(self, app_name: t.Optional[str] = None):
        """Get all versions of an application as Version objects.

        Parameters
        ----------
        app_name
            Name of the application to get versions for

        Returns
        -------
        List[ApplicationVersion]
            List of versions
        """
        return self.api.get_versions(app_name=app_name)

    @HandleExceptions(logger)
    def annotate(self, user_interaction_id: str, version_name: str,
                 annotation: AnnotationType = None, reason: t.Optional[str] = None):
        """Annotate a specific interaction by its user_interaction_id

        Parameters
        ----------
        user_interaction_id
            The user_interaction_id of the interaction to annotate
        version_name
            Name of the version to which this interaction belongs
        annotation
            Could be one of AnnotationType.GOOD, AnnotationType.BAD, AnnotationType.UNKNOWN
            or None to remove annotation
        reason
            String that explains the reason for the annotation

        Returns
        -------
            None
        """
        version_id = self._get_version_id(version_name)
        self.api.annotate(user_interaction_id, version_id, annotation, reason=reason)

    # pylint: disable=redefined-builtin
    @HandleExceptions(logger)
    def log_interaction(self,
                        input: str,
                        output: str,
                        full_prompt: str = None,
                        information_retrieval: t.Union[t.List[str], str] = None,
                        annotation: AnnotationType = None,
                        annotation_reason: str = None,
                        user_interaction_id: str = None,
                        started_at: t.Union[datetime, float, None] = None,
                        finished_at: t.Union[datetime, float, None] = None,
                        steps: t.List[Step] = None,
                        custom_props: t.Dict[str, t.Any] = None,
                        vuln_type: t.Optional[str] = None,
                        vuln_trigger_str: t.Optional[str] = None,
                        topic: t.Optional[str] = None,
                        ) -> str:
        """The log_interaction method is used to log user interactions.

        Parameters
        ----------
        input : str
            Input data
        output : str
            Output data
        full_prompt : str
            Full prompt data
        information_retrieval : str
            Information retrieval
        annotation : AnnotationType
            Annotation type of the interaction
        user_interaction_id : str
            Unique identifier of the interaction
        started_at : datetime or float
            Timestamp the interaction started at. Datetime format is deprecated, use timestamp instead
        finished_at : datetime or float
            Timestamp the interaction finished at. Datetime format is deprecated, use timestamp instead
        steps : list of Step
            List of steps taken during the interaction
        custom_props : dict
            Additional custom properties
        annotation_reason : str, optional
            Reason for the annotation
        vuln_type : str, optional
            Type of vulnerability (Only used in case of EnvType.PENTEST and must be sent there).
        vuln_trigger_str : str, optional
            Vulnerability trigger string (Only used in case of EnvType.PENTEST and is optional there).

        Returns
        -------
        str
            The uuid of the interaction

        """
        if isinstance(started_at, datetime) or isinstance(finished_at, datetime):
            logger.warning(
                "Deprecation Warning: Usage of datetime for started_at/finished_at is deprecated, use timestamp instead."
            )
            started_at = started_at.timestamp() if started_at else datetime.now(tz=pytz.UTC).timestamp()
            finished_at = finished_at.timestamp() if finished_at else None

        # pylint: disable=redefined-builtin
        result = self.api.log_interaction(
            input=input,
            output=output,
            full_prompt=full_prompt,
            information_retrieval=information_retrieval \
                if information_retrieval is None or isinstance(information_retrieval, list) \
                else [information_retrieval],
            annotation=annotation,
            annotation_reason=annotation_reason,
            user_interaction_id=user_interaction_id,
            started_at=started_at,
            finished_at=finished_at,
            steps=steps,
            custom_props=custom_props,
            vuln_type=vuln_type,
            vuln_trigger_str=vuln_trigger_str,
            topic=topic,
        )
        return result.json()[0]

    @HandleExceptions(logger)
    def log_batch_interactions(self, interactions: t.List[LogInteractionType]) -> t.List[str]:
        """Logs multiple interactions at once.

        Parameters
        ----------
        interactions : list of LogInteractionType
            The list of interaction data to log.

        Returns
        -------
        list of str
            List of the uuids of the interactions

        """
        result = self.api.log_batch(interactions=interactions)
        return result.json()

    @HandleExceptions(logger)
    def update_interaction(
            self,
            user_interaction_id: str,
            version_name: str,
            annotation: AnnotationType = None,
            annotation_reason: t.Optional[str] = None,
            custom_props: t.Union[t.Dict[str, t.Any], None] = None,
    ):
        """Update a specific interaction by its user_interaction_id

        Parameters
        ----------
        user_interaction_id
            Unique id of the interaction to update
        version_name
            Name of the version to which this interaction belongs
        annotation
            Could be one of AnnotationType.GOOD, AnnotationType.BAD, AnnotationType.UNKNOWN
        annotation_reason
            String that explains the reason for the annotation
        custom_props:
            Dictionary of custom properties for interaction

        Returns
        -------
            None
        """
        version_id = self._get_version_id(version_name)
        self.api.update_interaction(
            user_interaction_id=user_interaction_id,
            app_version_id=version_id,
            annotation=annotation,
            annotation_reason=annotation_reason,
            custom_props=custom_props,
        )

    @HandleExceptions(logger)
    def delete_interactions(self, user_interaction_ids: t.List[str]):
        """Delete specific interactions by their user_interaction_ids

        Parameters
        ----------
        user_interaction_ids: List[str]
            List of interaction user ids to delete

        Returns
        -------
            None
        """
        version_id = self._get_version_id(self.version_name)
        self.api.delete_interactions(
            user_interaction_ids=user_interaction_ids, app_version_id=version_id,
        )

    @HandleExceptions(logger)
    def update_application_config(self, file):
        """Update the auto-annotation YAML configuration file for the current application.

        Parameters
        ----------
        file : str
            The path to the configuration file to update

        Returns
        -------
            None
        """
        self.api.update_application_config(application_id=self.app["id"], file=file)

    @HandleExceptions(logger)
    def get_application_config(self, file_save_path: t.Union[str, None] = None) -> str:
        """Write the auto-annotation YAML configuration file to the specified path.

        Parameters
        ----------
        file_save_path : str | None, optional
            The path to save the configuration file to. If None, the file will not be saved.

        Returns
        -------
        str
            The auto-annotation YAML configuration file as a string.
        """
        return self.api.get_application_config(application_id=self.app["id"], file_save_path=file_save_path)

    @HandleGeneratorExceptions(init_logger)
    def data_iterator(self,
                      environment: t.Union[EnvType, str],
                      start_time: t.Union[datetime, int, None] = None,
                      end_time: t.Union[datetime, int, None] = None,
                      user_interaction_ids: t.Union[t.List[str], None] = None,
                      ) -> t.Iterable[Interaction]:
        """
        Fetch all interactions from the specified environment type (PROD/EVAL) as an iterable.
        Supports pagination, so this API is suitable for iterating over large amounts of data.

        Parameters
        ----------
        environment : EnvType | str
            The environment type from which to fetch interactions. This can be either "PROD" or "EVAL".

        start_time : datetime | int | None, optional
            The start time from which to fetch interactions. This can be a datetime object or an integer.
            If not provided, interactions will be fetched from the beginning.

        end_time : datetime | int | None, optional
            The end time until which to fetch interactions. This can be a datetime object or an integer.
            If not provided, interactions will be fetched up to the most recent.

        user_interaction_ids: list | None, optional
            user interactions ids to include into the list of interactions.annotation_reason


        Returns
        -------
        Iterable[Interaction]
            An iterable collection of interactions.

        """
        version_id = self._get_version_id(self.version_name)

        offset = 0
        limit = 20

        while True:
            interactions = \
                self.api.get_interactions(version_id,
                                          environment=environment,
                                          start_time_epoch=get_timestamp(start_time),
                                          end_time_epoch=get_timestamp(end_time),
                                          user_interaction_ids=user_interaction_ids,
                                          limit=limit, offset=offset)
            for interaction in interactions:
                yield self._build_interaction_object(interaction)

            # If the size of the data is less than the limit, we"ve reached the end
            if len(interactions) < limit:
                break

            offset += limit

    @HandleExceptions(init_logger)
    def get_data(self, environment: t.Union[EnvType, str],
                 return_topics: bool = False, return_annotation_data: bool = False,
                 return_input_props: bool = False, return_output_props: bool = False,
                 return_custom_props: bool = False, return_llm_props: bool = False,
                 start_time: t.Union[datetime, int, None] = None,
                 end_time: t.Union[datetime, int, None] = None,
                 return_similarities: bool = False,
                 user_interaction_ids: t.Union[t.List[str], None] = None,) -> t.Union[pd.DataFrame, None]:
        """
        Fetch all the interactions from the specified environment (PROD/EVAL) as a pandas DataFrame.

        Parameters
        ----------
        environment : EnvType | str
            The environment type from which to fetch interactions. This can be either "PROD" or "EVAL".

        return_annotation_data : bool, optional
            Whether to include annotation info in the data.

        return_topics : bool, optional
            Whether to include the topic in the data.

        return_input_props : bool, optional
            Whether to include input properties in the data.

        return_output_props : bool, optional
            Whether to include the output properties in the data.

        return_custom_props : bool, optional
            Whether to include custom properties in the data.

        return_llm_props : bool, optional
            Whether to include LLM properties in the data.

        return_similarities : bool, optional
            Whether to include similarities in the data.

        start_time : datetime | int | None, optional
            The start time from which to fetch interactions. This can be a datetime object or an integer.
            If not provided, interactions will be fetched from the beginning.

        end_time : datetime | int | None, optional
            The end time until which to fetch interactions. This can be a datetime object or an integer.
            If not provided, interactions will be fetched up to the most recent.

        user_interaction_ids: list | None, optional
            user interactions ids to include in the data.
        Returns
        -------
        pd.DataFrame | None
            A pandas DataFrame containing the interactions, or None in case of a problem retrieving the data.

        """
        eval_set_version_id = self._get_version_id(self.version_name)
        csv_as_text = self.api.get_interactions_csv(
            eval_set_version_id,
            environment=environment,
            start_time_epoch=get_timestamp(start_time),
            end_time_epoch=get_timestamp(end_time),
            return_topics=return_topics,
            return_annotation_data=return_annotation_data,
            return_output_props=return_output_props,
            return_custom_props=return_custom_props,
            return_input_props=return_input_props,
            return_llm_props=return_llm_props,
            return_similarities=return_similarities,
            user_interaction_ids=user_interaction_ids,
        )
        if not csv_as_text:
            return pd.DataFrame()
        return pd.read_csv(io.StringIO(csv_as_text))

    @HandleExceptions(init_logger)
    def get_interaction_by_user_interaction_id(self, user_interaction_id: str) -> Interaction:
        """Get a specific interaction by its user_interaction_id

        Parameters
        ----------
        user_interaction_id
            Unique id of the interaction to get

        Returns
        -------
        Interaction
            The interaction object, including the input, output, properties and other fields
        """
        version_id = self._get_version_id(self.version_name)
        interaction = self.api.get_interaction_by_user_interaction_id(version_id, user_interaction_id)
        return self._build_interaction_object(interaction)

    def _get_version_id(self, version_name, create_if_not_exist=False):

        app = self.api.get_application(self.api.app_name)
        if not app:
            raise DeepchecksLLMClientError(f"Application: \"{self.api.app_name}\", does not exist")
        if version_name:
            eval_set_version = next((ver for ver in app["versions"] if ver["name"] == version_name), None)
            if not eval_set_version:
                if not create_if_not_exist:
                    raise DeepchecksLLMClientError(
                        f"Could not find version \"{version_name}\", in application \"{self.api.app_name}\"",
                    )
                else:
                    return self.api.create_application_version(
                        application_id=app["id"], version_name=version_name,
                    )["id"]

        else:
            eval_set_version = max(app["versions"], key=lambda x: x["created_at"])
            if not eval_set_version:
                raise DeepchecksLLMClientError(
                    f"Could not find versions to select from in application \"{self.api.get_app_name()}\"")
        return eval_set_version["id"]

    def get_pentest_prompts(self, probes: t.Optional[t.List[str]] = None) -> pd.DataFrame:
        """Get pentest prompts for the application

        Parameters
        ----------
        probes: list of str
            List of probes to get pentest prompts for. If None, all probes will be returned.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the pentest prompts
        """
        csv_content = self.api.get_pentest_prompts(app_id=self.app["id"], probes=probes)
        df = pd.read_csv(io.StringIO(csv_content))
        return df

    def get_custom_properties(self) -> t.List[CustomPropertyType]:
        """Get the custom properties defined for the current application

        Returns
        -------
        list[CustomPropertyType]
            A list of custom properties defined for the application
        """
        custom_props = self.api.get_custom_properties_definitions(application_id=self.app["id"])
        return [
            CustomPropertyType(
                display_name=prop["display_name"],
                type=prop["type"],
                description=prop["description"]
            ) for prop in custom_props
        ]

    def create_custom_property(self, name: str, prop_type: PropertyColumnType, description: t.Optional[str] = None
                               ) -> None:
        """Define a custom property for the current application

        Parameters
        ----------
        name : str
            Name of the custom property
        prop_type : PropertyColumnType
            Type of the custom property
        description : str, optional
            Description of the custom property

        Returns
        -------
        None
        """
        self.api.create_custom_property_definition(
            application_id=self.app["id"], name=name, prop_type=prop_type, description=description,
        )

    def update_custom_property(self, old_name: str, new_name: t.Optional[str] = None,
                               description: t.Optional[str] = None) -> None:
        """Update a custom property for the current application

        Parameters
        ----------
        old_name : str
            Name of the custom property to update
        new_name : str, optional
            New name for the custom property
        description : str, optional
            Description of the custom property (if none provided, the description will not be updated)

        Returns
        -------
        None
        """
        self.api.update_custom_property_definition(
            application_id=self.app["id"],
            old_name=old_name,
            new_name=new_name if new_name else old_name,
            description=description,
        )

    def delete_custom_property(self, name: str):
        """Delete a custom property for the current application

        Parameters
        ----------
        name : str
            Name of the custom property to delete

        Returns
        -------
        None
        """
        self.api.delete_custom_property_definition(application_id=self.app["id"], name=name)

    @HandleExceptions(init_logger)
    def get_interactions_complete_status(
        self,
        user_interaction_ids:  t.List[str],
        events_to_check: t.Optional[t.List[InteractionCompleteEvents]] = None,
    ):
        """Get the completion status of interactions for specified events and user interaction IDs.

        Parameters
        ----------
        events_to_check : Optional[List[InteractionCompleteEvents]]
            A list of events whose completion status needs to be checked. By default, only annotation_completed is
            checked
        user_interaction_ids : List[str]
            A list of user interaction IDs to check for completion status.

        Returns
        -------
        Dict[InteractionCompleteEvents, bool]
            A dictionary where keys are events from `events_to_check`
            and values are objects that indicating whether interactions for each event are completed and number of
            completed interactions {"annotation_completed": {"all_completed": True, "number_of_completed": 10}}
        """

        if not events_to_check:
            events_to_check = [InteractionCompleteEvents.ANNOTATION_COMPLETED]
        version_id = self._get_version_id(self.version_name)
        return self.api.get_interactions_complete_status(
            app_version_id=version_id,
            events_to_check=events_to_check,
            user_interaction_ids=user_interaction_ids,
        )

    @HandleExceptions(init_logger)
    def get_data_if_calculations_completed(
        self,
        user_interaction_ids: t.List[str],
        events_to_check: t.Optional[t.List[InteractionCompleteEvents]] = None,
        max_retries: int = 60,
        retry_interval_in_seconds: int = 20,
        return_topics: bool = True, return_annotation_data: bool = True,
        return_input_props: bool = True, return_output_props: bool = True,
        return_custom_props: bool = True, return_llm_props: bool = True,
        return_similarities: bool = False,
    ) -> t.Optional[pd.DataFrame]:
        """This method checks if calculations for specified events are completed by calling `get_interactions_complete_status`.
        If all user_interaction_ids completed, then we will fetch the data for those ids,
        if not - will sleep and retry again. Consider increasing max_retries or retry_interval_in_seconds if running the method returns None.

        Parameters
        ----------
        events_to_check : Optional[List[InteractionCompleteEvents]]
            A list of events whose completion status needs to be checked. By default, only annotation_completed
            is checked
        user_interaction_ids : List[str]
            A list of user interaction IDs to retrieve data for.
        max_retries : Optional[int]
            Maximum number of retries if calculations are not completed. Defaults to 60.
        retry_interval_in_seconds : Optional[float]
            Interval between retries in seconds. Defaults to 20.
                return_annotation_data : bool, optional
            Whether to include annotation info in the data.
        return_topics : bool, optional
            Whether to include the topic in the data.
        return_annotation_data : bool, optional
            Whether to include annotation info in the data.
        return_input_props : bool, optional
            Whether to include input properties in the data.
        return_output_props : bool, optional
            Whether to include the output properties in the data.
        return_custom_props : bool, optional
            Whether to include custom properties in the data.
        return_llm_props : bool, optional
            Whether to include LLM properties in the data.
        return_similarities : bool, optional
            Whether to include similarities in the data.

        Returns
        -------
        Optional[pd.DataFrame]
            A DataFrame containing the retrieved data if calculations are completed, otherwise None.
        """
        if not events_to_check:
            events_to_check = [InteractionCompleteEvents.ANNOTATION_COMPLETED]
        retry_count = 0
        while retry_count < max_retries:
            complete_statuses = self.get_interactions_complete_status(events_to_check=events_to_check, user_interaction_ids=user_interaction_ids)
            if all(status["all_completed"] for status in complete_statuses.values()):
                return self.get_data(
                    environment=self.env_type,
                    return_topics=return_topics,
                    return_annotation_data=return_annotation_data,
                    return_input_props=return_input_props,
                    return_output_props=return_output_props,
                    return_custom_props=return_custom_props,
                    return_llm_props=return_llm_props,
                    return_similarities=return_similarities,
                    user_interaction_ids=user_interaction_ids,
                )
            else:
                for event, status in complete_statuses.items():
                    logger.debug(f"{event} = {status['number_of_completed']}")
                retry_count += 1
                time.sleep(retry_interval_in_seconds)
        return None

    @staticmethod
    def _build_interaction_object(interaction: dict) -> Interaction:
        return Interaction(
            user_interaction_id=interaction["user_interaction_id"],
            input=interaction["input"]["data"] if interaction.get("input") else None,
            information_retrieval=[i["data"] for i in interaction["information_retrieval"]] if
                                  interaction.get("information_retrieval") else None,
            full_prompt=interaction["prompt"]["data"] if interaction.get("prompt") else None,
            output=interaction["output"]["data"] if interaction.get("output") else None,
            created_at=interaction["created_at"],
            topic=interaction["topic"],
            output_properties=interaction.get("output_properties", {}) or {},
            input_properties=interaction.get("input_properties", {}) or {},
            custom_properties=interaction.get("custom_properties", {}) or {},
            llm_properties=interaction.get("llm_properties", {}) or {},
            llm_properties_reasons=interaction.get("llm_properties_reasons", {}) or {},
        )

# LLM Client publicly accessed singleton
dc_client: DeepchecksLLMClient = DeepchecksLLMClient()

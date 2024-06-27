# -----------------------------------------------------------------------------
# Deepchecks LLM Onboarding Script
# -----------------------------------------------------------------------------
# This script is designed to guide you through the process of integrating
# data with Deepchecks LLM Product, using Deepchecks' SDK.
# Please follow the instructions provided and replace placeholders with actual
# data as needed.


# Step 1: Import necessary modules
# Create new venv and install deepchecks' SDK using `pip install deepchecks-llm-client`
import uuid
from datetime import datetime

import openai
from deepchecks_llm_client.client import dc_client
from deepchecks_llm_client.data_types import AnnotationType, ApplicationType, EnvType, LogInteractionType, Step, StepType, Tag


def main():
    # pylint: disable=invalid-name
    # Step 2: Set up configuration

    # Fill deepchecks host name here
    DEEPCHECKS_LLM_HOST = "https://host-name-here"  # could be: https://app.llm.deepchecks.com

    # Login to deepchecks' service and generate new API Key (Configuration -> API Key) and place it here
    DEEPCHECKS_LLM_API_KEY = "Fill Key Here"

    # Use "Update Samples" in deepchecks' service, to create a new application name and place it here
    DEEPCHECKS_APP_NAME = "DemoApp"

    # In case you would like to experience with deepchecks auto collect capabilities, please set
    # Open AI's key here (as string)
    OPENAI_API_KEY = "Fill Key Here"

    # Step 3: Initialize the SDK

    # auto_collect=True wraps `openai.ChatCompletion` and `openai.Completion` APIs
    # so any OpenAI invocation will fire an event to Deepchecks with the relevant data
    # If you do not plan to use OpenAI auto collection, you can set it to `False`

    # Notice - deepchecks SDK was designed to be non-intrusive. It does not throw exceptions
    # and only print to log. By default, it prints only errors from the "init" phase
    # If you wish to increase verbosity, use `verbose=True` and `log_level=logging.INFO`
    version = "0.0.1"
    env_type = EnvType.EVAL

    print(
        f"init deepchecks client, host: {DEEPCHECKS_LLM_HOST}, "
        f"app: {DEEPCHECKS_APP_NAME}, version: {version}, env: {env_type}"
    )
    dc_client.init(host=DEEPCHECKS_LLM_HOST,
                   api_token=DEEPCHECKS_LLM_API_KEY,
                   app_name=DEEPCHECKS_APP_NAME,
                   version_name=version,
                   env_type=env_type,
                   auto_collect=True,
                   silent_mode=False,
                   app_type=ApplicationType.QA,
                   )

    # Step 4: Auto collecting OpenAI Data (Q&A + Annotation)
    if OPENAI_API_KEY:
        # You can set_tags() to add additional information to the collected data
        # most important is the INPUT, which is the actual user question, without this
        # information, deepchecks won't be able to evaluate the question the user asked
        INPUT = "How much is 2 plus 2?"
        # If you have "information retrieval" step in your flow, you can supply is as well
        # using the Tag.INFORMATION_RETRIEVAL tag
        INFORMATION_RETRIEVAL = "1 plus 1 equals 2"
        # Notice that you can add USER_ID (optional) to track the number of unique users that are
        # using your LLM application (remember PII and obfuscate the username if needed)
        dc_client.set_tags({Tag.INPUT: INPUT,
                            Tag.USER_ID: "A05fdfbb2035e@gmail.com",
                            Tag.INFORMATION_RETRIEVAL: INFORMATION_RETRIEVAL})

        # Setting up your OpenAI API credentials
        print("calling OpenAI ChatCompletion API")
        openai.api_key = OPENAI_API_KEY
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.7,
            messages=[
                {"role": "system",
                 "content": f"Act as a calculator {INFORMATION_RETRIEVAL}"},
                {"role": "user", "content": INPUT}
            ]
        )

        # The data has already logged to deepchecks server, you can annotate the data
        # in anytime you like using OpenAI's unique id
        # Notice that you can set your own unique id using Tags.USER_INTERACTION_ID (before calling
        # OpenAI's API), and use it here instead of OpenAI's id
        print(f"Annotating OpenAI interaction with key: {chat_completion.openai_id}")
        dc_client.annotate(
            user_interaction_id=str(chat_completion.openai_id),
            version_name=version,
            annotation=AnnotationType.GOOD,
        )

        # clear tags so we won't carry them on to the next calls
        # relevant only for "auto collected" data
        dc_client.set_tags({})
    else:
        print("OpenAI Key was not supply, skipping OpenAI demo")

    # Step 5: Explicit Logging of data and optionally addition of steps for flow visibility
    # Notice that we can also log custom properties - you can use custom properties that were
    # already defined via the UI, or use the "CP_xxx" convention to create new custom property
    # on the fly

    # We can explicitly log interaction
    print("log interaction using explicit Deepchecks API: log_interaction()")
    user_inter_id = str(uuid.uuid4())
    dc_client.log_interaction(input="my user input",
                              output="my model output",
                              full_prompt="system part: my user input",
                              annotation=AnnotationType.BAD,
                              user_interaction_id=user_inter_id,
                              started_at=datetime(2021, 10, 31, 15, 1, 0).astimezone(),
                              finished_at=datetime.utcnow().astimezone(),
                              steps=[
                                  Step(
                                      name="Information Retrieval",
                                      type=StepType.INFORMATION_RETRIEVAL,
                                      attributes={"env": "dev"},
                                      output="system part: my information retrieval"),
                                  Step(
                                      input="my user input + the retried data",
                                      name="Information Retrieval",
                                      type=StepType.LLM,
                                      attributes={"env": "dev"},
                                      annotation=AnnotationType.BAD,
                                      output="my model output"),
                                  Step(
                                      name="Information Retrieval",
                                      type=StepType.TRANSFORMATION,
                                      attributes={"env": "dev"},
                                      output="my model output after PII removal")
                              ],
                              custom_props={"CP_MY_PROP1": 0.1},
                              topic="Some Topic",
                              )

    # Notice that we can re-annotate our logged interation in a later phase
    # using out own external id
    print(f"Annotating explicit interaction with key: {user_inter_id}")
    dc_client.annotate(
        user_interaction_id=user_inter_id,
        version_name=version,
        annotation=AnnotationType.GOOD,
    )

    # Send batch of interactions to
    dc_client.log_batch_interactions(
        interactions=[
            LogInteractionType(
                input="my user input2",
                output="my model output2",
                full_prompt="system part: my user input2",
                annotation=AnnotationType.GOOD,
                user_interaction_id=str(uuid.uuid4()),
                started_at=datetime(2021, 10, 31, 15, 1, 0).astimezone(),
                finished_at=datetime.utcnow().astimezone(),
                steps=[
                    Step(
                        name="Information Retrieval",
                        type=StepType.INFORMATION_RETRIEVAL,
                        attributes={"env": "dev"},
                        output="system part: my information retrieval"),
                ],
                custom_props={"CP_MY_PROP1": 0.1}
            ),
            LogInteractionType(
                input="my user input3",
                output="my model output3",
                full_prompt="system part: my user input3",
                annotation=AnnotationType.GOOD,
                user_interaction_id=str(uuid.uuid4()),
                started_at=datetime(2021, 10, 31, 15, 1, 0).astimezone(),
                finished_at=datetime.utcnow().astimezone(),
                custom_props={"CP_MY_PROP1": 0.1}
            ),
        ]
    )

    # Step 6: Creating a new version based on the "0.0.1" eval set

    # Set different version / env type, to be carried on to the next calls
    # Usually, in "dev mode", you will log to "EnvType.EVAL" and use a different version
    # for each evaluation you make. Check the performance of your LLM application using deepchecks,
    # and deploy the selected version to production, and from that point on,
    # you will use "EnvType.PROD" with the "production version" to log production data
    new_version = "0.0.2"
    eval_env_type = EnvType.EVAL
    print(f"switching to version: {new_version}, and EnvType: {eval_env_type}")
    dc_client.version_name = new_version
    dc_client.env_type = eval_env_type

    # Now we have 1 or 2 interactions logged into deepchecks' under version '0.0.1'
    # We can get the "eval set" out of deepchecks and rerun it against OpenAI while log the
    # new result to our new version (i.e. - "0.0.2")
    if OPENAI_API_KEY:

        # data_iterator() can get "version_name" as param, if no version_name was supplied
        # the latest created version will be taken (this is useful when integrating it in the CI)
        dc_client.version_name = "0.0.1"
        for interaction in dc_client.data_iterator(EnvType.EVAL):
            print(f"processing eval set interaction with unique_interaction_id: {interaction.user_interaction_id}  "
                  f"(created_at: {interaction.created_at})")
            dc_client.version_name = "0.0.2"
            dc_client.set_tags({Tag.INPUT: interaction.input,
                                Tag.INFORMATION_RETRIEVAL: interaction.information_retrieval})

            # We run the same OpenAI command, only changing the temperature...
            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                api_key=OPENAI_API_KEY,
                temperature=0.2,
                messages=[
                    {"role": "system", "content": f"Act as a calculator {interaction.information_retrieval}"},
                    {"role": "user", "content": interaction.input}
                ]
            )
            dc_client.version_name = "0.0.1"

    # One can also retrieve eval set as dataframe, for example:
    dc_client.version_name = "0.0.1"
    df = dc_client.get_data(EnvType.EVAL)
    print("We can also fetch the eval set as dataframe, here are the dataframe columns")
    print(list(df.columns))


if __name__ == "__main__":
    main()

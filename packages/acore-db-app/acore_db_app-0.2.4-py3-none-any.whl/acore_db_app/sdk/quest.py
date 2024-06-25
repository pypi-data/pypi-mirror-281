# -*- coding: utf-8 -*-

import typing as T
import json

from boto_session_manager import BotoSesManager
from acore_paths.api import path_acore_db_app_cli
import aws_ssm_run_command.api as aws_ssm_run_command

from ..app.api import quest


def get_latest_n_request(
    bsm: BotoSesManager,
    instance_id: str,
    character: str,
    locale: str,
    n: int,
) -> T.List[quest.EnrichedQuestData]:
    command_invocations = aws_ssm_run_command.better_boto.run_shell_script_sync(
        ssm_client=bsm.ssm_client,
        commands=[
            (
                f"{path_acore_db_app_cli} "
                f"quest get-latest-n-quest --char {character} --locale {locale} --n {n}"
            ),
        ],
        instance_ids=instance_id,
        delays=1,
        timeout=10,
    )
    enriched_quest_data_list = [
        quest.EnrichedQuestData(**dct)
        for dct in json.loads(command_invocations[0].StandardOutputContent)
    ]
    return enriched_quest_data_list

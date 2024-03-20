from typing import Any

from pydantic import BaseModel, Field, validator

from shared import settings


class BrownieAtelierHttpTriggerInput(BaseModel):
    """
    BrownieAtelierHttpTriggerの起動に必要な引数のチェックを行う。
    ・target_container: 指定がない場合、Autoをデフォルトとする。
    ・container_controll_command: 指定がない場合、stopをデフォルトとする。
    """

    target_container: str = Field(
        default=settings.TARGET_CONTAINER__AUTO, title="対象コンテナー"
    )
    container_controll_command: str = Field(
        default=settings.CONTAINER_CONTROLL__STOP,
        title="コンテナーコントロールコマンド",
    )

    def __init__(self, **data: Any):
        super().__init__(**data)

    """
    定義順にチェックされる。
    valuesにはチェック済みの値のみが入るため順序は重要。(単項目チェック、関連項目チェックの順で定義するのが良さそう。)
    """

    ##################################
    # 単項目チェック
    ##################################
    @validator("target_container")
    def target_container_check(cls, value: str, values: dict) -> str:
        if value:
            assert isinstance(value, str), "文字列型以外がエラー"

            if value not in settings.TARGET_CONTAINER_LIST:
                raise ValueError(
                    f"""対象コンテナーの指定ミス。
                        {', '.join(settings.TARGET_CONTAINER_LIST)},
                        で入力してください。"""
                )

        return value

    @validator("container_controll_command")
    def container_controll_command_check(cls, value: str, values: dict) -> str:
        if value:
            assert isinstance(value, str), "文字列型以外がエラー"

            if value not in settings.CONTAINER_CONTROLL_LIST:
                raise ValueError(
                    f"""コンテナーコントロールコマンドの指定ミス。
                        {', '.join(settings.CONTAINER_CONTROLL_LIST)}
                        で入力してください。"""
                )

        return value

    ###################################
    # 関連項目チェック
    ###################################

    #####################################
    # カスタマイズデータ
    #####################################

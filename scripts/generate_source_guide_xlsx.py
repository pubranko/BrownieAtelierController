from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


OUTPUT_PATH = Path("docs/source-guide.xlsx")


@dataclass(frozen=True)
class Sheet:
    name: str
    rows: list[list[str]]
    widths: list[int]
    title: str | None = None


def xml_escape(value: object) -> str:
    return escape(str(value), {'"': "&quot;"})


def col_name(index: int) -> str:
    name = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def cell_ref(row: int, col: int) -> str:
    return f"{col_name(col)}{row}"


def sheet_quoted(name: str) -> str:
    return "'" + name.replace("'", "''") + "'"


def inline_cell(row: int, col: int, value: str, style: int = 1) -> str:
    ref = cell_ref(row, col)
    text = xml_escape(value)
    return (
        f'<c r="{ref}" t="inlineStr" s="{style}">'
        f"<is><t>{text}</t></is>"
        "</c>"
    )


def rows_xml(rows: list[list[str]], start_row: int) -> str:
    xml_rows: list[str] = []
    for offset, row_values in enumerate(rows):
        row_number = start_row + offset
        style = 2 if offset == 0 else 1
        cells = "".join(
            inline_cell(row_number, col_index, value, style)
            for col_index, value in enumerate(row_values, start=1)
        )
        xml_rows.append(f'<row r="{row_number}" ht="24" customHeight="1">{cells}</row>')
    return "".join(xml_rows)


def hyperlink_xml(ref: str, location: str, display: str) -> str:
    return (
        f'<hyperlink ref="{ref}" location="{xml_escape(location)}" '
        f'display="{xml_escape(display)}"/>'
    )


def worksheet_xml(sheet: Sheet, is_main: bool, sheet_names: list[str]) -> str:
    max_cols = max((len(row) for row in sheet.rows), default=1)
    cols = "".join(
        f'<col min="{index}" max="{index}" width="{width}" customWidth="1"/>'
        for index, width in enumerate(sheet.widths[:max_cols], start=1)
    )

    row_parts: list[str] = []
    hyperlinks: list[str] = []

    if is_main:
        row_parts.append(
            '<row r="1" ht="30" customHeight="1">'
            + inline_cell(1, 1, "Brownie Atelier Controller ソース解説資料", 4)
            + "</row>"
        )
        start_row = 3
        for row_number, row in enumerate(sheet.rows, start=start_row):
            style = 2 if row_number == start_row else 1
            cells: list[str] = []
            for col_index, value in enumerate(row, start=1):
                cell_style = 3 if col_index == 1 and row_number > start_row else style
                cells.append(inline_cell(row_number, col_index, value, cell_style))
            row_parts.append(
                f'<row r="{row_number}" ht="24" customHeight="1">'
                + "".join(cells)
                + "</row>"
            )
            if row_number > start_row and row and row[0] in sheet_names:
                hyperlinks.append(
                    hyperlink_xml(
                        cell_ref(row_number, 1),
                        f"{sheet_quoted(row[0])}!A1",
                        row[0],
                    )
                )
        freeze = (
            '<sheetViews><sheetView workbookViewId="0">'
            '<pane ySplit="2" topLeftCell="A3" activePane="bottomLeft" state="frozen"/>'
            '<selection pane="bottomLeft"/>'
            "</sheetView></sheetViews>"
        )
    else:
        row_parts.append(
            '<row r="1" ht="24" customHeight="1">'
            + inline_cell(1, 1, "← 目次へ戻る", 3)
            + "</row>"
        )
        hyperlinks.append(hyperlink_xml("A1", f"{sheet_quoted('目次')}!A1", "← 目次へ戻る"))
        row_parts.append(
            '<row r="2" ht="30" customHeight="1">'
            + inline_cell(2, 1, sheet.title or sheet.name, 4)
            + "</row>"
        )
        row_parts.append('<row r="3" ht="10" customHeight="1"></row>')
        row_parts.append(rows_xml(sheet.rows, 4))
        freeze = (
            '<sheetViews><sheetView workbookViewId="0">'
            '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
            '<selection pane="bottomLeft"/>'
            "</sheetView></sheetViews>"
        )

    hyperlinks_part = f"<hyperlinks>{''.join(hyperlinks)}</hyperlinks>" if hyperlinks else ""
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f"{freeze}"
        f"<cols>{cols}</cols>"
        f"<sheetData>{''.join(row_parts)}</sheetData>"
        f"{hyperlinks_part}"
        '<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>'
        "</worksheet>"
    )


def workbook_xml(sheets: list[Sheet]) -> str:
    sheet_entries = "".join(
        f'<sheet name="{xml_escape(sheet.name)}" sheetId="{index}" r:id="rId{index}"/>'
        for index, sheet in enumerate(sheets, start=1)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        "<bookViews><workbookView/></bookViews>"
        f"<sheets>{sheet_entries}</sheets>"
        "</workbook>"
    )


def workbook_rels_xml(sheets: list[Sheet]) -> str:
    rels = [
        f'<Relationship Id="rId{index}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
        f'Target="worksheets/sheet{index}.xml"/>'
        for index, _ in enumerate(sheets, start=1)
    ]
    rels.append(
        '<Relationship Id="rIdStyles" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
        'Target="styles.xml"/>'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(rels)
        + "</Relationships>"
    )


def content_types_xml(sheet_count: int) -> str:
    sheets = "".join(
        f'<Override PartName="/xl/worksheets/sheet{index}.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for index in range(1, sheet_count + 1)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/styles.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        + sheets
        + "</Types>"
    )


def styles_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="4">
    <font><sz val="11"/><name val="Yu Gothic"/></font>
    <font><sz val="11"/><name val="Yu Gothic"/></font>
    <font><b/><sz val="11"/><name val="Yu Gothic"/></font>
    <font><u/><color rgb="FF0563C1"/><sz val="11"/><name val="Yu Gothic"/></font>
  </fonts>
  <fills count="4">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFD9EAF7"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1F4E79"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border><left style="thin"><color rgb="FFBFBFBF"/></left><right style="thin"><color rgb="FFBFBFBF"/></right><top style="thin"><color rgb="FFBFBFBF"/></top><bottom style="thin"><color rgb="FFBFBFBF"/></bottom><diagonal/></border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="5">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="0" borderId="1" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="2" fillId="2" borderId="1" xfId="0" applyFill="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="3" fillId="0" borderId="1" xfId="0" applyFont="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="2" fillId="3" borderId="0" xfId="0" applyFill="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/><protection locked="0"/></xf>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>"""


def root_rels_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""


def app_xml(sheet_names: Iterable[str]) -> str:
    names = "".join(f"<vt:lpstr>{xml_escape(name)}</vt:lpstr>" for name in sheet_names)
    count = len(list(sheet_names)) if not isinstance(sheet_names, list) else len(sheet_names)
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        "<Application>Codex</Application>"
        "<HeadingPairs><vt:vector size=\"2\" baseType=\"variant\"><vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant>"
        f"<vt:variant><vt:i4>{count}</vt:i4></vt:variant></vt:vector></HeadingPairs>"
        f"<TitlesOfParts><vt:vector size=\"{count}\" baseType=\"lpstr\">{names}</vt:vector></TitlesOfParts>"
        "</Properties>"
    )


def core_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Brownie Atelier Controller ソース解説資料</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">2026-05-29T00:00:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2026-05-29T00:00:00Z</dcterms:modified>
</cp:coreProperties>"""


def build_sheets() -> list[Sheet]:
    directory_rows = [
        ["ディレクトリ/ファイル", "役割", "主なファイル", "関連リソース/補足"],
        ["BrownieAtelierHttpTrigger", "HTTP POST で ACI の作成・起動・停止・削除などを手動実行する関数", "__init__.py / function.json / brownie_atelier_http_trigger_input.py", "target_container と container_controll_command を Pydantic で検証"],
        ["BrownieAtelierTimerTrigger", "Timer Trigger で定期的に自動実行用 ACI を作成する関数", "__init__.py / function.json", "schedule は %TIMER_TRIGGER_SCHEDULE%"],
        ["BrownieAtelierBlobTrigger", "停止指示 Blob を契機に ACI を削除する関数", "__init__.py / function.json", "brownie-atelier/container-stop-coomand-execute を監視"],
        ["shared", "Azure SDK クライアント取得、ACI 状態確認、ACI 操作、設定値を集約", "settings.py / command_execution.py / container_status_check.py / resource_client_get.py", "各 Trigger から呼び出される中核処理"],
        ["BrownieAtelierStorage", "Git Submodule 化された Azure Storage 操作用の共通部品", "settings.py / models/*.py", "Blob/File/Queue の汎用モデル。具体的な利用方法はメインモジュール側で決まる"],
        ["terraform", "Azure リソースの IaC 定義", "environments/product / environments/test / scripts", "Function App、Storage、App Insights、Service Plan など"],
        ["tests", "手動実行に近い確認用スクリプトと一部テスト", "test_http_trigger.py / test_container_status.py / test_settings.py", "Azure 実リソースや環境変数に依存するものがある"],
        ["scripts", "GitHub Actions 環境変数や Terraform 実行の補助", "generate-github-env-files.sh / set-github-env-vars.sh / terraform-run.sh", "運用補助スクリプト"],
        ["docs", "生成した図・資料の置き場", "system-overview.drawio / source-guide.xlsx", "本 Excel はたたき台"],
    ]

    function_rows = [
        ["Function", "Trigger種別", "発火条件/入力", "主な処理", "操作対象", "関連ファイル"],
        ["BrownieAtelierTimerTrigger", "timerTrigger", "%TIMER_TRIGGER_SCHEDULE%", "Resource Group 取得、ACI 状態確認、manual mode 確認、存在しない場合に create", "BrownieAtelierMongo / BrownieAtelierNewsCrawler", "BrownieAtelierTimerTrigger/__init__.py"],
        ["BrownieAtelierHttpTrigger", "httpTrigger", "POST。body: target_container, container_controll_command", "入力検証、ACI 状態確認、manual mode 更新、指定コマンド実行", "Auto / BrownieAtelierMongo / BrownieAtelierNewsCrawler / BrownieAtelierNewsCrawlerManual", "BrownieAtelierHttpTrigger/__init__.py"],
        ["BrownieAtelierBlobTrigger", "blobTrigger", "brownie-atelier/container-stop-coomand-execute の Blob 作成/更新", "ACI 状態確認、manual mode 確認、Mongo と NewsCrawler を delete", "BrownieAtelierMongo / BrownieAtelierNewsCrawler", "BrownieAtelierBlobTrigger/__init__.py"],
        ["共通", "Azure SDK", "DefaultAzureCredential", "ResourceManagementClient と ContainerInstanceManagementClient を使う", "Azure Resource Group / ACI", "shared/resource_client_get.py"],
    ]

    shared_rows = [
        ["ファイル", "関数/定義", "役割", "呼び出し元", "注意点"],
        ["shared/settings.py", "環境変数・定数", "Azure、Docker Registry、Mongo、NewsCrawler、制御コマンド、対象コンテナーを定義", "全 Trigger / ACI 定義", "秘密情報を含む設定は環境変数から取得"],
        ["shared/resource_client_get.py", "resource_client_get", "DefaultAzureCredential で ResourceManagementClient を作成し、Resource Group へアクセスできるか確認", "各 Trigger", "Resource Group が無い場合は例外"],
        ["shared/container_status_check.py", "container_status_check", "ACI Container Group の instance_view.state を取得。404 の場合は空文字を返す", "各 Trigger", "空文字はコンテナー未存在を意味する"],
        ["shared/command_execution.py", "command_execution", "create/restart/start/stop/delete を ContainerInstanceManagementClient で実行", "各 Trigger", "create は既存 state があると中止、delete は state が無いと中止"],
        ["shared/brownie_atelier_mongo_settings.py", "CONTAINER_GROUP", "Mongo 用 ContainerGroup 定義、Volume、環境変数、公開 DNS/Port を定義", "Timer/HTTP/Blob", "Azure Files を複数マウント"],
        ["shared/brownie_atelier_news_crawler_settings.py", "CONTAINER_GROUP__AUTO / MANUAL", "NewsCrawler 用 ContainerGroup 定義、Docker Hub イメージ、環境変数、Volume を定義", "Timer/HTTP/Blob", "Auto と Manual で ContainerGroup を分ける"],
    ]

    storage_rows = [
        ["種別", "クラス/ファイル", "共通部品としての役割", "このアプリでの使い方", "主な設定値"],
        ["前提", "BrownieAtelierStorage", "Git Submodule 化された Azure Storage 操作用の共通部品", "このリポジトリではメインモジュール側の Function/ACI 定義から呼び出して利用する", "BrownieAtelierStorage/settings.py"],
        ["Azure Blob", "ControllerBlobModel", "Blob コンテナー/Blob ファイルの作成・削除・ダウンロードを扱うモデル", "NewsCrawler 側が停止指示 Blob を作成し、BrownieAtelierBlobTrigger の発火契機にする想定", "AZURE_STORAGE__CONNECTION_STRING / AZURE_STORAGE__BLOB_CONTAINER_NAME / AZURE_STORAGE__BLOB_FILE_NAME"],
        ["Azure Files", "ControllerFileModel", "File Share 上のファイルをアップロード/ダウンロードするモデル", "controller/mongo_mode を使い、Mongo の manual mode フラグを on/off 管理する", "AZURE_STORAGE__CONNECTION_STRING / AZURE_STORAGE__FILE_SHARE"],
        ["Azure Queue", "ControllerQueModel", "Queue の作成・削除・送信・受信・peek を扱うモデル", "共通部品として利用可能。現時点の主要 Function では直接利用していない", "AZURE_STORAGE__CONNECTION_STRING / AZURE_STORAGE__QUE_NAME"],
    ]

    aci_rows = [
        ["ContainerGroup", "コンテナー名", "Dockerイメージ", "起動コマンド", "Volume Mount", "Restart Policy", "備考"],
        ["BrownieAtelierMongo", "mongo", "mongo:{CONTAINER_MONGO__MONGO_TAG}", "sleep 5 && mongod --config {mongo_conf_path}", "/data/db, /etc/mongo-conf, /etc/mongo-key, /var/log/mongodb, /docker-entrypoint-initdb.d", "Never", "Public DNS と 27017/tcp を設定。Azure Files Volume 定義は shared/brownie_atelier_mongo_settings.py にある"],
        ["BrownieAtelierNewsCrawler", "brownie-atelier-news-crawler-auto", "docker.io/{user}/brownie-atelier-news-crawler:{tag}", "sleep 5 && {CONTAINER_NEWS_CRAWLER__CONTAINER_START_COMMAND}", "data, mongo-key", "Never", "Timer/Auto 操作用。Azure Files Volume 定義は shared/brownie_atelier_news_crawler_settings.py にある"],
        ["BrownieAtelierNewsCrawlerManual", "brownie-atelier-news-crawler-manual", "docker.io/{user}/brownie-atelier-news-crawler:{tag}", "sleep 5 && {CONTAINER_NEWS_CRAWLER__CONTAINER_START_COMMAND}", "data, mongo-key", "Never", "HTTP 手動操作用。Azure Files Volume 定義は shared/brownie_atelier_news_crawler_settings.py にある"],
    ]

    settings_rows = [
        ["分類", "設定値", "用途", "デフォルト/例", "秘密情報"],
        ["Azure", "AZURE_SUBSCRIPTION_ID", "Azure SDK の subscription_id", "環境変数必須", "いいえ"],
        ["Azure", "AZURE_RESOURCE_GROUP_NAME", "操作対象 Resource Group", "環境変数必須", "いいえ"],
        ["Azure", "AZURE_LOCATION", "ACI/リソース作成リージョン", "環境変数必須", "いいえ"],
        ["Docker", "ACI_DOCKER_IMAGE__REGISTRY_SERVER", "Docker Registry Server", "docker.io", "いいえ"],
        ["Docker", "ACI_DOCKER_IMAGE__REGISTRY_USERNAME", "Docker Registry Username", "環境変数必須", "はい"],
        ["Docker", "ACI_DOCKER_IMAGE__REGISTRY_PASSWORD", "Docker Registry Password", "環境変数必須", "はい"],
        ["Mongo", "CONTAINER_MONGO__CONTAINER_GROUP_NAME", "Mongo ACI 名", "BrownieAtelierMongo", "いいえ"],
        ["Mongo", "CONTAINER_MONGO__MONGO_INITDB_ROOT_USERNAME/PASSWORD", "Mongo root 認証情報", "環境変数必須", "はい"],
        ["Crawler", "CONTAINER_NEWS_CRAWLER__CONTAINER_GROUP_NAME", "自動操作版 Crawler ACI 名", "BrownieAtelierNewsCrawler", "いいえ"],
        ["Crawler", "CONTAINER_NEWS_CRAWLER__CONTAINER_GROUP_NAME__MANUAL", "手動操作版 Crawler ACI 名", "BrownieAtelierNewsCrawlerManual", "いいえ"],
        ["Storage", "AZURE_STORAGE__CONNECTION_STRING", "Blob/File/Queue 接続", "環境変数", "はい"],
        ["Storage", "AZURE_STORAGE__BLOB_CONTAINER_NAME", "停止指示 Blob のコンテナー", "brownie-atelier", "いいえ"],
        ["Storage", "AZURE_STORAGE__BLOB_FILE_NAME", "停止指示 Blob 名", "container-stop-coomand-execute", "いいえ"],
        ["制御", "CONTAINER_CONTROLL_LIST", "HTTP で受け付ける操作", "create/start/restart/stop/delete", "いいえ"],
        ["制御", "TARGET_CONTAINER_LIST", "HTTP で受け付ける対象", "Auto/Mongo/NewsCrawler/Manual", "いいえ"],
    ]

    terraform_rows = [
        ["環境/場所", "主なリソース", "管理対象", "備考"],
        ["terraform/environments/product", "Resource Group、brownieatelierdatawest、brownieatelierwest3、Flex Consumption Function App、Application Insights", "本番/West3 用基盤", "app_settings は GitHub Actions 管理で Terraform は ignore_changes"],
        ["terraform/environments/test", "Resource Group、brownieatelierdata、brownieatelierfunctest、Linux Function App、Application Insights、Service Plan", "テスト/既存環境の基盤", "backend key は test.tfstate"],
        ["terraform backend", "BrownieAtelierTerraformStateRG / brownieateliertfstate / tfstate", "Terraform state", "product.tfstate / test.tfstate"],
        ["terraform/scripts", "import 系スクリプト、state から west3 を外す手順メモ", "既存リソース取り込み・state 整理", "実行前に対象環境を要確認"],
    ]

    flow_rows = [
        ["フロー", "ステップ", "概要", "関連ファイル"],
        ["Timer 定期起動", "1", "Timer Trigger がスケジュールで発火", "BrownieAtelierTimerTrigger/function.json"],
        ["Timer 定期起動", "2", "Resource Group 取得、Mongo/NewsCrawler の ACI 状態確認", "resource_client_get.py / container_status_check.py"],
        ["Timer 定期起動", "3", "manual mode が off なら Mongo を create。NewsCrawler が存在しなければ create", "BrownieAtelierTimerTrigger/__init__.py"],
        ["HTTP 手動操作", "1", "POST Body を Pydantic で検証", "brownie_atelier_http_trigger_input.py"],
        ["HTTP 手動操作", "2", "target_container と command に応じて ACI を操作", "BrownieAtelierHttpTrigger/__init__.py"],
        ["HTTP 手動操作", "3", "Mongo 手動 create/start/restart で manual mode on、delete/stop で off", "ControllerFileModel"],
        ["Blob 自動削除", "1", "NewsCrawler 側が停止指示 Blob を作成", "ControllerBlobModel / コンテナー側アプリ"],
        ["Blob 自動削除", "2", "Blob Trigger が発火し、manual mode 確認後に Mongo と NewsCrawler を delete", "BrownieAtelierBlobTrigger/__init__.py"],
    ]

    tests_rows = [
        ["ファイル", "目的", "実行形態", "注意点"],
        ["tests/test_http_trigger.py", "HTTP Trigger を実際に呼び出す確認用スクリプト", "python 実行", "MSAL、Function URL/Key、Azure AD 設定が必要"],
        ["tests/test_container_status.py", "ACI の状態確認関数を実リソースに対して確認", "python 実行", "Azure 認証と Resource Group が必要"],
        ["tests/test_resource_client_get.py", "ResourceManagementClient 取得の確認", "pytest または python 実行想定", "環境変数と Azure 認証に依存"],
        ["tests/test_settings.py", "settings の読み込み確認", "pytest 想定", "環境変数不足に注意"],
        ["BrownieAtelierStorage/test_tools", "Blob/File/Queue モデルの手動確認", "python 実行", "実 Storage への接続文字列が必要"],
    ]

    todo_rows = [
        ["確認項目", "補正メモ", "優先度"],
        ["ControllerFileModel.mode_check の exists 判定", "現在の実装コメントと if/else の意味が逆に見えるため、実動作を確認したい", "高"],
        ["Blob 名の typo", "container-stop-coomand-execute は既存設定に合わせて記載。意図した名称か確認", "中"],
        ["BrownieAtelierStorage の説明粒度", "Git Submodule の共通部品として説明し、個別アプリ固有の使い方はメインモジュール側の呼び出し元で説明する", "中"],
        ["Terraform product/test の差分", "本番は Flex Consumption、test は Linux Function App。移行中か運用方針を追記", "中"],
        ["HTTP Trigger のレスポンス文言", "stop/delete でも「起動しました」と返る箇所があるため必要なら補正", "低"],
    ]

    sheet_names = [
        "ディレクトリ構成",
        "Function一覧",
        "shared処理",
        "Storage関連",
        "ACIコンテナー定義",
        "設定値一覧",
        "Terraform構成",
        "処理フロー",
        "テスト関連",
        "TODO手補正メモ",
    ]
    contents_rows = [
        ["シート名", "概要", "おすすめ確認ポイント"],
        ["ディレクトリ構成", "リポジトリ全体のフォルダ・ファイルの役割一覧", "まず全体像を掴む"],
        ["Function一覧", "Timer/HTTP/Blob Trigger の責務と入力・操作対象", "Azure Functions の入口を確認"],
        ["shared処理", "共通処理と ACI 操作ロジックの説明", "command_execution と status_check を確認"],
        ["Storage関連", "Blob/File/Queue と manual mode の整理", "自動削除と手動モードの関係を確認"],
        ["ACIコンテナー定義", "Mongo / NewsCrawler の ContainerGroup 定義", "Docker image、volume、起動コマンドを確認"],
        ["設定値一覧", "主要な環境変数とデフォルト値・秘密情報区分", "GitHub Actions の環境変数と照合"],
        ["Terraform構成", "product/test の IaC 管理範囲", "Terraform 管理と Actions 管理の境界を確認"],
        ["処理フロー", "Timer/HTTP/Blob の実行順序", "draw.io 図と照らし合わせる"],
        ["テスト関連", "テスト・手動確認スクリプトの用途", "実 Azure 依存の有無を確認"],
        ["TODO手補正メモ", "AI 生成後に人手で補正したい論点", "レビュー時のチェックリストにする"],
    ]

    return [
        Sheet("目次", contents_rows, [28, 70, 70], "目次"),
        Sheet("ディレクトリ構成", directory_rows, [34, 58, 54, 62], "ディレクトリ構成"),
        Sheet("Function一覧", function_rows, [32, 18, 54, 64, 58, 48], "Function一覧"),
        Sheet("shared処理", shared_rows, [40, 36, 64, 46, 60], "shared処理"),
        Sheet("Storage関連", storage_rows, [22, 36, 56, 56, 62], "Storage関連"),
        Sheet("ACIコンテナー定義", aci_rows, [34, 36, 56, 58, 62, 18, 46], "ACIコンテナー定義"),
        Sheet("設定値一覧", settings_rows, [18, 48, 58, 48, 14], "設定値一覧"),
        Sheet("Terraform構成", terraform_rows, [34, 78, 52, 64], "Terraform構成"),
        Sheet("処理フロー", flow_rows, [24, 12, 82, 54], "処理フロー"),
        Sheet("テスト関連", tests_rows, [42, 58, 28, 64], "テスト関連"),
        Sheet("TODO手補正メモ", todo_rows, [48, 86, 16], "TODO手補正メモ"),
    ]


def write_xlsx(sheets: list[Sheet]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    sheet_names = [sheet.name for sheet in sheets]
    with ZipFile(OUTPUT_PATH, "w", ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types_xml(len(sheets)))
        archive.writestr("_rels/.rels", root_rels_xml())
        archive.writestr("docProps/core.xml", core_xml())
        archive.writestr("docProps/app.xml", app_xml(sheet_names))
        archive.writestr("xl/workbook.xml", workbook_xml(sheets))
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml(sheets))
        archive.writestr("xl/styles.xml", styles_xml())
        for index, sheet in enumerate(sheets, start=1):
            archive.writestr(
                f"xl/worksheets/sheet{index}.xml",
                worksheet_xml(sheet, is_main=(index == 1), sheet_names=sheet_names),
            )


if __name__ == "__main__":
    write_xlsx(build_sheets())
    print(f"created: {OUTPUT_PATH}")

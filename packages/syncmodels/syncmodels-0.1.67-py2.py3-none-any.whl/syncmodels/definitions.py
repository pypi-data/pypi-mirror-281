import re
from enum import Enum
from typing import NewType

# from .models import (
#     BudgetTypeEnum,
#     TravelPartyCompositionEnum,
# )

DEFAULT_LANGUAGE = "es"

MODEL_TABLE = "model"

UID_TYPE = str

# TODO: reallocate
UID = NewType("UID", str)
QUERY = NewType("QUERY", dict)

URI = NewType("URI", str)
DURI = NewType("DURI", dict)

WAVE = NewType("WAVE", int)
JSON = NewType("JSON", dict)
QUERY = NewType("QUERY", dict)


# ----------------------------------------------------------
# common keys
# ----------------------------------------------------------
# public call_kw | data keys
KIND_KEY = "kind__"
BODY_KEY = "body"
PATH_KEY = "path"

# reserved and private keys
METHOD_KEY = "method__"
FUNC_KEY = "func__"
FILTERS_KEY = "filters__"

CRAWLER_KEY = "crawler__"
BOT_KEY = "bot__"

MONOTONIC_KEY = "wave__"
MONOTONIC_SINCE = "since__"
MONOTONIC_SINCE_KEY = "since_key__"
MONOTONIC_SINCE_VALUE = "since_value__"
ID_KEY = "id"
ORG_KEY = "id__"
FORCE_SAVE = "__save"
REG_PRIVATE_KEY = r".*__$"


# ----------------------------------------------------------
# fqid helpers
# ----------------------------------------------------------

# split table:uid from fqid
# TODO: get until ":"
REG_FQID = r"((?P<table>\w+):)?(?P<uid>\w+)$"

REG_SPLIT_ID = re.compile(
    """(?imsx)
    ^
    (?P<thing>[^:]+)(:(?P<id>[^:]+))?$
    """
)
REG_SPLIT_ID = re.compile(
    """(?imsx)
    ^
    (?P<thing>[^:]+)(:(?P<id>.+))?$
    """
)
# REG_SPLIT_PATH = re.compile(
#     r"(?P<path>(?P<_path>.*?)[/:](?P<id>[^/:?#]*))(\?(?P<query>[^#]*))?(\#(?P<fragment>.*))?$"
# )
REG_SPLIT_PATH = re.compile(
    """(?imsx)
^
(?P<xpath>
 (?P<path>
  (?P<_path>
    (?P<basename>
      (?P<table>[^/:]+)
      [/:]
      (?P<id>[^/:?#]*)
    )
  )
 )
)
(
  \?
  (?P<query>[^#]*)
)?
  (\#(?P<fragment>.*))?
$
"""
)


def build_fqid(fqid, table=""):
    m = re.match(REG_FQID, str(fqid))
    if m:
        d = m.groupdict(default=table)
        return "{table}:{uid}".format_map(d)
    return table, fqid


def filter_4_compare(data, table=""):
    """Filter data to be used for comparison"""
    if data:
        result = {
            key: value
            for key, value in data.items()
            if not re.match(REG_PRIVATE_KEY, key)
        }
        # check id:
        uid = result.get("id")
        if uid is not None:
            result["id"] = build_fqid(str(uid))
    else:
        result = {}

    return result

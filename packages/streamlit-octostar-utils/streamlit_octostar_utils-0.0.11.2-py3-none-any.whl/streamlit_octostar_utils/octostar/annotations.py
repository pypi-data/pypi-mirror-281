from typing import Union, List, Literal, Dict, Optional, Callable, Any
from copy import deepcopy, copy
import functools
from pydantic import BaseModel
import uuid
import itertools
import json

import datetime as dt
import time
from dateutil import parser as dt_parser

def now():
    return dt.datetime.fromtimestamp(time.time(), dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def string_to_unix(datetime_str):
    return dt_parser.parse(datetime_str or dt.datetime.fromtimestamp(0, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

def unix_to_string(timestamp_unix):
    return dt.datetime.fromtimestamp(timestamp_unix or 0, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def recursive_update_dict(
    d1: dict,
    d2: dict,
    op: Callable[[Any, Any], Any],
    recurse: bool = True
) -> dict:
    if not isinstance(d1, dict) or not isinstance(d2, dict):
        if d1 is None:
            return d2
        elif d2 is None:
            return d1
        else:
            return op(d1, d2)
    for k2, v2 in d2.items():
        if isinstance(v2, dict):
            v1 = d1.get(k2, {})
            if isinstance(v1, dict):
                if recurse:
                    if isinstance(recurse, int):
                        recurse -= 1
                    d1[k2] = recursive_update_dict(v1, v2, op, recurse)
                else:
                    d1[k2] = op(v1, v2)
            else:
                if k2 in d1:
                    d1[k2] = op(v1, v2)
                else:
                    d1[k2] = v2
        else:
            if k2 in d1:
                d1[k2] = op(d1[k2], v2)
            else:
                d1[k2] = v2
    return d1

def travel_dict(
    d: dict,
    keylist: List[str],
    mode: Literal['r', 'w'] = 'r',
    strict: bool = False
) -> Union[Any, callable]:
    def __set(pointer, key, value):
        pointer[key] = value    
    pointer = d
    match mode:
        case 'w':
            for key in keylist[:-1]:
                if key not in pointer:
                    if strict:
                        raise KeyError(key)
                    pointer[key] = dict()
                pointer = pointer[key]
            return lambda v: __set(pointer, key, v)
        case 'r':
            for key in keylist:
                if not hasattr(pointer, "__contains__"):
                    if strict:
                        raise KeyError(key)
                    return pointer
                else:
                    if key not in pointer:
                        if strict:
                            raise KeyError(key)
                        return pointer
                    else:
                        pointer = pointer[key]
            return pointer                 


import os
os.environ["OS_API_ENDPOINT"] = 'https://1054.pr.dev.octostar.com/'
os.environ["OS_JWT"] = \
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJpZCI6MTgsInVzZXJuYW1lIjoidi50b25lbGxpIiwiZW1haWwiOiJ2LnRvbmVsbGlAb2N0b3N0YXIuY29tIiwicm9sZXMiOlsiQWRtaW4iXSwidGltYnJfdG9rZW5fZW5jIjoiMDQxMzIwOGJmYmFkYzM3ZDg4NmUwOTc3ZDlkM2Y2ZjU2MmFhM2M1Y2M2NDVjYjUzMzExMDkwMWM0YjQxMThmMzBiMDM0ZmRhMzRmZDg1YzJmZGY3OGQ5Y2Y1YmFiMjRjNjJjNjQzY2JkZmZhZjA3MGZiMWQ2MTUwNjkyZjY5NWJjOTA3YThiNDc1NWQ2MmRkZmMwMjRkZWRhYWY2ZGE1NjM0MTRmZDBiYWZlZTU5OTIxNDlkZGU5NzZiOThhZmJmOGJkNTA4NWIyYjA1MWFhZjI3MmYyMDdmODYwZDYxZGFlZWM3NjM3YTk5ZGE5NTIyYzY1ZjQ3OGI4NzBmMDg0MzU3NTNkOGZmYzdmNjM1NmU4ZGNjNjczY2YwOTZlYzI2ZTBkOWI2OGIzMmFkNDY2NzE5OWJkZTJmNGM1MDlmOTVhOGNlMTExMSIsImFzeW5jX2NoYW5uZWwiOiJhYjFjN2E5My00MTk4LTQyOTgtYjJjYS0wMjlmOTA0OGRiZjUiLCJzdWIiOjE4LCJpYXQiOjE3MTg4MTE4ODAsImV4cCI6MTcxODg5ODI4MCwiaXNzIjoib2N0b3N0YXJfcGxhdGZvcm0ifQ.e43x-3xWXBcRImJ6fQ7wbwXBRjz0MevaCVJdHcqhvxPBkdRAB41TpwT5Xgg4bBCdXWi06VMlYtLMIwkSSnPGIg"
os.environ["OS_USER"] = "v.tonelli"
os.environ["OS_ONTOLOGY"] = "os_ontology_v1"
from octostar.client import AuthenticatedClient, set_default_client
client = AuthenticatedClient(os.environ['OS_API_ENDPOINT'], os.environ['OS_JWT'], headers={
    "x-ontology": os.environ.get("OS_ONTOLOGY"),
})
set_default_client(client)

from octostar.utils.ontology import query_ontology
from octostar.utils.workspace import delete_entities, upsert_entities, write_attachment, read_attachment

ANNOTATION_UUID_RANDOM_CHARS = 16
ANNOTATION_CONCEPT_NAME = 'annotation'
ANNOTATION_RELATIONSHIP = ('annotated_with', 'annotation_of')
ANNOTATION_SOURCE_ENTITY_UID_PROP = 'source_entity_uid'
ANNOTATION_SOURCE_ENTITY_TYPE_PROP = 'source_entity_type'
ANNOTATION_PRODUCER_PROP = 'producer_name'
ANNOTATION_CONTENT_PROP = 'os_item_content'
NO_ATTACHMENT_CHAR_LIMIT = 5000

class NestedMergeParams(BaseModel):
    op: Optional[Callable[[Any, Any], Any]] = lambda v1, _: v1
    recurse: Optional[Union[int, bool]] = True
    fields: Optional[Dict[str, 'NestedMergeParams']] = {}
NestedMergeParams.model_rebuild()

def generate_annotation_uuid(
    entity_id: str,
    x: int = ANNOTATION_UUID_RANDOM_CHARS
) -> str:
    entity_id = uuid.UUID(entity_id).hex
    random_id = uuid.uuid4().hex
    combined_hex = entity_id[:x] + random_id[len(entity_id)-x:]
    return str(uuid.UUID(combined_hex))

def read_annotations(
    entity_id: List[str],
    producer_name: Union[Literal['all'], List[str]]='all',
    dotted_keylist: Optional[str] = None,
    last_timestamp: Optional[str] = None
) -> List[dict]:
    def _get_annotation_contents(annotation):
        if not annotation['os_has_attachment']:
            return annotation[ANNOTATION_CONTENT_PROP] or {}
        else:
            return json.loads(read_attachment.sync(annotation['os_workspace'], annotation['os_entity_uid'], decode=True)) or {}
    conditions = []
    entity_ids_str = ",".join(["'" + e + "'" for e in entity_id])
    conditions.append(f"`{ANNOTATION_SOURCE_ENTITY_UID_PROP}` IN ({entity_ids_str})")
    if producer_name != 'all':
        producer_name = ",".join(["'" + p + "'" for p in producer_name])
        conditions.append(f"`{ANNOTATION_PRODUCER_PROP}` IN ({producer_name})")
    if last_timestamp:
        conditions.append(f"`os_last_updated_at` >= '{last_timestamp}'")
    if conditions:
        conditions = "WHERE " + " AND ".join(conditions)
    annotation_records = query_ontology.sync(f"SELECT * FROM `dtimbr`.`{ANNOTATION_CONCEPT_NAME}` {conditions}")
    annotations = [{
            ANNOTATION_CONTENT_PROP: _get_annotation_contents(a),
            'os_entity_uid': a['source_entity_uid'],
            'os_last_updated_at': a['os_last_updated_at']
        } for a in annotation_records]
    if dotted_keylist:
        keylist = dotted_keylist.split(".")
        for annotation in annotations:
            try:
                annotation[ANNOTATION_CONTENT_PROP] = travel_dict(annotation[ANNOTATION_CONTENT_PROP], keylist, mode='r', strict=True)
            except KeyError:
                annotation[ANNOTATION_CONTENT_PROP] = dict()
    annotations = sorted(annotations, key=lambda x: x['os_entity_uid'])
    merged_annotations = dict()
    for uid, group in itertools.groupby(annotations, key=lambda x: x['os_entity_uid']):
        group = sorted(list(group), key=lambda x: string_to_unix(x['os_last_updated_at']))
        merged_annotations[uid] = merge_annotations(
            [a[ANNOTATION_CONTENT_PROP] for a in group],
            {'op': lambda _, v2: v2}
        )
    merged_annotations = [merged_annotations.get(uid) for uid in entity_id]
    return merged_annotations

def write_annotations(
    entity_id: List[str],
    entity_type: List[str],
    os_workspace: Union[List[str], str],
    producer_name: Union[str, List[str]],
    annotation: List[dict],
    overwrite: bool = True,
    annotation_id: Optional[List[Optional[str]]] = None
) -> Union[List[dict]]:
    if isinstance(producer_name, str):
        producer_name = [producer_name]
    if isinstance(os_workspace, str):
        os_workspace = [os_workspace]
    if not annotation_id:
        annotation_id = [generate_annotation_uuid(e) for e in entity_id]
    assert(len(annotation) == len(entity_id))
    assert(len(entity_id) == len(entity_type))
    assert(len(producer_name) == len(entity_id))
    assert(len(annotation_id) == len(entity_id))
    annotation_id = [uid or generate_annotation_uuid(entity_id[i]) for i, uid in enumerate(annotation_id)]
    if overwrite:
        select_query = f"SELECT `entity_id` FROM `dtimbr`.`{ANNOTATION_CONCEPT_NAME}` WHERE `{ANNOTATION_SOURCE_ENTITY_UID_PROP}` IN (" + '{entity_ids}' f") AND `{ANNOTATION_PRODUCER_PROP}`='" + '{producer_name}' + "'"
        sql_query = []
        entity_id = [e[1] for e in sorted(enumerate(entity_id), key=lambda e: producer_name[e[0]])]
        for producer, group in itertools.groupby(enumerate(entity_id), key=lambda e: producer_name[e[0]]):
            ids = ",".join(["'" + e[1] + "'" for e in group])
            sql_query.append(select_query.format(entity_ids=ids, producer_name=producer))
        annotation_records = query_ontology.sync(" UNION ALL ".join(sql_query))       
        annotation_ids = list(set([r['entity_id'] for r in annotation_records]))
        if annotation_records:
            delete_entities.sync(annotation_ids)
    annotation_id = [generate_annotation_uuid(e) for e in entity_id]
    as_attachment = [False]*len(annotation)
    for i, annot in enumerate(annotation):
        if len(json.dumps(annot)) > NO_ATTACHMENT_CHAR_LIMIT:
           as_attachment[i] = True
    upserted = upsert_entities.sync(os_workspace, [{
            'entity_type': ANNOTATION_CONCEPT_NAME,
            'os_entity_uid': annotation_id[i],
            'fields': {
                ANNOTATION_CONTENT_PROP: annotation[i] if not as_attachment[i] else None,
                ANNOTATION_PRODUCER_PROP: producer_name[i],
                ANNOTATION_SOURCE_ENTITY_UID_PROP: entity_id[i],
                ANNOTATION_SOURCE_ENTITY_TYPE_PROP: entity_type[i],
                'os_has_attachment': as_attachment[i]
            }
        } for i in range(len(entity_id))])
    for i, annot in enumerate(annotation):
        if as_attachment[i]:
            write_attachment.sync(
                os_workspace[i], annotation_id[i], ANNOTATION_CONCEPT_NAME, "application/json",
                json.dumps(annotation[i]).encode('utf-8'), 
            )
    return upserted

def merge_annotations(
    annotations: List[dict],
    merge_params: NestedMergeParams
) -> dict:
    if isinstance(merge_params, dict):
        merge_params = NestedMergeParams(**merge_params)
    def _recursive_merge_fields(d1, d2, params):
        params = params or {}
        op = params.op or (lambda v1, _: v1)
        recurse = params.recurse or True
        updated_d1 = recursive_update_dict(deepcopy(d1), d2, op, recurse)
        if not params.fields or not isinstance(d1, dict) or not isinstance(d2, dict):
            pass
        else:
            for k, v in params.fields.items():
                updated_d1[k] = _recursive_merge_fields(d1.get(k), d2.get(k), v)
        return updated_d1
    return functools.reduce(lambda d1, d2: _recursive_merge_fields(d1, d2, merge_params),
                            annotations, {})
    
annot = write_annotations(
    ['0f46f60b-6433-453e-b12b-e54d3c3724fd'],
    '05db01b0-c00d-4847-8ab3-bfef9c86b310',
    'test',
    [{
        'my_data': 'hello world!'*5000
    }]
)

annot = read_annotations(['0f46f60b-6433-453e-b12b-e54d3c3724fd'], ['test'], 'my_data')
print(annot)
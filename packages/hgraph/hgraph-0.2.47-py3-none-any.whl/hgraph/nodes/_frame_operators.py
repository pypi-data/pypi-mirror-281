from dataclasses import asdict
from datetime import date, datetime
from typing import Type, Dict

import polars as pl
from frozendict import frozendict

from hgraph import (
    compute_node,
    Frame,
    TS,
    SCHEMA,
    SCALAR,
    AUTO_RESOLVE,
    Series,
    COMPOUND_SCALAR,
    K,
    TSD,
    HgTypeMetaData,
    WiringContext,
    MissingInputsError,
    IncorrectTypeBinding,
    with_signature,
    TimeSeries,
    getitem_,
    getattr_,
    max_,
    min_,
    COMPOUND_SCALAR_1,
)

__all__ = (
    "frame_from_tsd_items",
    "frame_from_columns",
)


@compute_node
def frame_from_tsd_items(
    tsd: TSD[K, TS[COMPOUND_SCALAR]], mapping: Dict[str, str] = frozendict()
) -> TS[Frame[COMPOUND_SCALAR_1]]:
    data = []
    for k, v in tsd.valid_items():
        data.append(
            ({mapping["key"]: k} if "key" in mapping else {})
            | {
                mapping.get(k, k): v if isinstance(v, (bool, int, str, float, date, datetime)) else str(v)
                for k, v in asdict(v.value).items()
            }
        )

    return pl.DataFrame(data)


def frame_from_columns(cls: Type[COMPOUND_SCALAR], **kwargs) -> TS[SCALAR]:
    scalar_schema = cls.__meta_data_schema__
    kwargs_schema = {k: HgTypeMetaData.parse_value(v) for k, v in kwargs.items()}

    with WiringContext(current_signature=dict(signature=f"frame_from_columns({cls.__name__}, ...)")):
        for k, t in scalar_schema.items():
            if (kt := kwargs_schema.get(k)) is None:
                if getattr(cls, k, None) is None:
                    raise MissingInputsError(kwargs)
            elif not t.matches(kt if kt.is_scalar else kt.scalar_type().value_tp):
                raise IncorrectTypeBinding(t, kwargs_schema[k])

        @compute_node
        @with_signature(kwargs=kwargs_schema, return_annotation=TS[Frame[cls]])
        def from_ts_node(**kwargs):
            return cls(**{k: v if not isinstance(v, TimeSeries) else v.value for k, v in kwargs.items()})

        return from_ts_node(**kwargs)

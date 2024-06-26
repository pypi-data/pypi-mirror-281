# -*- encoding: utf-8 -*-
import dataclasses
from dataclasses import dataclass

__all__ = [
    "Options",
]


@dataclass(kw_only=True)
class Options:
    calculate_memory_size: bool = dataclasses.field(default=False, metadata=dict(description="Calculate Memory Size"))
    ignore_measurements: bool = dataclasses.field(default=True, metadata=dict(description="Ignore Measurements"))
    read_instance: bool = dataclasses.field(default=True, metadata=dict(description="Process Instance Label"))

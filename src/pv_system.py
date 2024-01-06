from typing import List

from attrs import define, field


@define
class PVPanelArea:
    panel_count: int
    square_meter_per_panel: float
    panel_efficiency: float
    horizontal_panel_angle_degrees: float
    directly_radiated: bool = field(default=True)


@define
class PVPanelGroup:
    name: str
    panel_areas: List[PVPanelArea]


@define
class PVSystem:
    name: str
    panel_groups: List[PVPanelGroup]

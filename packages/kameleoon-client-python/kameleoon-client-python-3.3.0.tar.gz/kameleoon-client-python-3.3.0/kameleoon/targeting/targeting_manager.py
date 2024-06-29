"""Targeting Segment"""

from typing import Optional
from kameleoon.data.manager.visitor import Visitor
from kameleoon.helpers.functions import enum_from_literal
from kameleoon.configuration.rule import Rule
from kameleoon.configuration.data_file import DataFile
from kameleoon.data.manager.visitor_manager import VisitorManager
from kameleoon.targeting.conditions.exclusive_feature_flag_condition import (
    ExclusiveFeatureFlagCondition,
)
from kameleoon.targeting.conditions.sdk_language_condition import SdkLanguageCondition
from kameleoon.sdk_version import SdkVersion
from kameleoon.targeting.conditions.segment_condition import SegmentCondition
from kameleoon.targeting.conditions.target_feature_flag_condition import (
    TargetFeatureFlagCondition,
)
from kameleoon.targeting.conditions.targeting_condition import TargetingConditionType


class TargetingManager:
    """Manager for check visitor is targeted for rule"""

    def __init__(self, visitor_manager: VisitorManager, data_file: DataFile) -> None:
        self.__visitor_manager = visitor_manager
        self.__data_file = data_file

    # pylint: disable=W0238
    def check_targeting(self, visitor_code: str, campaign_id: int, rule: Rule):
        """Check if visitor is targeted for rule"""
        segment = rule.targeting_segment
        if segment is None:
            return True
        visitor = self.__visitor_manager.get_visitor(visitor_code)
        return segment.check_tree(lambda type: self.__get_condition_data(type, visitor, visitor_code, campaign_id))

    # pylint: disable=R0911
    def __get_condition_data(
        self,
        condition_type_literal: str,
        visitor: Optional[Visitor],
        visitor_code: str,
        campaign_id: int,
    ):
        # pylint: disable=E1101,W0212
        condition_type = enum_from_literal(
            condition_type_literal,
            TargetingConditionType,
            TargetingConditionType.UNKNOWN,
        )
        if visitor:
            condition_data = self.__get_condition_data_by_type(visitor, condition_type)
            if condition_data is not None:
                return condition_data
        if condition_type == TargetingConditionType.SEGMENT:
            return SegmentCondition.SegmentInfo(
                self.__data_file,
                lambda type: self.__get_condition_data(type, visitor, visitor_code, campaign_id),
            )
        if condition_type == TargetingConditionType.EXCLUSIVE_FEATURE_FLAG:
            return ExclusiveFeatureFlagCondition.ExclusiveFeatureFlagInfo(
                campaign_id, {} if visitor is None else visitor.variations
            )
        if condition_type == TargetingConditionType.VISITOR_CODE:
            return visitor_code
        if condition_type == TargetingConditionType.SDK_LANGUAGE:
            return SdkLanguageCondition.SdkInfo(SdkVersion.NAME, SdkVersion.VERSION)
        return None

    def __get_condition_data_by_type(self, visitor: Visitor, condition_type: TargetingConditionType):
        if condition_type == TargetingConditionType.BROWSER:
            return visitor.browser
        if condition_type == TargetingConditionType.DEVICE_TYPE:
            return visitor.device
        if condition_type == TargetingConditionType.COOKIE:
            return visitor.cookie
        if condition_type == TargetingConditionType.GEOLOCATION:
            return visitor.geolocation
        if condition_type == TargetingConditionType.OPERATING_SYSTEM:
            return visitor.operating_system
        if condition_type == TargetingConditionType.CUSTOM_DATUM:
            return visitor.custom_data
        if condition_type == TargetingConditionType.CONVERSIONS:
            return visitor.conversions
        if condition_type in (
            TargetingConditionType.PAGE_URL,
            TargetingConditionType.PAGE_TITLE,
            TargetingConditionType.PAGE_VIEWS,
            TargetingConditionType.PREVIOUS_PAGE,
        ):
            return visitor.page_view_visits
        if condition_type == TargetingConditionType.TARGET_FEATURE_FLAG:
            return TargetFeatureFlagCondition.TargetFeatureFlagInfo(self.__data_file, visitor.variations)
        if condition_type in (
            TargetingConditionType.FIRST_VISIT,
            TargetingConditionType.LAST_VISIT,
            TargetingConditionType.VISITS,
            TargetingConditionType.SAME_DAY_VISITS,
            TargetingConditionType.NEW_VISITORS,
        ):
            return visitor.visitor_visits
        if TargetingConditionType.HEAT_SLICE:
            return visitor.kcs_heat
        return None

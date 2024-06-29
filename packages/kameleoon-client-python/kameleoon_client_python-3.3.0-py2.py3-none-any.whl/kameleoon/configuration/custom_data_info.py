"""Custom data info"""

from logging import Logger
from typing import Optional, Dict, Union, Any, List


class CustomDataInfo:
    """Custom data info"""

    SCOPE_VISITOR = "VISITOR"

    def __init__(
        self, custom_data: Optional[List[Dict[str, Union[str, int, Any]]]], logger: Optional[Logger] = None
    ) -> None:
        super().__init__()
        self.__mapping_identifier_index = None
        self.__local_only = set()
        self.__visitor_scope = set()
        if custom_data is not None:
            for data in custom_data:
                index = data.get("index")
                if index is not None:
                    index = int(index)
                    if data.get("localOnly"):
                        self.__local_only.add(index)
                    if data.get("scope") == self.SCOPE_VISITOR:
                        self.__visitor_scope.add(index)
                    if data.get("isMappingIdentifier"):
                        if bool(self.__mapping_identifier_index is not None) and logger is not None:
                            logger.info(
                                "More than one mapping identifier is set. Undefined behavior may occur" +
                                " on cross-device reconciliation."
                            )
                        self.__mapping_identifier_index = index

    def is_local_only(self, index: int) -> bool:
        """Check for local only"""
        return index in self.__local_only

    def is_mapping_identifier(self, index: int) -> bool:
        """Check for mapping identifier"""
        return self.__mapping_identifier_index == index

    def is_visitor_scope(self, index: int) -> bool:
        """Check for visitor scope"""
        return index in self.__visitor_scope

    @property
    def mapping_identifier_index(self) -> Optional[int]:
        """Take mapping identifier index"""
        return self.__mapping_identifier_index

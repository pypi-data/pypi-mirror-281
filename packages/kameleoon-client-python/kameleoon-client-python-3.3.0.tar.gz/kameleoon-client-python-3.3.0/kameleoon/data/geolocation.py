# pylint: disable=duplicate-code
"""Geolocation data"""

from typing import Optional
from kameleoon.data.data import Data, DataType
from kameleoon.network.sendable import DuplicationUnsafeSendableBase
from kameleoon.network.query_builder import QueryBuilder, QueryParam, QueryParams


class Geolocation(Data, DuplicationUnsafeSendableBase):
    """Geolocation data"""

    EVENT_TYPE = "staticData"

    # pylint: disable=R0913
    def __init__(
        self,
        country: str,
        region: Optional[str] = None,
        city: Optional[str] = None,
        postal_code: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ) -> None:
        """
        :param country: required
        :type country: str
        :param region:
        :type region: Optional[str]
        :param city:
        :type city: Optional[str]
        :param postal_code:
        :type postal_code: Optional[str]
        :param latitude:
        :type latitude: Optional[float]
        :param longitude:
        :type longitude: Optional[float]

        Example:
        .. code-block:: python3
                kameleoon_client.add_data(visitor_code, Geolocation("France"))
        """
        super().__init__()
        self.__country = country
        self.__region = region
        self.__city = city
        self.__postal_code = postal_code
        self.__latitude = latitude
        self.__longitude = longitude

    @property
    def country(self) -> Optional[str]:
        """Returns country"""
        return self.__country

    @property
    def region(self) -> Optional[str]:
        """Returns region"""
        return self.__region

    @property
    def city(self) -> Optional[str]:
        """Returns city"""
        return self.__city

    @property
    def postal_code(self) -> Optional[str]:
        """Returns postal_code"""
        return self.__postal_code

    @property
    def latitude(self) -> Optional[float]:
        """Returns latitude"""
        return self.__latitude

    @property
    def longitude(self) -> Optional[float]:
        """Returns longitude"""
        return self.__longitude

    @property
    def data_type(self) -> DataType:
        return DataType.GEOLOCATION

    def _add_query_params(self, qb: QueryBuilder) -> None:
        qb.extend(
            QueryParam(QueryParams.EVENT_TYPE, self.EVENT_TYPE),
        )
        if self.country:
            qb.append(QueryParam(QueryParams.COUNTRY, self.country))
        if self.region:
            qb.append(QueryParam(QueryParams.REGION, self.region))
        if self.city:
            qb.append(QueryParam(QueryParams.CITY, self.city))
        if self.postal_code:
            qb.append(QueryParam(QueryParams.POSTAL_CODE, self.postal_code))
        if self.latitude is not None:
            qb.append(QueryParam(QueryParams.LATITUDE, str(self.latitude)))
        if self.longitude is not None:
            qb.append(QueryParam(QueryParams.LONGITUDE, str(self.longitude)))

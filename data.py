#     import json
#
# and then, to convert JSON from a string, do
#
#     result = cian_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, Optional, Dict, TypeVar, Type, Callable, cast
from enum import Enum
from datetime import datetime
from uuid import UUID
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class Breadcrumb:
    url: str
    title: str

    @staticmethod
    def from_dict(obj: Any) -> 'Breadcrumb':
        assert isinstance(obj, dict)
        url = from_str(obj.get("url"))
        title = from_str(obj.get("title"))
        return Breadcrumb(url, title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["url"] = from_str(self.url)
        result["title"] = from_str(self.title)
        return result


class EngineVersionType(Enum):
    TERM = "term"


@dataclass
class EngineVersion:
    type: EngineVersionType
    value: int

    @staticmethod
    def from_dict(obj: Any) -> 'EngineVersion':
        assert isinstance(obj, dict)
        type = EngineVersionType(obj.get("type"))
        value = from_int(obj.get("value"))
        return EngineVersion(type, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = to_enum(EngineVersionType, self.type)
        result["value"] = from_int(self.value)
        return result


class OfficeTypeType(Enum):
    TERMS = "terms"


@dataclass
class OfficeType:
    type: OfficeTypeType
    value: List[int]

    @staticmethod
    def from_dict(obj: Any) -> 'OfficeType':
        assert isinstance(obj, dict)
        type = OfficeTypeType(obj.get("type"))
        value = from_list(from_int, obj.get("value"))
        return OfficeType(type, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = to_enum(OfficeTypeType, self.type)
        result["value"] = from_list(from_int, self.value)
        return result


class TypeEnum(Enum):
    COMMERCIALSALE = "commercialsale"


@dataclass
class JSONQuery:
    region: OfficeType
    type: TypeEnum
    office_type: OfficeType
    engine_version: EngineVersion

    @staticmethod
    def from_dict(obj: Any) -> 'JSONQuery':
        assert isinstance(obj, dict)
        region = OfficeType.from_dict(obj.get("region"))
        type = TypeEnum(obj.get("_type"))
        office_type = OfficeType.from_dict(obj.get("office_type"))
        engine_version = EngineVersion.from_dict(obj.get("engine_version"))
        return JSONQuery(region, type, office_type, engine_version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["region"] = to_class(OfficeType, self.region)
        result["_type"] = to_enum(TypeEnum, self.type)
        result["office_type"] = to_class(OfficeType, self.office_type)
        result["engine_version"] = to_class(EngineVersion, self.engine_version)
        return result


class DealTypeEnum(Enum):
    SALE = "sale"


class Currency(Enum):
    RUR = "rur"
    USD = "usd"
    EUR = "eur"


class PriceTypeEnum(Enum):
    ALL = "all"


@dataclass
class VatPrices:
    rur: int
    usd: int
    eur: int

    @staticmethod
    def from_dict(obj: Any) -> 'VatPrices':
        assert isinstance(obj, dict)
        rur = from_int(obj.get("rur"))
        usd = from_int(obj.get("usd"))
        eur = from_int(obj.get("eur"))
        return VatPrices(rur, usd, eur)

    def to_dict(self) -> dict:
        result: dict = {}
        result["rur"] = from_int(self.rur)
        result["usd"] = from_int(self.usd)
        result["eur"] = from_int(self.eur)
        return result


class VatType(Enum):
    INCLUDED = "included"
    USN = "usn"


@dataclass
class BargainTerms:
    price_rur: int
    contract_type: Optional[DealTypeEnum]
    included_options: List[Any]
    vat_price: Optional[int]
    price: int
    vat_type: Optional[VatType]
    price_usd: int
    vat_included: Optional[bool]
    currency: Currency
    vat_prices: Optional[VatPrices]
    price_eur: int
    price_type: PriceTypeEnum
    sale_type: Optional[str]
    mortgage_allowed: Optional[bool]

    @staticmethod
    def from_dict(obj: Any) -> 'BargainTerms':
        assert isinstance(obj, dict)
        price_rur = from_int(obj.get("priceRur"))
        contract_type = from_union([DealTypeEnum, from_none], obj.get("contractType"))
        included_options = from_list(lambda x: x, obj.get("includedOptions"))
        vat_price = from_union([from_float, from_int, from_str, from_none], obj.get("vatPrice"))
        price = from_float(obj.get("price"))
        vat_type = from_union([VatType, from_none], obj.get("vatType"))
        price_usd = from_int(obj.get("priceUsd"))
        vat_included = from_union([from_none, from_bool], obj.get("vatIncluded"))
        currency = Currency(obj.get("currency"))
        vat_prices = from_union([VatPrices.from_dict, from_none], obj.get("vatPrices"))
        price_eur = from_int(obj.get("priceEur"))
        price_type = PriceTypeEnum(obj.get("priceType"))
        sale_type = from_union([from_str, from_none], obj.get("saleType"))
        mortgage_allowed = from_union([from_none, from_bool], obj.get("mortgageAllowed"))
        return BargainTerms(price_rur, contract_type, included_options, vat_price, price, vat_type, price_usd, vat_included, currency, vat_prices, price_eur, price_type, sale_type, mortgage_allowed)

    def to_dict(self) -> dict:
        result: dict = {}
        result["priceRur"] = from_int(self.price_rur)
        result["contractType"] = from_union([lambda x: to_enum(DealTypeEnum, x), from_none], self.contract_type)
        result["includedOptions"] = from_list(lambda x: x, self.included_options)
        result["vatPrice"] = from_union([from_int, from_none], self.vat_price)
        result["price"] = from_int(self.price)
        result["vatType"] = from_union([lambda x: to_enum(VatType, x), from_none], self.vat_type)
        result["priceUsd"] = from_int(self.price_usd)
        result["vatIncluded"] = from_union([from_none, from_bool], self.vat_included)
        result["currency"] = to_enum(Currency, self.currency)
        result["vatPrices"] = from_union([lambda x: to_class(VatPrices, x), from_none], self.vat_prices)
        result["priceEur"] = from_int(self.price_eur)
        result["priceType"] = to_enum(PriceTypeEnum, self.price_type)
        result["saleType"] = from_union([from_str, from_none], self.sale_type)
        result["mortgageAllowed"] = from_union([from_none, from_bool], self.mortgage_allowed)
        return result


@dataclass
class Parking:
    type: Optional[str]
    is_free: Optional[bool]
    currency: Optional[Currency]
    purpose_type: Optional[str]
    places_count: Optional[int]
    location_type: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Parking':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        is_free = from_union([from_none, from_bool], obj.get("isFree"))
        currency = from_union([Currency, from_none], obj.get("currency"))
        purpose_type = from_union([from_str, from_none], obj.get("purposeType"))
        places_count = from_union([from_int, from_none], obj.get("placesCount"))
        location_type = from_union([from_str, from_none], obj.get("locationType"))
        return Parking(type, is_free, currency, purpose_type, places_count, location_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["isFree"] = from_union([from_none, from_bool], self.is_free)
        result["currency"] = from_union([lambda x: to_enum(Currency, x), from_none], self.currency)
        result["purposeType"] = from_union([from_str, from_none], self.purpose_type)
        result["placesCount"] = from_union([from_int, from_none], self.places_count)
        result["locationType"] = from_union([from_str, from_none], self.location_type)
        return result


class ShoppingCenterScaleTypeEnum(Enum):
    DISTRICT = "district"
    HOUSE = "house"
    STREET = "street"


class StatusType(Enum):
    OPERATIONAL = "operational"


@dataclass
class Building:
    cranage_types: List[Any]
    type: Optional[str]
    build_year: Optional[int]
    lift_types: List[Any]
    floors_count: Optional[int]
    status_type: Optional[StatusType]
    parking: Optional[Parking]
    house_line_type: Optional[str]
    ceiling_height: Optional[str]
    conditioning_type: Optional[str]
    infrastructure: Optional[Dict[str, bool]]
    name: Optional[str]
    material_type: Optional[str]
    total_area: Optional[str]
    house_material_type: Optional[str]
    ventilation_type: Optional[str]
    heating_type: Optional[str]
    extinguishing_system_type: Optional[str]
    gates_type: Optional[str]
    shopping_center_scale_type: Optional[ShoppingCenterScaleTypeEnum]
    class_type: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Building':
        assert isinstance(obj, dict)
        cranage_types = from_list(lambda x: x, obj.get("cranageTypes"))
        type = from_union([from_str, from_none], obj.get("type"))
        build_year = from_union([from_int, from_none], obj.get("buildYear"))
        lift_types = from_list(lambda x: x, obj.get("liftTypes"))
        floors_count = from_union([from_int, from_none], obj.get("floorsCount"))
        status_type = from_union([StatusType, from_none], obj.get("statusType"))
        parking = from_union([Parking.from_dict, from_none], obj.get("parking"))
        house_line_type = from_union([from_str, from_none], obj.get("houseLineType"))
        ceiling_height = from_union([from_str, from_none], obj.get("ceilingHeight"))
        conditioning_type = from_union([from_str, from_none], obj.get("conditioningType"))
        infrastructure = from_union([lambda x: from_dict(from_bool, x), from_none], obj.get("infrastructure"))
        name = from_union([from_str, from_none], obj.get("name"))
        material_type = from_union([from_str, from_none], obj.get("materialType"))
        total_area = from_union([from_str, from_none], obj.get("totalArea"))
        house_material_type = from_union([from_str, from_none], obj.get("houseMaterialType"))
        ventilation_type = from_union([from_str, from_none], obj.get("ventilationType"))
        heating_type = from_union([from_str, from_none], obj.get("heatingType"))
        extinguishing_system_type = from_union([from_str, from_none], obj.get("extinguishingSystemType"))
        gates_type = from_union([from_str, from_none], obj.get("gatesType"))
        shopping_center_scale_type = from_union([ShoppingCenterScaleTypeEnum, from_none], obj.get("shoppingCenterScaleType"))
        class_type = from_union([from_str, from_none], obj.get("classType"))
        return Building(cranage_types, type, build_year, lift_types, floors_count, status_type, parking, house_line_type, ceiling_height, conditioning_type, infrastructure, name, material_type, total_area, house_material_type, ventilation_type, heating_type, extinguishing_system_type, gates_type, shopping_center_scale_type, class_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cranageTypes"] = from_list(lambda x: x, self.cranage_types)
        result["type"] = from_union([from_str, from_none], self.type)
        result["buildYear"] = from_union([from_int, from_none], self.build_year)
        result["liftTypes"] = from_list(lambda x: x, self.lift_types)
        result["floorsCount"] = from_union([from_int, from_none], self.floors_count)
        result["statusType"] = from_union([lambda x: to_enum(StatusType, x), from_none], self.status_type)
        result["parking"] = from_union([lambda x: to_class(Parking, x), from_none], self.parking)
        result["houseLineType"] = from_union([from_str, from_none], self.house_line_type)
        result["ceilingHeight"] = from_union([from_str, from_none], self.ceiling_height)
        result["conditioningType"] = from_union([from_str, from_none], self.conditioning_type)
        result["infrastructure"] = from_union([lambda x: from_dict(from_bool, x), from_none], self.infrastructure)
        result["name"] = from_union([from_str, from_none], self.name)
        result["materialType"] = from_union([from_str, from_none], self.material_type)
        result["totalArea"] = from_union([from_str, from_none], self.total_area)
        result["houseMaterialType"] = from_union([from_str, from_none], self.house_material_type)
        result["ventilationType"] = from_union([from_str, from_none], self.ventilation_type)
        result["heatingType"] = from_union([from_str, from_none], self.heating_type)
        result["extinguishingSystemType"] = from_union([from_str, from_none], self.extinguishing_system_type)
        result["gatesType"] = from_union([from_str, from_none], self.gates_type)
        result["shoppingCenterScaleType"] = from_union([lambda x: to_enum(ShoppingCenterScaleTypeEnum, x), from_none], self.shopping_center_scale_type)
        result["classType"] = from_union([from_str, from_none], self.class_type)
        return result


@dataclass
class BusinessShoppingCenter:
    from_representative: bool
    id: int

    @staticmethod
    def from_dict(obj: Any) -> 'BusinessShoppingCenter':
        assert isinstance(obj, dict)
        from_representative = from_bool(obj.get("fromRepresentative"))
        id = from_int(obj.get("id"))
        return BusinessShoppingCenter(from_representative, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fromRepresentative"] = from_bool(self.from_representative)
        result["id"] = from_int(self.id)
        return result


class CallTrackingProvider(Enum):
    MTS = "mts"


class GeoType(Enum):
    GEO = "geo"


@dataclass
class ValueElement:
    type: ShoppingCenterScaleTypeEnum
    id: int

    @staticmethod
    def from_dict(obj: Any) -> 'ValueElement':
        assert isinstance(obj, dict)
        type = ShoppingCenterScaleTypeEnum(obj.get("type"))
        id = from_int(obj.get("id"))
        return ValueElement(type, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = to_enum(ShoppingCenterScaleTypeEnum, self.type)
        result["id"] = from_int(self.id)
        return result


@dataclass
class DemandJSONQueryGeo:
    type: GeoType
    value: List[ValueElement]

    @staticmethod
    def from_dict(obj: Any) -> 'DemandJSONQueryGeo':
        assert isinstance(obj, dict)
        type = GeoType(obj.get("type"))
        value = from_list(ValueElement.from_dict, obj.get("value"))
        return DemandJSONQueryGeo(type, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = to_enum(GeoType, self.type)
        result["value"] = from_list(lambda x: to_class(ValueElement, x), self.value)
        return result


class PriceType(Enum):
    RANGE = "range"


@dataclass
class PriceValue:
    gte: int
    lte: int

    @staticmethod
    def from_dict(obj: Any) -> 'PriceValue':
        assert isinstance(obj, dict)
        gte = from_int(obj.get("gte"))
        lte = from_int(obj.get("lte"))
        return PriceValue(gte, lte)

    def to_dict(self) -> dict:
        result: dict = {}
        result["gte"] = from_int(self.gte)
        result["lte"] = from_int(self.lte)
        return result


@dataclass
class Price:
    type: PriceType
    value: PriceValue

    @staticmethod
    def from_dict(obj: Any) -> 'Price':
        assert isinstance(obj, dict)
        type = PriceType(obj.get("type"))
        value = PriceValue.from_dict(obj.get("value"))
        return Price(type, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = to_enum(PriceType, self.type)
        result["value"] = to_class(PriceValue, self.value)
        return result


@dataclass
class DemandJSONQuery:
    type: TypeEnum
    office_type: OfficeType
    price: Price
    total_area: Price
    engine_version: EngineVersion
    currency: EngineVersion
    geo: DemandJSONQueryGeo
    region: OfficeType

    @staticmethod
    def from_dict(obj: Any) -> 'DemandJSONQuery':
        assert isinstance(obj, dict)
        type = TypeEnum(obj.get("_type"))
        office_type = OfficeType.from_dict(obj.get("office_type"))
        price = Price.from_dict(obj.get("price"))
        total_area = Price.from_dict(obj.get("total_area"))
        engine_version = EngineVersion.from_dict(obj.get("engine_version"))
        currency = EngineVersion.from_dict(obj.get("currency"))
        geo = DemandJSONQueryGeo.from_dict(obj.get("geo"))
        region = OfficeType.from_dict(obj.get("region"))
        return DemandJSONQuery(type, office_type, price, total_area, engine_version, currency, geo, region)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_type"] = to_enum(TypeEnum, self.type)
        result["office_type"] = to_class(OfficeType, self.office_type)
        result["price"] = to_class(Price, self.price)
        result["total_area"] = to_class(Price, self.total_area)
        result["engine_version"] = to_class(EngineVersion, self.engine_version)
        result["currency"] = to_class(EngineVersion, self.currency)
        result["geo"] = to_class(DemandJSONQueryGeo, self.geo)
        result["region"] = to_class(OfficeType, self.region)
        return result


@dataclass
class Electricity:
    possible_to_connect: None
    power: Optional[int]
    location_type: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Electricity':
        assert isinstance(obj, dict)
        possible_to_connect = from_none(obj.get("possibleToConnect"))
        power = from_union([from_int, from_none], obj.get("power"))
        location_type = from_union([from_none, from_str], obj.get("locationType"))
        return Electricity(possible_to_connect, power, location_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["possibleToConnect"] = from_none(self.possible_to_connect)
        result["power"] = from_union([from_int, from_none], self.power)
        result["locationType"] = from_union([from_none, from_str], self.location_type)
        return result


class EstateTypeEnum(Enum):
    OWNED = "owned"


@dataclass
class Flags:
    is_archived: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Flags':
        assert isinstance(obj, dict)
        is_archived = from_bool(obj.get("isArchived"))
        return Flags(is_archived)

    def to_dict(self) -> dict:
        result: dict = {}
        result["isArchived"] = from_bool(self.is_archived)
        return result


@dataclass
class Garage:
    status: Optional[str]
    material: Optional[str]
    type: str
    garage_type: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Garage':
        assert isinstance(obj, dict)
        status = from_union([from_none, from_str], obj.get("status"))
        material = from_union([from_none, from_str], obj.get("material"))
        type = from_str(obj.get("type"))
        garage_type = from_union([from_none, from_str], obj.get("garageType"))
        return Garage(status, material, type, garage_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["status"] = from_union([from_none, from_str], self.status)
        result["material"] = from_union([from_none, from_str], self.material)
        result["type"] = from_str(self.type)
        result["garageType"] = from_union([from_none, from_str], self.garage_type)
        return result


class AddressType(Enum):
    HOUSE = "house"
    LOCATION = "location"
    STREET = "street"


@dataclass
class Address:
    name: str
    id: int
    location_type_id: Optional[int]
    full_name: str
    type: AddressType
    short_name: str
    is_forming_address: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Address':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        id = from_int(obj.get("id"))
        location_type_id = from_union([from_int, from_none], obj.get("locationTypeId"))
        full_name = from_str(obj.get("fullName"))
        type = AddressType(obj.get("type"))
        short_name = from_str(obj.get("shortName"))
        is_forming_address = from_bool(obj.get("isFormingAddress"))
        return Address(name, id, location_type_id, full_name, type, short_name, is_forming_address)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["id"] = from_int(self.id)
        result["locationTypeId"] = from_union([from_int, from_none], self.location_type_id)
        result["fullName"] = from_str(self.full_name)
        result["type"] = to_enum(AddressType, self.type)
        result["shortName"] = from_str(self.short_name)
        result["isFormingAddress"] = from_bool(self.is_forming_address)
        return result


@dataclass
class Coordinates:
    lat: float
    lng: float

    @staticmethod
    def from_dict(obj: Any) -> 'Coordinates':
        assert isinstance(obj, dict)
        lat = from_float(obj.get("lat"))
        lng = from_float(obj.get("lng"))
        return Coordinates(lat, lng)

    def to_dict(self) -> dict:
        result: dict = {}
        result["lat"] = to_float(self.lat)
        result["lng"] = to_float(self.lng)
        return result


class DistrictType(Enum):
    RAION = "raion"


@dataclass
class District:
    location_id: int
    type: DistrictType
    id: int
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'District':
        assert isinstance(obj, dict)
        location_id = from_int(obj.get("locationId"))
        type = DistrictType(obj.get("type"))
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        return District(location_id, type, id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["locationId"] = from_int(self.location_id)
        result["type"] = to_enum(DistrictType, self.type)
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        return result


@dataclass
class LocationPath:
    country_id: int
    child_to_parent: List[int]

    @staticmethod
    def from_dict(obj: Any) -> 'LocationPath':
        assert isinstance(obj, dict)
        country_id = from_int(obj.get("countryId"))
        child_to_parent = from_list(from_int, obj.get("childToParent"))
        return LocationPath(country_id, child_to_parent)

    def to_dict(self) -> dict:
        result: dict = {}
        result["countryId"] = from_int(self.country_id)
        result["childToParent"] = from_list(from_int, self.child_to_parent)
        return result


@dataclass
class OffersSerializedGeo:
    highways: List[Any]
    country_id: int
    undergrounds: List[Any]
    coordinates: Coordinates
    districts: List[District]
    user_input: str
    address: List[Address]
    location_path: LocationPath

    @staticmethod
    def from_dict(obj: Any) -> 'OffersSerializedGeo':
        assert isinstance(obj, dict)
        highways = from_list(lambda x: x, obj.get("highways"))
        country_id = from_int(obj.get("countryId"))
        undergrounds = from_list(lambda x: x, obj.get("undergrounds"))
        coordinates = Coordinates.from_dict(obj.get("coordinates"))
        districts = from_list(District.from_dict, obj.get("districts"))
        user_input = from_str(obj.get("userInput"))
        address = from_list(Address.from_dict, obj.get("address"))
        location_path = LocationPath.from_dict(obj.get("locationPath"))
        return OffersSerializedGeo(highways, country_id, undergrounds, coordinates, districts, user_input, address, location_path)

    def to_dict(self) -> dict:
        result: dict = {}
        result["highways"] = from_list(lambda x: x, self.highways)
        result["countryId"] = from_int(self.country_id)
        result["undergrounds"] = from_list(lambda x: x, self.undergrounds)
        result["coordinates"] = to_class(Coordinates, self.coordinates)
        result["districts"] = from_list(lambda x: to_class(District, x), self.districts)
        result["userInput"] = from_str(self.user_input)
        result["address"] = from_list(lambda x: to_class(Address, x), self.address)
        result["locationPath"] = to_class(LocationPath, self.location_path)
        return result


class AreaUnitType(Enum):
    HECTARE = "hectare"
    SOTKA = "sotka"


@dataclass
class Land:
    status: None
    type: Optional[EstateTypeEnum]
    area_unit_type: AreaUnitType
    possible_to_change_status: None
    area: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Land':
        assert isinstance(obj, dict)
        status = from_none(obj.get("status"))
        type = from_union([from_none, EstateTypeEnum], obj.get("type"))
        area_unit_type = AreaUnitType(obj.get("areaUnitType"))
        possible_to_change_status = from_none(obj.get("possibleToChangeStatus"))
        area = from_union([from_none, from_str], obj.get("area"))
        return Land(status, type, area_unit_type, possible_to_change_status, area)

    def to_dict(self) -> dict:
        result: dict = {}
        result["status"] = from_none(self.status)
        result["type"] = from_union([from_none, lambda x: to_enum(EstateTypeEnum, x)], self.type)
        result["areaUnitType"] = to_enum(AreaUnitType, self.area_unit_type)
        result["possibleToChangeStatus"] = from_none(self.possible_to_change_status)
        result["area"] = from_union([from_none, from_str], self.area)
        return result


@dataclass
class MonthlyIncome:
    currency: Currency
    income: Optional[int]

    @staticmethod
    def from_dict(obj: Any) -> 'MonthlyIncome':
        assert isinstance(obj, dict)
        currency = Currency(obj.get("currency"))
        income = from_union([from_int, from_none], obj.get("income"))
        return MonthlyIncome(currency, income)

    def to_dict(self) -> dict:
        result: dict = {}
        result["currency"] = to_enum(Currency, self.currency)
        result["income"] = from_union([from_int, from_none], self.income)
        return result


@dataclass
class Notes:
    realtor: None
    offer: None

    @staticmethod
    def from_dict(obj: Any) -> 'Notes':
        assert isinstance(obj, dict)
        realtor = from_none(obj.get("realtor"))
        offer = from_none(obj.get("offer"))
        return Notes(realtor, offer)

    def to_dict(self) -> dict:
        result: dict = {}
        result["realtor"] = from_union([from_str, from_none],self.realtor) 
        result["offer"] = from_none(self.offer)
        return result


class OfferType(Enum):
    COMMERCIAL = "commercial"


@dataclass
class Phone:
    number: str
    country_code: str

    @staticmethod
    def from_dict(obj: Any) -> 'Phone':
        assert isinstance(obj, dict)
        number = from_str(obj.get("number"))
        country_code = from_str(obj.get("countryCode"))
        return Phone(number, country_code)

    def to_dict(self) -> dict:
        result: dict = {}
        result["number"] = from_str(self.number)
        result["countryCode"] = from_str(self.country_code)
        return result


@dataclass
class Photo:
    thumbnail2_url: str
    coordinates: None
    id: int
    source: None
    rotate_degree: None
    thumbnail_url: str
    full_url: str
    is_default: bool
    mini_url: str

    @staticmethod
    def from_dict(obj: Any) -> 'Photo':
        assert isinstance(obj, dict)
        thumbnail2_url = from_str(obj.get("thumbnail2Url"))
        coordinates = from_none(obj.get("coordinates"))
        id = from_int(obj.get("id"))
        source = from_none(obj.get("source"))
        rotate_degree = from_none(obj.get("rotateDegree"))
        thumbnail_url = from_str(obj.get("thumbnailUrl"))
        full_url = from_str(obj.get("fullUrl"))
        is_default = from_bool(obj.get("isDefault"))
        mini_url = from_str(obj.get("miniUrl"))
        return Photo(thumbnail2_url, coordinates, id, source, rotate_degree, thumbnail_url, full_url, is_default, mini_url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["thumbnail2Url"] = from_str(self.thumbnail2_url)
        result["coordinates"] = from_none(self.coordinates)
        result["id"] = from_int(self.id)
        result["source"] = from_none(self.source)
        result["rotateDegree"] = from_none(self.rotate_degree)
        result["thumbnailUrl"] = from_str(self.thumbnail_url)
        result["fullUrl"] = from_str(self.full_url)
        result["isDefault"] = from_bool(self.is_default)
        result["miniUrl"] = from_str(self.mini_url)
        return result


class PlatformType(Enum):
    IOS = "ios"
    UPLOAD = "upload"
    WEB_SITE = "webSite"


@dataclass
class Platform:
    version: Optional[str]
    type: PlatformType

    @staticmethod
    def from_dict(obj: Any) -> 'Platform':
        assert isinstance(obj, dict)
        version = from_union([from_none, from_str], obj.get("version"))
        type = PlatformType(obj.get("type"))
        return Platform(version, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["version"] = from_union([from_none, from_str], self.version)
        result["type"] = to_enum(PlatformType, self.type)
        return result


@dataclass
class PriceData:
    payment_period: None
    currency: Currency
    price: int

    @staticmethod
    def from_dict(obj: Any) -> 'PriceData':
        assert isinstance(obj, dict)
        payment_period = from_none(obj.get("paymentPeriod"))
        currency = Currency(obj.get("currency"))
        price = from_int(obj.get("price"))
        return PriceData(payment_period, currency, price)

    def to_dict(self) -> dict:
        result: dict = {}
        result["paymentPeriod"] = from_none(self.payment_period)
        result["currency"] = to_enum(Currency, self.currency)
        result["price"] = from_int(self.price)
        return result


@dataclass
class PriceChange:
    change_time: datetime
    price_data: PriceData

    @staticmethod
    def from_dict(obj: Any) -> 'PriceChange':
        assert isinstance(obj, dict)
        change_time = from_datetime(obj.get("changeTime"))
        price_data = PriceData.from_dict(obj.get("priceData"))
        return PriceChange(change_time, price_data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["changeTime"] = self.change_time.isoformat()
        result["priceData"] = to_class(PriceData, self.price_data)
        return result


class Service(Enum):
    AUCTION = "auction"
    CALLTRACKING = "calltracking"
    HIGHLIGHT = "highlight"
    PAID = "paid"
    PREMIUM = "premium"
    TOP3 = "top3"


class TermType(Enum):
    DAILY_LIMITED = "dailyLimited"
    DAILY_TERMLESS = "dailyTermless"
    PERIODICAL = "periodical"


@dataclass
class Term:
    tariff_identificator: None
    is_compulsory: None
    days: int
    services: List[Service]
    type: TermType
    dynamic_price: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Term':
        assert isinstance(obj, dict)
        tariff_identificator = from_none(obj.get("tariffIdentificator"))
        is_compulsory = from_none(obj.get("isCompulsory"))
        days = from_int(obj.get("days"))
        services = from_list(Service, obj.get("services"))
        type = TermType(obj.get("type"))
        dynamic_price = from_union([from_none, from_str], obj.get("dynamicPrice"))
        return Term(tariff_identificator, is_compulsory, days, services, type, dynamic_price)

    def to_dict(self) -> dict:
        result: dict = {}
        result["tariffIdentificator"] = from_none(self.tariff_identificator)
        result["isCompulsory"] = from_none(self.is_compulsory)
        result["days"] = from_int(self.days)
        result["services"] = from_list(lambda x: to_enum(Service, x), self.services)
        result["type"] = to_enum(TermType, self.type)
        result["dynamicPrice"] = from_union([from_none, from_str], self.dynamic_price)
        return result


@dataclass
class PublishTerms:
    autoprolong: bool
    terms: List[Term]

    @staticmethod
    def from_dict(obj: Any) -> 'PublishTerms':
        assert isinstance(obj, dict)
        autoprolong = from_bool(obj.get("autoprolong"))
        terms = from_list(Term.from_dict, obj.get("terms"))
        return PublishTerms(autoprolong, terms)

    def to_dict(self) -> dict:
        result: dict = {}
        result["autoprolong"] = from_bool(self.autoprolong)
        result["terms"] = from_list(lambda x: to_class(Term, x), self.terms)
        return result


@dataclass
class SpecialtyElement:
    rus_name: str
    eng_name: str
    id: int

    @staticmethod
    def from_dict(obj: Any) -> 'SpecialtyElement':
        assert isinstance(obj, dict)
        rus_name = from_str(obj.get("rusName"))
        eng_name = from_str(obj.get("engName"))
        id = from_int(obj.get("id"))
        return SpecialtyElement(rus_name, eng_name, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["rusName"] = from_str(self.rus_name)
        result["engName"] = from_str(self.eng_name)
        result["id"] = from_int(self.id)
        return result


@dataclass
class OffersSerializedSpecialty:
    additional_types: List[Any]
    specialties: Optional[List[SpecialtyElement]]
    types: List[str]

    @staticmethod
    def from_dict(obj: Any) -> 'OffersSerializedSpecialty':
        assert isinstance(obj, dict)
        additional_types = from_list(lambda x: x, obj.get("additionalTypes"))
        specialties = from_union([lambda x: from_list(SpecialtyElement.from_dict, x), from_none], obj.get("specialties"))
        types = from_list(from_str, obj.get("types"))
        return OffersSerializedSpecialty(additional_types, specialties, types)

    def to_dict(self) -> dict:
        result: dict = {}
        result["additionalTypes"] = from_list(lambda x: x, self.additional_types)
        result["specialties"] = from_union([lambda x: from_list(lambda x: to_class(SpecialtyElement, x), x), from_none], self.specialties)
        result["types"] = from_list(from_str, self.types)
        return result


@dataclass
class Statistic:
    total: int
    daily: int

    @staticmethod
    def from_dict(obj: Any) -> 'Statistic':
        assert isinstance(obj, dict)
        total = from_int(obj.get("total"))
        daily = from_int(obj.get("daily"))
        return Statistic(total, daily)

    def to_dict(self) -> dict:
        result: dict = {}
        result["total"] = from_int(self.total)
        result["daily"] = from_int(self.daily)
        return result


class Status(Enum):
    PUBLISHED = "published"


class AgentAccountType(Enum):
    AGENCY = "agency"
    SPECIALIST = "specialist"


@dataclass
class AgentAvailability:
    available: bool
    user_id: int

    @staticmethod
    def from_dict(obj: Any) -> 'AgentAvailability':
        assert isinstance(obj, dict)
        available = from_bool(obj.get("available"))
        user_id = from_int(obj.get("userId"))
        return AgentAvailability(available, user_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["available"] = from_bool(self.available)
        result["userId"] = from_int(self.user_id)
        return result


class CianProfileStatus(Enum):
    APPROVED = "approved"
    HIDE = "hide"


class UserTrustLevel(Enum):
    INVOLVED = "involved"
    NEW = "new"
    NOT_INVOLVED = "notInvolved"


class UserType(Enum):
    REALTOR_BASED = "realtor_based"
    REALTOR_NOT_COMMERCE = "realtor_not_commerce"


@dataclass
class User:
    user_trust_level: UserTrustLevel
    agency_name: str
    agent_availability: AgentAvailability
    cian_user_id: int
    is_chats_enabled: bool
    is_sub_agent: bool
    user_type: UserType
    is_agent: bool
    is_hidden: bool
    phone_numbers: Optional[List[Phone]]
    agent_account_type: Optional[AgentAccountType]
    cian_profile_status: Optional[CianProfileStatus]
    agency_name_v2: Optional[str]
    company_name: Optional[str]
    experience: Optional[str]
    agent_avatar_url: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        user_trust_level = UserTrustLevel(obj.get("userTrustLevel"))
        agency_name = from_str(obj.get("agencyName"))
        agent_availability = AgentAvailability.from_dict(obj.get("agentAvailability"))
        cian_user_id = from_int(obj.get("cianUserId"))
        is_chats_enabled = from_bool(obj.get("isChatsEnabled"))
        is_sub_agent = from_bool(obj.get("isSubAgent"))
        user_type = UserType(obj.get("userType"))
        is_agent = from_bool(obj.get("isAgent"))
        is_hidden = from_bool(obj.get("isHidden"))
        phone_numbers = from_union([lambda x: from_list(Phone.from_dict, x), from_none], obj.get("phoneNumbers"))
        agent_account_type = from_union([AgentAccountType, from_none], obj.get("agentAccountType"))
        cian_profile_status = from_union([CianProfileStatus, from_none], obj.get("cianProfileStatus"))
        agency_name_v2 = from_union([from_str, from_none], obj.get("agencyNameV2"))
        company_name = from_union([from_str, from_none], obj.get("companyName"))
        experience = from_union([from_str, from_none], obj.get("experience"))
        agent_avatar_url = from_union([from_str, from_none], obj.get("agentAvatarUrl"))
        return User(user_trust_level, agency_name, agent_availability, cian_user_id, is_chats_enabled, is_sub_agent, user_type, is_agent, is_hidden, phone_numbers, agent_account_type, cian_profile_status, agency_name_v2, company_name, experience, agent_avatar_url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["userTrustLevel"] = to_enum(UserTrustLevel, self.user_trust_level)
        result["agencyName"] = from_str(self.agency_name)
        result["agentAvailability"] = to_class(AgentAvailability, self.agent_availability)
        result["cianUserId"] = from_int(self.cian_user_id)
        result["isChatsEnabled"] = from_bool(self.is_chats_enabled)
        result["isSubAgent"] = from_bool(self.is_sub_agent)
        result["userType"] = to_enum(UserType, self.user_type)
        result["isAgent"] = from_bool(self.is_agent)
        result["isHidden"] = from_bool(self.is_hidden)
        result["phoneNumbers"] = from_union([lambda x: from_list(lambda x: to_class(Phone, x), x), from_none], self.phone_numbers)
        result["agentAccountType"] = from_union([lambda x: to_enum(AgentAccountType, x), from_none], self.agent_account_type)
        result["cianProfileStatus"] = from_union([lambda x: to_enum(CianProfileStatus, x), from_none], self.cian_profile_status)
        result["agencyNameV2"] = from_union([from_str, from_none], self.agency_name_v2)
        result["companyName"] = from_union([from_str, from_none], self.company_name)
        result["experience"] = from_union([from_str, from_none], self.experience)
        result["agentAvatarUrl"] = from_union([from_str, from_none], self.agent_avatar_url)
        return result


@dataclass
class ValueAddedServices:
    is_premium: bool
    is_paid: bool
    is_top3: bool
    is_colorized: bool
    is_free: bool
    is_calltracking: bool

    @staticmethod
    def from_dict(obj: Any) -> 'ValueAddedServices':
        assert isinstance(obj, dict)
        is_premium = from_bool(obj.get("isPremium"))
        is_paid = from_bool(obj.get("isPaid"))
        is_top3 = from_bool(obj.get("isTop3"))
        is_colorized = from_bool(obj.get("isColorized"))
        is_free = from_bool(obj.get("isFree"))
        is_calltracking = from_bool(obj.get("isCalltracking"))
        return ValueAddedServices(is_premium, is_paid, is_top3, is_colorized, is_free, is_calltracking)

    def to_dict(self) -> dict:
        result: dict = {}
        result["isPremium"] = from_bool(self.is_premium)
        result["isPaid"] = from_bool(self.is_paid)
        result["isTop3"] = from_bool(self.is_top3)
        result["isColorized"] = from_bool(self.is_colorized)
        result["isFree"] = from_bool(self.is_free)
        result["isCalltracking"] = from_bool(self.is_calltracking)
        return result


@dataclass
class OffersSerialized:
    tax_number: None
    has_phone: None
    newbuilding: None
    has_hairdryer: None
    room_type: None
    drainage_type: None
    furniture_presence: None
    has_furniture: Optional[bool]
    has_conditioner: None
    share_amount: None
    price_per_unit_area_per_year_rur_for_search: None
    archived_date: None
    layout: Optional[str]
    settlement_name: None
    title: None
    electricity: Optional[Electricity]
    work_time_info: None
    min_price_total: None
    all_from_offrep: None
    platform: Platform
    has_extinguishing_system: None
    electricity_power: None
    garage: Optional[Garage]
    chat_id: None
    user_id: int
    price_total_rur: int
    description_minhash: str
    has_pool: None
    ga_label: str
    total_area: str
    leisure: None
    price_per_unit_area: int
    separate_wcs_count: None
    property_type: Optional[str]
    drainage_capacity: None
    geo: OffersSerializedGeo
    furniture: None
    all_rooms_area: None
    demand_json_query: DemandJSONQuery
    is_paid: bool
    name: None
    notes: Notes
    children_allowed: None
    price_per_unit_area_per_year_rur: None
    has_check_in_24: None
    min_vat_price_total_per_month_rur: None
    demolished_in_moscow_programm: None
    permitted_use_type: None
    drainage: None
    min_vat_price_total_rur: None
    floor_material_type: Optional[str]
    vas_type: None
    price_total_usd: int
    rosreestr_check: None
    has_lift: None
    phones: List[Phone]
    floor_number: Optional[int]
    min_area: None
    has_investment_project: None
    statistic: Statistic
    price_per_unit_area_usd: int
    has_transport_services: None
    price_per_unit_area_rur: int
    category: str
    room_area: None
    has_shower: None
    is_colorized: bool
    is_hidden_by_user: bool
    bedrooms_count: None
    min_price_total_rur: None
    price_total_per_month: None
    external_id: None
    is_occupied: Optional[bool]
    external_url: None
    has_dishwasher: None
    booking: None
    price_total_eur: int
    has_wired_internet: None
    additional_phone_lines_allowed: None
    is_top3: bool
    possible_to_change_permitted_use_type: None
    price_total_per_month_usd: None
    water: None
    pets_allowed: None
    electricity_type: None
    has_fridge: None
    rooms_area: None
    max_area: None
    has_transfer: None
    publish_terms: PublishTerms
    min_price_total_per_month: None
    is_enabled_call_tracking: Optional[bool]
    min_price_total_rur_for_search: None
    gas_type: None
    has_heating: None
    cpl_moderation: None
    water_capacity: None
    flat_type: None
    has_jacuzzi: None
    placement_type: Optional[str]
    is_fairplay: bool
    gas_pressure: None
    has_parking: None
    rent_by_parts_description: None
    has_internet: None
    condition_rating_type: None
    price_per_unit_area_per_month_rur_for_search: None
    categories_ids: List[int]
    min_price_total_per_month_rur: None
    feedbox_multi_offer_key: None
    has_bathhouse: None
    has_encumbrances: None
    kitchen_area: None
    is_legal_address_provided: Optional[bool]
    videos: List[Any]
    is_favorite: bool
    price_per_unit_area_per_month: None
    windows_view_type: None
    has_washer: None
    gas_capacity: None
    cian_id: int
    without_client_fee: None
    price_per_unit_area_per_year_eur: None
    cian_user_id: int
    phone_lines_count: None
    is_rent_by_parts: bool
    loggias_count: None
    has_security: None
    price_per_unit_area_per_year_usd: None
    is_customs: None
    price_changes: List[PriceChange]
    business_shopping_center: Optional[BusinessShoppingCenter]
    gas: None
    specialty: OffersSerializedSpecialty
    price_per_unit_area_per_year: None
    photos: List[Photo]
    has_shop_windows: Optional[bool]
    rooms_for_sale_count: None
    is_penthouse: None
    has_equipment: Optional[bool]
    is_auction: bool
    offer_type: OfferType
    is_new: bool
    vat_price_total_rur: Optional[int]
    edit_date: datetime
    price_total_per_month_eur: None
    object_guid: UUID
    wc_location_type: None
    has_light: Optional[bool]
    is_from_builder: None
    repair_type: None
    value_added_services: ValueAddedServices
    has_seconded_docs: None
    deal_type: DealTypeEnum
    similar: None
    has_drainage: None
    price_total_rur_for_search: int
    price_total_per_month_rur: None
    has_kitchen_furniture: None
    is_by_homeowner: None
    has_tv: None
    driveway_type: None
    min_price_total_per_month_rur_for_search: None
    jk_url: None
    layout_photo: None
    decoration: None
    has_tea_coffee_sugar: None
    has_electricity: Optional[bool]
    price_per_unit_area_eur: int
    call_tracking_provider: Optional[CallTrackingProvider]
    input_type: Optional[str]
    has_bathtub: None
    has_wifi: None
    condition_type: Optional[str]
    water_type: None
    has_garage: None
    can_parts: Optional[bool]
    has_excursions: None
    access_type: Optional[str]
    is_duplicated_description: bool
    id: int
    price_per_unit_area_per_month_rur: None
    has_gas: None
    estate_type: Optional[EstateTypeEnum]
    project_declaration_url: None
    is_apartments: None
    has_iron: None
    has_water: Optional[bool]
    status: Status
    available_from: Optional[datetime]
    is_premium: bool
    added: str
    description: str
    price_total_per_month_rur_for_search: None
    is_in_hidden_base: bool
    price_per_unit_area_rur_for_search: int
    monthly_income: Optional[MonthlyIncome]
    district: None
    user: User
    bargain_terms: BargainTerms
    from_developer: None
    has_safe_custody: None
    balconies_count: None
    building: Building
    land: Optional[Land]
    living_area: None
    published_user_id: int
    beds_count: None
    water_pipes_count: Optional[int]
    vat_price_total_per_month_rur: None
    wc_type: None
    kp: None
    flags: Flags
    has_ramp: None
    promo_info: None
    rooms_count: None
    price_total: int
    combined_wcs_count: None
    is_pro: Optional[bool]

    @staticmethod
    def from_dict(obj: Any) -> 'OffersSerialized':
        assert isinstance(obj, dict)
        tax_number = from_none(obj.get("taxNumber"))
        has_phone = from_none(obj.get("hasPhone"))
        newbuilding = from_none(obj.get("newbuilding"))
        has_hairdryer = from_none(obj.get("hasHairdryer"))
        room_type = from_none(obj.get("roomType"))
        drainage_type = from_none(obj.get("drainageType"))
        furniture_presence = from_none(obj.get("furniturePresence"))
        has_furniture = from_union([from_none, from_bool], obj.get("hasFurniture"))
        has_conditioner = from_none(obj.get("hasConditioner"))
        share_amount = from_none(obj.get("shareAmount"))
        price_per_unit_area_per_year_rur_for_search = from_none(obj.get("pricePerUnitAreaPerYearRurForSearch"))
        archived_date = from_none(obj.get("archivedDate"))
        layout = from_union([from_none, from_str], obj.get("layout"))
        settlement_name = from_none(obj.get("settlementName"))
        title = from_none(obj.get("title"))
        electricity = from_union([from_none, Electricity.from_dict], obj.get("electricity"))
        work_time_info = from_none(obj.get("workTimeInfo"))
        min_price_total = from_none(obj.get("minPriceTotal"))
        all_from_offrep = from_none(obj.get("allFromOffrep"))
        platform = Platform.from_dict(obj.get("platform"))
        has_extinguishing_system = from_none(obj.get("hasExtinguishingSystem"))
        electricity_power = from_none(obj.get("electricityPower"))
        garage = from_union([from_none, Garage.from_dict], obj.get("garage"))
        chat_id = from_none(obj.get("chatId"))
        user_id = from_int(obj.get("userId"))
        price_total_rur = from_int(obj.get("priceTotalRur"))
        description_minhash = from_str(obj.get("descriptionMinhash"))
        has_pool = from_none(obj.get("hasPool"))
        ga_label = from_str(obj.get("gaLabel"))
        total_area = from_str(obj.get("totalArea"))
        leisure = from_none(obj.get("leisure"))
        price_per_unit_area = from_int(obj.get("pricePerUnitArea"))
        separate_wcs_count = from_none(obj.get("separateWcsCount"))
        property_type = from_union([from_none, from_str], obj.get("propertyType"))
        drainage_capacity = from_none(obj.get("drainageCapacity"))
        geo = OffersSerializedGeo.from_dict(obj.get("geo"))
        furniture = from_none(obj.get("furniture"))
        all_rooms_area = from_none(obj.get("allRoomsArea"))
        demand_json_query = DemandJSONQuery.from_dict(obj.get("demandJsonQuery"))
        is_paid = from_bool(obj.get("isPaid"))
        name = from_none(obj.get("name"))
        notes = Notes.from_dict(obj.get("notes"))
        children_allowed = from_none(obj.get("childrenAllowed"))
        price_per_unit_area_per_year_rur = from_none(obj.get("pricePerUnitAreaPerYearRur"))
        has_check_in_24 = from_none(obj.get("hasCheckIn_24"))
        min_vat_price_total_per_month_rur = from_none(obj.get("minVatPriceTotalPerMonthRur"))
        demolished_in_moscow_programm = from_none(obj.get("demolishedInMoscowProgramm"))
        permitted_use_type = from_none(obj.get("permittedUseType"))
        drainage = from_none(obj.get("drainage"))
        min_vat_price_total_rur = from_none(obj.get("minVatPriceTotalRur"))
        floor_material_type = from_union([from_none, from_str], obj.get("floorMaterialType"))
        vas_type = from_none(obj.get("vasType"))
        price_total_usd = from_int(obj.get("priceTotalUsd"))
        rosreestr_check = from_none(obj.get("rosreestrCheck"))
        has_lift = from_none(obj.get("hasLift"))
        phones = from_list(Phone.from_dict, obj.get("phones"))
        floor_number = from_union([from_int, from_none], obj.get("floorNumber"))
        min_area = from_none(obj.get("minArea"))
        has_investment_project = from_none(obj.get("hasInvestmentProject"))
        statistic = Statistic.from_dict(obj.get("statistic"))
        price_per_unit_area_usd = from_int(obj.get("pricePerUnitAreaUsd"))
        has_transport_services = from_none(obj.get("hasTransportServices"))
        price_per_unit_area_rur = from_int(obj.get("pricePerUnitAreaRur"))
        category = from_str(obj.get("category"))
        room_area = from_none(obj.get("roomArea"))
        has_shower = from_none(obj.get("hasShower"))
        is_colorized = from_bool(obj.get("isColorized"))
        is_hidden_by_user = from_bool(obj.get("isHiddenByUser"))
        bedrooms_count = from_none(obj.get("bedroomsCount"))
        min_price_total_rur = from_none(obj.get("minPriceTotalRur"))
        price_total_per_month = from_none(obj.get("priceTotalPerMonth"))
        external_id = from_none(obj.get("externalId"))
        is_occupied = from_union([from_none, from_bool], obj.get("isOccupied"))
        external_url = from_none(obj.get("externalUrl"))
        has_dishwasher = from_none(obj.get("hasDishwasher"))
        booking = from_none(obj.get("booking"))
        price_total_eur = from_int(obj.get("priceTotalEur"))
        has_wired_internet = from_none(obj.get("hasWiredInternet"))
        additional_phone_lines_allowed = from_none(obj.get("additionalPhoneLinesAllowed"))
        is_top3 = from_bool(obj.get("isTop3"))
        possible_to_change_permitted_use_type = from_none(obj.get("possibleToChangePermittedUseType"))
        price_total_per_month_usd = from_none(obj.get("priceTotalPerMonthUsd"))
        water = from_none(obj.get("water"))
        pets_allowed = from_none(obj.get("petsAllowed"))
        electricity_type = from_none(obj.get("electricityType"))
        has_fridge = from_none(obj.get("hasFridge"))
        rooms_area = from_none(obj.get("roomsArea"))
        max_area = from_none(obj.get("maxArea"))
        has_transfer = from_none(obj.get("hasTransfer"))
        publish_terms = PublishTerms.from_dict(obj.get("publishTerms"))
        min_price_total_per_month = from_none(obj.get("minPriceTotalPerMonth"))
        is_enabled_call_tracking = from_union([from_none, from_bool], obj.get("isEnabledCallTracking"))
        min_price_total_rur_for_search = from_none(obj.get("minPriceTotalRurForSearch"))
        gas_type = from_none(obj.get("gasType"))
        has_heating = from_none(obj.get("hasHeating"))
        cpl_moderation = from_none(obj.get("cplModeration"))
        water_capacity = from_none(obj.get("waterCapacity"))
        flat_type = from_none(obj.get("flatType"))
        has_jacuzzi = from_none(obj.get("hasJacuzzi"))
        placement_type = from_union([from_none, from_str], obj.get("placementType"))
        is_fairplay = from_bool(obj.get("isFairplay"))
        gas_pressure = from_none(obj.get("gasPressure"))
        has_parking = from_none(obj.get("hasParking"))
        rent_by_parts_description = from_none(obj.get("rentByPartsDescription"))
        has_internet = from_none(obj.get("hasInternet"))
        condition_rating_type = from_none(obj.get("conditionRatingType"))
        price_per_unit_area_per_month_rur_for_search = from_none(obj.get("pricePerUnitAreaPerMonthRurForSearch"))
        categories_ids = from_list(from_int, obj.get("categoriesIds"))
        min_price_total_per_month_rur = from_none(obj.get("minPriceTotalPerMonthRur"))
        feedbox_multi_offer_key = from_none(obj.get("feedboxMultiOfferKey"))
        has_bathhouse = from_none(obj.get("hasBathhouse"))
        has_encumbrances = from_none(obj.get("hasEncumbrances"))
        kitchen_area = from_none(obj.get("kitchenArea"))
        is_legal_address_provided = from_union([from_none, from_bool], obj.get("isLegalAddressProvided"))
        videos = from_list(lambda x: x, obj.get("videos"))
        is_favorite = from_bool(obj.get("isFavorite"))
        price_per_unit_area_per_month = from_none(obj.get("pricePerUnitAreaPerMonth"))
        windows_view_type = from_none(obj.get("windowsViewType"))
        has_washer = from_none(obj.get("hasWasher"))
        gas_capacity = from_none(obj.get("gasCapacity"))
        cian_id = from_int(obj.get("cianId"))
        without_client_fee = from_none(obj.get("withoutClientFee"))
        price_per_unit_area_per_year_eur = from_none(obj.get("pricePerUnitAreaPerYearEur"))
        cian_user_id = from_int(obj.get("cianUserId"))
        phone_lines_count = from_none(obj.get("phoneLinesCount"))
        is_rent_by_parts = from_bool(obj.get("isRentByParts"))
        loggias_count = from_none(obj.get("loggiasCount"))
        has_security = from_none(obj.get("hasSecurity"))
        price_per_unit_area_per_year_usd = from_none(obj.get("pricePerUnitAreaPerYearUsd"))
        is_customs = from_none(obj.get("isCustoms"))
        price_changes = from_list(PriceChange.from_dict, obj.get("priceChanges"))
        business_shopping_center = from_union([from_none, BusinessShoppingCenter.from_dict], obj.get("businessShoppingCenter"))
        gas = from_none(obj.get("gas"))
        specialty = OffersSerializedSpecialty.from_dict(obj.get("specialty"))
        price_per_unit_area_per_year = from_none(obj.get("pricePerUnitAreaPerYear"))
        photos = from_list(Photo.from_dict, obj.get("photos"))
        has_shop_windows = from_union([from_none, from_bool], obj.get("hasShopWindows"))
        rooms_for_sale_count = from_none(obj.get("roomsForSaleCount"))
        is_penthouse = from_none(obj.get("isPenthouse"))
        has_equipment = from_union([from_none, from_bool], obj.get("hasEquipment"))
        is_auction = from_bool(obj.get("isAuction"))
        offer_type = OfferType(obj.get("offerType"))
        is_new = from_bool(obj.get("isNew"))
        vat_price_total_rur = from_union([from_int, from_none], obj.get("vatPriceTotalRur"))
        edit_date = from_datetime(obj.get("editDate"))
        price_total_per_month_eur = from_none(obj.get("priceTotalPerMonthEur"))
        object_guid = UUID(obj.get("objectGuid"))
        wc_location_type = from_none(obj.get("wcLocationType"))
        has_light = from_union([from_none, from_bool], obj.get("hasLight"))
        is_from_builder = from_none(obj.get("isFromBuilder"))
        repair_type = from_none(obj.get("repairType"))
        value_added_services = ValueAddedServices.from_dict(obj.get("valueAddedServices"))
        has_seconded_docs = from_none(obj.get("hasSecondedDocs"))
        deal_type = DealTypeEnum(obj.get("dealType"))
        similar = from_none(obj.get("similar"))
        has_drainage = from_none(obj.get("hasDrainage"))
        price_total_rur_for_search = from_int(obj.get("priceTotalRurForSearch"))
        price_total_per_month_rur = from_none(obj.get("priceTotalPerMonthRur"))
        has_kitchen_furniture = from_none(obj.get("hasKitchenFurniture"))
        is_by_homeowner = from_none(obj.get("isByHomeowner"))
        has_tv = from_none(obj.get("hasTv"))
        driveway_type = from_none(obj.get("drivewayType"))
        min_price_total_per_month_rur_for_search = from_none(obj.get("minPriceTotalPerMonthRurForSearch"))
        jk_url = from_none(obj.get("jkUrl"))
        layout_photo = from_none(obj.get("layoutPhoto"))
        decoration = from_none(obj.get("decoration"))
        has_tea_coffee_sugar = from_none(obj.get("hasTeaCoffeeSugar"))
        has_electricity = from_union([from_none, from_bool], obj.get("hasElectricity"))
        price_per_unit_area_eur = from_int(obj.get("pricePerUnitAreaEur"))
        call_tracking_provider = from_union([from_none, CallTrackingProvider], obj.get("callTrackingProvider"))
        input_type = from_union([from_none, from_str], obj.get("inputType"))
        has_bathtub = from_none(obj.get("hasBathtub"))
        has_wifi = from_none(obj.get("hasWifi"))
        condition_type = from_union([from_none, from_str], obj.get("conditionType"))
        water_type = from_none(obj.get("waterType"))
        has_garage = from_none(obj.get("hasGarage"))
        can_parts = from_union([from_none, from_bool], obj.get("canParts"))
        has_excursions = from_none(obj.get("hasExcursions"))
        access_type = from_union([from_none, from_str], obj.get("accessType"))
        is_duplicated_description = from_bool(obj.get("isDuplicatedDescription"))
        id = from_int(obj.get("id"))
        price_per_unit_area_per_month_rur = from_none(obj.get("pricePerUnitAreaPerMonthRur"))
        has_gas = from_none(obj.get("hasGas"))
        estate_type = from_union([from_none, EstateTypeEnum], obj.get("estateType"))
        project_declaration_url = from_none(obj.get("projectDeclarationUrl"))
        is_apartments = from_none(obj.get("isApartments"))
        has_iron = from_none(obj.get("hasIron"))
        has_water = from_union([from_none, from_bool], obj.get("hasWater"))
        status = Status(obj.get("status"))
        available_from = from_union([from_none, from_datetime], obj.get("availableFrom"))
        is_premium = from_bool(obj.get("isPremium"))
        added = from_str(obj.get("added"))
        description = from_str(obj.get("description"))
        price_total_per_month_rur_for_search = from_none(obj.get("priceTotalPerMonthRurForSearch"))
        is_in_hidden_base = from_bool(obj.get("isInHiddenBase"))
        price_per_unit_area_rur_for_search = from_int(obj.get("pricePerUnitAreaRurForSearch"))
        monthly_income = from_union([from_none, MonthlyIncome.from_dict], obj.get("monthlyIncome"))
        district = from_none(obj.get("district"))
        user = User.from_dict(obj.get("user"))
        bargain_terms = BargainTerms.from_dict(obj.get("bargainTerms"))
        from_developer = from_none(obj.get("fromDeveloper"))
        has_safe_custody = from_none(obj.get("hasSafeCustody"))
        balconies_count = from_none(obj.get("balconiesCount"))
        building = Building.from_dict(obj.get("building"))
        land = from_union([Land.from_dict, from_none], obj.get("land"))
        living_area = from_none(obj.get("livingArea"))
        published_user_id = from_int(obj.get("publishedUserId"))
        beds_count = from_none(obj.get("bedsCount"))
        water_pipes_count = from_union([from_int, from_none], obj.get("waterPipesCount"))
        vat_price_total_per_month_rur = from_none(obj.get("vatPriceTotalPerMonthRur"))
        wc_type = from_none(obj.get("wcType"))
        kp = from_none(obj.get("kp"))
        flags = Flags.from_dict(obj.get("flags"))
        has_ramp = from_none(obj.get("hasRamp"))
        promo_info = from_none(obj.get("promoInfo"))
        rooms_count = from_none(obj.get("roomsCount"))
        price_total = from_int(obj.get("priceTotal"))
        combined_wcs_count = from_none(obj.get("combinedWcsCount"))
        is_pro = from_union([from_none, from_bool], obj.get("isPro"))
        return OffersSerialized(tax_number, has_phone, newbuilding, has_hairdryer, room_type, drainage_type, furniture_presence, has_furniture, has_conditioner, share_amount, price_per_unit_area_per_year_rur_for_search, archived_date, layout, settlement_name, title, electricity, work_time_info, min_price_total, all_from_offrep, platform, has_extinguishing_system, electricity_power, garage, chat_id, user_id, price_total_rur, description_minhash, has_pool, ga_label, total_area, leisure, price_per_unit_area, separate_wcs_count, property_type, drainage_capacity, geo, furniture, all_rooms_area, demand_json_query, is_paid, name, notes, children_allowed, price_per_unit_area_per_year_rur, has_check_in_24, min_vat_price_total_per_month_rur, demolished_in_moscow_programm, permitted_use_type, drainage, min_vat_price_total_rur, floor_material_type, vas_type, price_total_usd, rosreestr_check, has_lift, phones, floor_number, min_area, has_investment_project, statistic, price_per_unit_area_usd, has_transport_services, price_per_unit_area_rur, category, room_area, has_shower, is_colorized, is_hidden_by_user, bedrooms_count, min_price_total_rur, price_total_per_month, external_id, is_occupied, external_url, has_dishwasher, booking, price_total_eur, has_wired_internet, additional_phone_lines_allowed, is_top3, possible_to_change_permitted_use_type, price_total_per_month_usd, water, pets_allowed, electricity_type, has_fridge, rooms_area, max_area, has_transfer, publish_terms, min_price_total_per_month, is_enabled_call_tracking, min_price_total_rur_for_search, gas_type, has_heating, cpl_moderation, water_capacity, flat_type, has_jacuzzi, placement_type, is_fairplay, gas_pressure, has_parking, rent_by_parts_description, has_internet, condition_rating_type, price_per_unit_area_per_month_rur_for_search, categories_ids, min_price_total_per_month_rur, feedbox_multi_offer_key, has_bathhouse, has_encumbrances, kitchen_area, is_legal_address_provided, videos, is_favorite, price_per_unit_area_per_month, windows_view_type, has_washer, gas_capacity, cian_id, without_client_fee, price_per_unit_area_per_year_eur, cian_user_id, phone_lines_count, is_rent_by_parts, loggias_count, has_security, price_per_unit_area_per_year_usd, is_customs, price_changes, business_shopping_center, gas, specialty, price_per_unit_area_per_year, photos, has_shop_windows, rooms_for_sale_count, is_penthouse, has_equipment, is_auction, offer_type, is_new, vat_price_total_rur, edit_date, price_total_per_month_eur, object_guid, wc_location_type, has_light, is_from_builder, repair_type, value_added_services, has_seconded_docs, deal_type, similar, has_drainage, price_total_rur_for_search, price_total_per_month_rur, has_kitchen_furniture, is_by_homeowner, has_tv, driveway_type, min_price_total_per_month_rur_for_search, jk_url, layout_photo, decoration, has_tea_coffee_sugar, has_electricity, price_per_unit_area_eur, call_tracking_provider, input_type, has_bathtub, has_wifi, condition_type, water_type, has_garage, can_parts, has_excursions, access_type, is_duplicated_description, id, price_per_unit_area_per_month_rur, has_gas, estate_type, project_declaration_url, is_apartments, has_iron, has_water, status, available_from, is_premium, added, description, price_total_per_month_rur_for_search, is_in_hidden_base, price_per_unit_area_rur_for_search, monthly_income, district, user, bargain_terms, from_developer, has_safe_custody, balconies_count, building, land, living_area, published_user_id, beds_count, water_pipes_count, vat_price_total_per_month_rur, wc_type, kp, flags, has_ramp, promo_info, rooms_count, price_total, combined_wcs_count, is_pro)

    def to_dict(self) -> dict:
        result: dict = {}
        result["taxNumber"] = from_none(self.tax_number)
        result["hasPhone"] = from_none(self.has_phone)
        result["newbuilding"] = from_none(self.newbuilding)
        result["hasHairdryer"] = from_none(self.has_hairdryer)
        result["roomType"] = from_none(self.room_type)
        result["drainageType"] = from_none(self.drainage_type)
        result["furniturePresence"] = from_none(self.furniture_presence)
        result["hasFurniture"] = from_union([from_none, from_bool], self.has_furniture)
        result["hasConditioner"] = from_none(self.has_conditioner)
        result["shareAmount"] = from_none(self.share_amount)
        result["pricePerUnitAreaPerYearRurForSearch"] = from_none(self.price_per_unit_area_per_year_rur_for_search)
        result["archivedDate"] = from_none(self.archived_date)
        result["layout"] = from_union([from_none, from_str], self.layout)
        result["settlementName"] = from_none(self.settlement_name)
        result["title"] = from_none(self.title)
        result["electricity"] = from_union([from_none, lambda x: to_class(Electricity, x)], self.electricity)
        result["workTimeInfo"] = from_none(self.work_time_info)
        result["minPriceTotal"] = from_none(self.min_price_total)
        result["allFromOffrep"] = from_none(self.all_from_offrep)
        result["platform"] = to_class(Platform, self.platform)
        result["hasExtinguishingSystem"] = from_none(self.has_extinguishing_system)
        result["electricityPower"] = from_none(self.electricity_power)
        result["garage"] = from_union([from_none, lambda x: to_class(Garage, x)], self.garage)
        result["chatId"] = from_none(self.chat_id)
        result["userId"] = from_int(self.user_id)
        result["priceTotalRur"] = from_int(self.price_total_rur)
        result["descriptionMinhash"] = from_str(self.description_minhash)
        result["hasPool"] = from_none(self.has_pool)
        result["gaLabel"] = from_str(self.ga_label)
        result["totalArea"] = from_str(self.total_area)
        result["leisure"] = from_none(self.leisure)
        result["pricePerUnitArea"] = from_int(self.price_per_unit_area)
        result["separateWcsCount"] = from_none(self.separate_wcs_count)
        result["propertyType"] = from_union([from_none, from_str], self.property_type)
        result["drainageCapacity"] = from_none(self.drainage_capacity)
        result["geo"] = to_class(OffersSerializedGeo, self.geo)
        result["furniture"] = from_none(self.furniture)
        result["allRoomsArea"] = from_none(self.all_rooms_area)
        result["demandJsonQuery"] = to_class(DemandJSONQuery, self.demand_json_query)
        result["isPaid"] = from_bool(self.is_paid)
        result["name"] = from_none(self.name)
        result["notes"] = to_class(Notes, self.notes)
        result["childrenAllowed"] = from_none(self.children_allowed)
        result["pricePerUnitAreaPerYearRur"] = from_none(self.price_per_unit_area_per_year_rur)
        result["hasCheckIn_24"] = from_none(self.has_check_in_24)
        result["minVatPriceTotalPerMonthRur"] = from_none(self.min_vat_price_total_per_month_rur)
        result["demolishedInMoscowProgramm"] = from_none(self.demolished_in_moscow_programm)
        result["permittedUseType"] = from_none(self.permitted_use_type)
        result["drainage"] = from_none(self.drainage)
        result["minVatPriceTotalRur"] = from_none(self.min_vat_price_total_rur)
        result["floorMaterialType"] = from_union([from_none, from_str], self.floor_material_type)
        result["vasType"] = from_none(self.vas_type)
        result["priceTotalUsd"] = from_int(self.price_total_usd)
        result["rosreestrCheck"] = from_none(self.rosreestr_check)
        result["hasLift"] = from_none(self.has_lift)
        result["phones"] = from_list(lambda x: to_class(Phone, x), self.phones)
        result["floorNumber"] = from_union([from_int, from_none], self.floor_number)
        result["minArea"] = from_none(self.min_area)
        result["hasInvestmentProject"] = from_none(self.has_investment_project)
        result["statistic"] = to_class(Statistic, self.statistic)
        result["pricePerUnitAreaUsd"] = from_int(self.price_per_unit_area_usd)
        result["hasTransportServices"] = from_none(self.has_transport_services)
        result["pricePerUnitAreaRur"] = from_int(self.price_per_unit_area_rur)
        result["category"] = from_str(self.category)
        result["roomArea"] = from_none(self.room_area)
        result["hasShower"] = from_none(self.has_shower)
        result["isColorized"] = from_bool(self.is_colorized)
        result["isHiddenByUser"] = from_bool(self.is_hidden_by_user)
        result["bedroomsCount"] = from_none(self.bedrooms_count)
        result["minPriceTotalRur"] = from_none(self.min_price_total_rur)
        result["priceTotalPerMonth"] = from_none(self.price_total_per_month)
        result["externalId"] = from_none(self.external_id)
        result["isOccupied"] = from_union([from_none, from_bool], self.is_occupied)
        result["externalUrl"] = from_none(self.external_url)
        result["hasDishwasher"] = from_none(self.has_dishwasher)
        result["booking"] = from_none(self.booking)
        result["priceTotalEur"] = from_int(self.price_total_eur)
        result["hasWiredInternet"] = from_none(self.has_wired_internet)
        result["additionalPhoneLinesAllowed"] = from_none(self.additional_phone_lines_allowed)
        result["isTop3"] = from_bool(self.is_top3)
        result["possibleToChangePermittedUseType"] = from_none(self.possible_to_change_permitted_use_type)
        result["priceTotalPerMonthUsd"] = from_none(self.price_total_per_month_usd)
        result["water"] = from_none(self.water)
        result["petsAllowed"] = from_none(self.pets_allowed)
        result["electricityType"] = from_none(self.electricity_type)
        result["hasFridge"] = from_none(self.has_fridge)
        result["roomsArea"] = from_none(self.rooms_area)
        result["maxArea"] = from_none(self.max_area)
        result["hasTransfer"] = from_none(self.has_transfer)
        result["publishTerms"] = to_class(PublishTerms, self.publish_terms)
        result["minPriceTotalPerMonth"] = from_none(self.min_price_total_per_month)
        result["isEnabledCallTracking"] = from_union([from_none, from_bool], self.is_enabled_call_tracking)
        result["minPriceTotalRurForSearch"] = from_none(self.min_price_total_rur_for_search)
        result["gasType"] = from_none(self.gas_type)
        result["hasHeating"] = from_none(self.has_heating)
        result["cplModeration"] = from_none(self.cpl_moderation)
        result["waterCapacity"] = from_none(self.water_capacity)
        result["flatType"] = from_none(self.flat_type)
        result["hasJacuzzi"] = from_none(self.has_jacuzzi)
        result["placementType"] = from_union([from_none, from_str], self.placement_type)
        result["isFairplay"] = from_bool(self.is_fairplay)
        result["gasPressure"] = from_none(self.gas_pressure)
        result["hasParking"] = from_none(self.has_parking)
        result["rentByPartsDescription"] = from_none(self.rent_by_parts_description)
        result["hasInternet"] = from_none(self.has_internet)
        result["conditionRatingType"] = from_none(self.condition_rating_type)
        result["pricePerUnitAreaPerMonthRurForSearch"] = from_none(self.price_per_unit_area_per_month_rur_for_search)
        result["categoriesIds"] = from_list(from_int, self.categories_ids)
        result["minPriceTotalPerMonthRur"] = from_none(self.min_price_total_per_month_rur)
        result["feedboxMultiOfferKey"] = from_none(self.feedbox_multi_offer_key)
        result["hasBathhouse"] = from_none(self.has_bathhouse)
        result["hasEncumbrances"] = from_none(self.has_encumbrances)
        result["kitchenArea"] = from_none(self.kitchen_area)
        result["isLegalAddressProvided"] = from_union([from_none, from_bool], self.is_legal_address_provided)
        result["videos"] = from_list(lambda x: x, self.videos)
        result["isFavorite"] = from_bool(self.is_favorite)
        result["pricePerUnitAreaPerMonth"] = from_none(self.price_per_unit_area_per_month)
        result["windowsViewType"] = from_none(self.windows_view_type)
        result["hasWasher"] = from_none(self.has_washer)
        result["gasCapacity"] = from_none(self.gas_capacity)
        result["cianId"] = from_int(self.cian_id)
        result["withoutClientFee"] = from_none(self.without_client_fee)
        result["pricePerUnitAreaPerYearEur"] = from_none(self.price_per_unit_area_per_year_eur)
        result["cianUserId"] = from_int(self.cian_user_id)
        result["phoneLinesCount"] = from_none(self.phone_lines_count)
        result["isRentByParts"] = from_bool(self.is_rent_by_parts)
        result["loggiasCount"] = from_none(self.loggias_count)
        result["hasSecurity"] = from_none(self.has_security)
        result["pricePerUnitAreaPerYearUsd"] = from_none(self.price_per_unit_area_per_year_usd)
        result["isCustoms"] = from_none(self.is_customs)
        result["priceChanges"] = from_list(lambda x: to_class(PriceChange, x), self.price_changes)
        result["businessShoppingCenter"] = from_union([from_none, lambda x: to_class(BusinessShoppingCenter, x)], self.business_shopping_center)
        result["gas"] = from_none(self.gas)
        result["specialty"] = to_class(OffersSerializedSpecialty, self.specialty)
        result["pricePerUnitAreaPerYear"] = from_none(self.price_per_unit_area_per_year)
        result["photos"] = from_list(lambda x: to_class(Photo, x), self.photos)
        result["hasShopWindows"] = from_union([from_none, from_bool], self.has_shop_windows)
        result["roomsForSaleCount"] = from_none(self.rooms_for_sale_count)
        result["isPenthouse"] = from_none(self.is_penthouse)
        result["hasEquipment"] = from_union([from_none, from_bool], self.has_equipment)
        result["isAuction"] = from_bool(self.is_auction)
        result["offerType"] = to_enum(OfferType, self.offer_type)
        result["isNew"] = from_bool(self.is_new)
        result["vatPriceTotalRur"] = from_union([from_int, from_none], self.vat_price_total_rur)
        result["editDate"] = self.edit_date.isoformat()
        result["priceTotalPerMonthEur"] = from_none(self.price_total_per_month_eur)
        result["objectGuid"] = str(self.object_guid)
        result["wcLocationType"] = from_none(self.wc_location_type)
        result["hasLight"] = from_union([from_none, from_bool], self.has_light)
        result["isFromBuilder"] = from_none(self.is_from_builder)
        result["repairType"] = from_none(self.repair_type)
        result["valueAddedServices"] = to_class(ValueAddedServices, self.value_added_services)
        result["hasSecondedDocs"] = from_none(self.has_seconded_docs)
        result["dealType"] = to_enum(DealTypeEnum, self.deal_type)
        result["similar"] = from_none(self.similar)
        result["hasDrainage"] = from_none(self.has_drainage)
        result["priceTotalRurForSearch"] = from_int(self.price_total_rur_for_search)
        result["priceTotalPerMonthRur"] = from_none(self.price_total_per_month_rur)
        result["hasKitchenFurniture"] = from_none(self.has_kitchen_furniture)
        result["isByHomeowner"] = from_none(self.is_by_homeowner)
        result["hasTv"] = from_none(self.has_tv)
        result["drivewayType"] = from_none(self.driveway_type)
        result["minPriceTotalPerMonthRurForSearch"] = from_none(self.min_price_total_per_month_rur_for_search)
        result["jkUrl"] = from_none(self.jk_url)
        result["layoutPhoto"] = from_none(self.layout_photo)
        result["decoration"] = from_none(self.decoration)
        result["hasTeaCoffeeSugar"] = from_none(self.has_tea_coffee_sugar)
        result["hasElectricity"] = from_union([from_none, from_bool], self.has_electricity)
        result["pricePerUnitAreaEur"] = from_int(self.price_per_unit_area_eur)
        result["callTrackingProvider"] = from_union([from_none, lambda x: to_enum(CallTrackingProvider, x)], self.call_tracking_provider)
        result["inputType"] = from_union([from_none, from_str], self.input_type)
        result["hasBathtub"] = from_none(self.has_bathtub)
        result["hasWifi"] = from_none(self.has_wifi)
        result["conditionType"] = from_union([from_none, from_str], self.condition_type)
        result["waterType"] = from_none(self.water_type)
        result["hasGarage"] = from_none(self.has_garage)
        result["canParts"] = from_union([from_none, from_bool], self.can_parts)
        result["hasExcursions"] = from_none(self.has_excursions)
        result["accessType"] = from_union([from_none, from_str], self.access_type)
        result["isDuplicatedDescription"] = from_bool(self.is_duplicated_description)
        result["id"] = from_int(self.id)
        result["pricePerUnitAreaPerMonthRur"] = from_none(self.price_per_unit_area_per_month_rur)
        result["hasGas"] = from_none(self.has_gas)
        result["estateType"] = from_union([from_none, lambda x: to_enum(EstateTypeEnum, x)], self.estate_type)
        result["projectDeclarationUrl"] = from_none(self.project_declaration_url)
        result["isApartments"] = from_none(self.is_apartments)
        result["hasIron"] = from_none(self.has_iron)
        result["hasWater"] = from_union([from_none, from_bool], self.has_water)
        result["status"] = to_enum(Status, self.status)
        result["availableFrom"] = from_union([from_none, lambda x: x.isoformat()], self.available_from)
        result["isPremium"] = from_bool(self.is_premium)
        result["added"] = from_str(self.added)
        result["description"] = from_str(self.description)
        result["priceTotalPerMonthRurForSearch"] = from_none(self.price_total_per_month_rur_for_search)
        result["isInHiddenBase"] = from_bool(self.is_in_hidden_base)
        result["pricePerUnitAreaRurForSearch"] = from_int(self.price_per_unit_area_rur_for_search)
        result["monthlyIncome"] = from_union([from_none, lambda x: to_class(MonthlyIncome, x)], self.monthly_income)
        result["district"] = from_none(self.district)
        result["user"] = to_class(User, self.user)
        result["bargainTerms"] = to_class(BargainTerms, self.bargain_terms)
        result["fromDeveloper"] = from_none(self.from_developer)
        result["hasSafeCustody"] = from_none(self.has_safe_custody)
        result["balconiesCount"] = from_none(self.balconies_count)
        result["building"] = to_class(Building, self.building)
        result["land"] = from_union([lambda x: to_class(Land, x), from_none], self.land)
        result["livingArea"] = from_none(self.living_area)
        result["publishedUserId"] = from_int(self.published_user_id)
        result["bedsCount"] = from_none(self.beds_count)
        result["waterPipesCount"] = from_union([from_int, from_none], self.water_pipes_count)
        result["vatPriceTotalPerMonthRur"] = from_none(self.vat_price_total_per_month_rur)
        result["wcType"] = from_none(self.wc_type)
        result["kp"] = from_none(self.kp)
        result["flags"] = to_class(Flags, self.flags)
        result["hasRamp"] = from_none(self.has_ramp)
        result["promoInfo"] = from_none(self.promo_info)
        result["roomsCount"] = from_none(self.rooms_count)
        result["priceTotal"] = from_int(self.price_total)
        result["combinedWcsCount"] = from_none(self.combined_wcs_count)
        result["isPro"] = from_union([from_none, from_bool], self.is_pro)
        return result


@dataclass
class SEOData:
    noindex: bool
    h1: str
    meta_description: str
    description: str
    title: str

    @staticmethod
    def from_dict(obj: Any) -> 'SEOData':
        assert isinstance(obj, dict)
        noindex = from_bool(obj.get("noindex"))
        h1 = from_str(obj.get("h1"))
        meta_description = from_str(obj.get("metaDescription"))
        description = from_str(obj.get("description"))
        title = from_str(obj.get("title"))
        return SEOData(noindex, h1, meta_description, description, title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["noindex"] = from_bool(self.noindex)
        result["h1"] = from_str(self.h1)
        result["metaDescription"] = from_str(self.meta_description)
        result["description"] = from_str(self.description)
        result["title"] = from_str(self.title)
        return result


@dataclass
class Data:
    suggestions_query: None
    aggregated_count: int
    query_string: str
    is_newobjects_enabled: bool
    is_call_button_enabled: bool
    ml_ranking_guid: None
    breadcrumbs: List[Breadcrumb]
    top3_is_on: bool
    seo_data: SEOData
    offer_count: int
    ml_ranking_model_version: None
    kp: None
    avg_price_informer: None
    call_button_variant: int
    search_uuid: UUID
    newobjects_serialized: List[Any]
    offers_serialized: List[OffersSerialized]
    json_query: JSONQuery

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        assert isinstance(obj, dict)
        suggestions_query = from_none(obj.get("suggestionsQuery"))
        aggregated_count = from_int(obj.get("aggregatedCount"))
        query_string = from_str(obj.get("queryString"))
        is_newobjects_enabled = from_bool(obj.get("isNewobjectsEnabled"))
        is_call_button_enabled = from_bool(obj.get("isCallButtonEnabled"))
        ml_ranking_guid = from_none(obj.get("mlRankingGuid"))
        breadcrumbs = from_list(Breadcrumb.from_dict, obj.get("breadcrumbs"))
        top3_is_on = from_bool(obj.get("top3IsOn"))
        seo_data = SEOData.from_dict(obj.get("seoData"))
        offer_count = from_int(obj.get("offerCount"))
        ml_ranking_model_version = from_none(obj.get("mlRankingModelVersion"))
        kp = from_none(obj.get("kp"))
        avg_price_informer = from_none(obj.get("avgPriceInformer"))
        call_button_variant = from_int(obj.get("callButtonVariant"))
        search_uuid = from_none(obj.get("searchUuid"))
        newobjects_serialized = from_list(lambda x: x, obj.get("newobjectsSerialized"))
        offers_serialized = from_list(OffersSerialized.from_dict, obj.get("offersSerialized"))
        json_query = JSONQuery.from_dict(obj.get("jsonQuery"))
        return Data(suggestions_query, aggregated_count, query_string, is_newobjects_enabled, is_call_button_enabled, ml_ranking_guid, breadcrumbs, top3_is_on, seo_data, offer_count, ml_ranking_model_version, kp, avg_price_informer, call_button_variant, search_uuid, newobjects_serialized, offers_serialized, json_query)

    def to_dict(self) -> dict:
        result: dict = {}
        result["suggestionsQuery"] = from_none(self.suggestions_query)
        result["aggregatedCount"] = from_int(self.aggregated_count)
        result["queryString"] = from_str(self.query_string)
        result["isNewobjectsEnabled"] = from_bool(self.is_newobjects_enabled)
        result["isCallButtonEnabled"] = from_bool(self.is_call_button_enabled)
        result["mlRankingGuid"] = from_none(self.ml_ranking_guid)
        result["breadcrumbs"] = from_list(lambda x: to_class(Breadcrumb, x), self.breadcrumbs)
        result["top3IsOn"] = from_bool(self.top3_is_on)
        result["seoData"] = to_class(SEOData, self.seo_data)
        result["offerCount"] = from_int(self.offer_count)
        result["mlRankingModelVersion"] = from_none(self.ml_ranking_model_version)
        result["kp"] = from_none(self.kp)
        result["avgPriceInformer"] = from_none(self.avg_price_informer)
        result["callButtonVariant"] = from_int(self.call_button_variant)
        result["searchUuid"] = str(self.search_uuid)
        result["newobjectsSerialized"] = from_list(lambda x: x, self.newobjects_serialized)
        result["offersSerialized"] = from_list(lambda x: to_class(OffersSerialized, x), self.offers_serialized)
        result["jsonQuery"] = to_class(JSONQuery, self.json_query)
        return result


@dataclass
class Cian:
    status: str
    data: Data

    @staticmethod
    def from_dict(obj: Any) -> 'Cian':
        assert isinstance(obj, dict)
        status = from_str(obj.get("status"))
        data = Data.from_dict(obj.get("data"))
        return Cian(status, data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["status"] = from_str(self.status)
        result["data"] = to_class(Data, self.data)
        return result


def cian_from_dict(s: Any) -> Cian:
    return Cian.from_dict(s)


def cian_to_dict(x: Cian) -> Any:
    return to_class(Cian, x)

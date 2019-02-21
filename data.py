# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = data_from_dict(json.loads(json_string))

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


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


class Breadcrumb:
    title: str
    url: str

    def __init__(self, title: str, url: str) -> None:
        self.title = title
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> 'Breadcrumb':
        assert isinstance(obj, dict)
        title = from_str(obj.get("title"))
        url = from_str(obj.get("url"))
        return Breadcrumb(title, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_str(self.title)
        result["url"] = from_str(self.url)
        return result


class EngineVersionType(Enum):
    TERM = "term"


class EngineVersion:
    type: EngineVersionType
    value: int

    def __init__(self, type: EngineVersionType, value: int) -> None:
        self.type = type
        self.value = value

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
    RANGE = "range"
    TERMS = "terms"


class OfficeType:
    type: OfficeTypeType
    value: List[Optional[int]]

    def __init__(self, type: OfficeTypeType, value: List[Optional[int]]) -> None:
        self.type = type
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'OfficeType':
        assert isinstance(obj, dict)
        type = OfficeTypeType(obj.get("type"))
        value = from_list(lambda x: from_union([from_int, from_none], x), obj.get("value"))
        return OfficeType(type, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = to_enum(OfficeTypeType, self.type)
        result["value"] = from_list(lambda x: from_union([from_int, from_none], x), self.value)
        return result


class TypeEnum(Enum):
    COMMERCIALSALE = "commercialsale"


class JSONQuery:
    type: TypeEnum
    engine_version: EngineVersion
    office_type: Optional[OfficeType]
    region: OfficeType

    def __init__(self, type: TypeEnum, engine_version: EngineVersion, office_type: Optional[OfficeType], region: OfficeType) -> None:
        self.type = type
        self.engine_version = engine_version
        self.office_type = office_type
        self.region = region

    @staticmethod
    def from_dict(obj: Any) -> 'JSONQuery':
        assert isinstance(obj, dict)
        type = TypeEnum(obj.get("_type"))
        engine_version = EngineVersion.from_dict(obj.get("engine_version"))
        office_type = from_union([OfficeType.from_dict, from_none], obj.get("office_type"))
        region = OfficeType.from_dict(obj.get("region"))
        return JSONQuery(type, engine_version, office_type, region)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_type"] = to_enum(TypeEnum, self.type)
        result["engine_version"] = to_class(EngineVersion, self.engine_version)
        result["office_type"] = from_union([lambda x: to_class(OfficeType, x), from_none], self.office_type)
        result["region"] = to_class(OfficeType, self.region)
        return result


class AccessTypeEnum(Enum):
    FREE = "free"
    PASS_SYSTEM = "passSystem"


class AllFromOffrep:
    count: int
    url: str

    def __init__(self, count: int, url: str) -> None:
        self.count = count
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> 'AllFromOffrep':
        assert isinstance(obj, dict)
        count = from_int(obj.get("count"))
        url = from_str(obj.get("url"))
        return AllFromOffrep(count, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_int(self.count)
        result["url"] = from_str(self.url)
        return result


class DealTypeEnum(Enum):
    LEASE_ASSIGNMENT = "leaseAssignment"
    SALE = "sale"


class Currency(Enum):
    EUR = "eur"
    RUR = "rur"
    USD = "usd"


class TPrices:
    eur: int
    rur: int
    usd: int

    def __init__(self, eur: int, rur: int, usd: int) -> None:
        self.eur = eur
        self.rur = rur
        self.usd = usd

    @staticmethod
    def from_dict(obj: Any) -> 'TPrices':
        assert isinstance(obj, dict)
        eur = from_int(obj.get("eur"))
        rur = from_int(obj.get("rur"))
        usd = from_int(obj.get("usd"))
        return TPrices(eur, rur, usd)

    def to_dict(self) -> dict:
        result: dict = {}
        result["eur"] = from_int(self.eur)
        result["rur"] = from_int(self.rur)
        result["usd"] = from_int(self.usd)
        return result


class IncludedOption(Enum):
    OPERATIONAL_COSTS = "operationalCosts"
    UTILITY_CHARGES = "utilityCharges "


class PriceTypeEnum(Enum):
    ALL = "all"
    HECTARE = "hectare"
    SOTKA = "sotka"
    SQUARE_METER = "squareMeter"


class VatType(Enum):
    INCLUDED = "included"
    NOT_INCLUDED = "notIncluded"
    USN = "usn"
    VAT_INCLUDED = "vatIncluded"
    VAT_NOT_INCLUDED = "vatNotIncluded"


class BargainTerms:
    contract_type: Optional[DealTypeEnum]
    currency: Currency
    deposit: Optional[int]
    deposit_prices: Optional[TPrices]
    included_options: Optional[List[IncludedOption]]
    mortgage_allowed: Optional[bool]
    price: Optional[float]
    price_eur: Optional[float]
    price_rur: Optional[float]
    price_type: PriceTypeEnum
    price_usd: Optional[float]
    sale_type: Optional[AccessTypeEnum]
    vat_included: Optional[bool]
    vat_price: Optional[float]
    vat_prices: Optional[TPrices]
    vat_type: Optional[VatType]

    def __init__(self, contract_type: Optional[DealTypeEnum], currency: Currency, deposit: Optional[int], deposit_prices: Optional[TPrices], included_options: Optional[List[IncludedOption]], mortgage_allowed: Optional[bool], price: Optional[float], price_eur: Optional[float], price_rur: Optional[float], price_type: PriceTypeEnum, price_usd: Optional[float], sale_type: Optional[AccessTypeEnum], vat_included: Optional[bool], vat_price: Optional[float], vat_prices: Optional[TPrices], vat_type: Optional[VatType]) -> None:
        self.contract_type = contract_type
        self.currency = currency
        self.deposit = deposit
        self.deposit_prices = deposit_prices
        self.included_options = included_options
        self.mortgage_allowed = mortgage_allowed
        self.price = price
        self.price_eur = price_eur
        self.price_rur = price_rur
        self.price_type = price_type
        self.price_usd = price_usd
        self.sale_type = sale_type
        self.vat_included = vat_included
        self.vat_price = vat_price
        self.vat_prices = vat_prices
        self.vat_type = vat_type

    @staticmethod
    def from_dict(obj: Any) -> 'BargainTerms':
        assert isinstance(obj, dict)
        contract_type = from_union([DealTypeEnum, from_none], obj.get("contractType"))
        currency = Currency(obj.get("currency"))
        deposit = from_union([from_int, from_none], obj.get("deposit"))
        deposit_prices = from_union([TPrices.from_dict, from_none], obj.get("depositPrices"))
        included_options = from_union([lambda x: from_list(IncludedOption, x), from_none], obj.get("includedOptions"))
        mortgage_allowed = from_union([from_none, from_bool], obj.get("mortgageAllowed"))
        price = from_union([from_float, from_none], obj.get("price"))
        price_eur = from_union([from_float, from_none], obj.get("priceEur"))
        price_rur = from_union([from_float, from_none], obj.get("priceRur"))
        price_type = PriceTypeEnum(obj.get("priceType"))
        price_usd = from_union([from_float, from_none], obj.get("priceUsd"))
        sale_type = from_union([from_none, AccessTypeEnum], obj.get("saleType"))
        vat_included = from_union([from_none, from_bool], obj.get("vatIncluded"))
        vat_price = from_union([from_float, from_none], obj.get("vatPrice"))
        vat_prices = from_union([TPrices.from_dict, from_none], obj.get("vatPrices"))
        vat_type = from_union([VatType, from_none], obj.get("vatType"))
        return BargainTerms(contract_type, currency, deposit, deposit_prices, included_options, mortgage_allowed, price, price_eur, price_rur, price_type, price_usd, sale_type, vat_included, vat_price, vat_prices, vat_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["contractType"] = from_union([lambda x: to_enum(DealTypeEnum, x), from_none], self.contract_type)
        result["currency"] = to_enum(Currency, self.currency)
        result["deposit"] = from_union([from_int, from_none], self.deposit)
        result["depositPrices"] = from_union([lambda x: to_class(TPrices, x), from_none], self.deposit_prices)
        result["includedOptions"] = from_union([lambda x: from_list(lambda x: to_enum(IncludedOption, x), x), from_none], self.included_options)
        result["mortgageAllowed"] = from_union([from_none, from_bool], self.mortgage_allowed)
        result["price"] = from_union([to_float, from_none], self.price)
        result["priceEur"] = from_union([to_float, from_none], self.price_eur)
        result["priceRur"] = from_union([to_float, from_none], self.price_rur)
        result["priceType"] = to_enum(PriceTypeEnum, self.price_type)
        result["priceUsd"] = from_union([to_float, from_none], self.price_usd)
        result["saleType"] = from_union([from_none, lambda x: to_enum(AccessTypeEnum, x)], self.sale_type)
        result["vatIncluded"] = from_union([from_none, from_bool], self.vat_included)
        result["vatPrice"] = from_union([to_float, from_none], self.vat_price)
        result["vatPrices"] = from_union([lambda x: to_class(TPrices, x), from_none], self.vat_prices)
        result["vatType"] = from_union([lambda x: to_enum(VatType, x), from_none], self.vat_type)
        return result


class ClassType(Enum):
    A = "a"
    A_PLUS = "aPlus"
    B = "b"
    B_MINUS = "bMinus"
    B_PLUS = "bPlus"
    C = "c"


class ConditioningTypeEnum(Enum):
    BORDER = "border"
    CENTRAL = "central"
    LOCAL = "local"
    LOCATION = "location"
    NO = "no"


class PurposeTypeEnum(Enum):
    BEAM = "beam"
    CARGO = "cargo"
    ESCALATOR = "escalator"
    LIFT = "lift"
    PASSENGER = "passenger"
    TELPHER = "telpher"


class CranageTypeElement:
    count: int
    load_capacity: Optional[float]
    type: PurposeTypeEnum

    def __init__(self, count: int, load_capacity: Optional[float], type: PurposeTypeEnum) -> None:
        self.count = count
        self.load_capacity = load_capacity
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'CranageTypeElement':
        assert isinstance(obj, dict)
        count = from_int(obj.get("count"))
        load_capacity = from_union([from_float, from_none], obj.get("loadCapacity"))
        type = PurposeTypeEnum(obj.get("type"))
        return CranageTypeElement(count, load_capacity, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_int(self.count)
        result["loadCapacity"] = from_union([to_float, from_none], self.load_capacity)
        result["type"] = to_enum(PurposeTypeEnum, self.type)
        return result


class ExtinguishingSystemType(Enum):
    ALARM = "alarm"
    HYDRANT = "hydrant"
    NO = "no"
    POWDER = "powder"
    SPRINKLER = "sprinkler"


class HeatingType(Enum):
    AUTONOMOUS = "autonomous"
    CENTRAL = "central"
    NO = "no"


class HouseLineType(Enum):
    FIRST = "first"
    OTHER = "other"
    SECOND = "second"


class HouseMaterialType(Enum):
    BRICK = "brick"
    METAL = "metal"
    MONOLITH = "monolith"
    MONOLITH_BRICK = "monolithBrick"
    PANEL = "panel"


class OpeningHoursType(Enum):
    ROUND_THE_CLOCK = "roundTheClock"
    SPECIFIC = "specific"


class OpeningHours:
    type: OpeningHoursType

    def __init__(self, type: OpeningHoursType) -> None:
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'OpeningHours':
        assert isinstance(obj, dict)
        type = OpeningHoursType(obj.get("type"))
        return OpeningHours(type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = to_enum(OpeningHoursType, self.type)
        return result


class ParkingType(Enum):
    GROUND = "ground"
    MULTILEVEL = "multilevel"
    OPEN = "open"
    ROOF = "roof"
    UNDERGROUND = "underground"


class Parking:
    currency: Optional[Currency]
    is_free: Optional[bool]
    location_type: Optional[str]
    places_count: Optional[int]
    price_monthly: Optional[float]
    purpose_type: Optional[PurposeTypeEnum]
    type: Optional[ParkingType]

    def __init__(self, currency: Optional[Currency], is_free: Optional[bool], location_type: Optional[str], places_count: Optional[int], price_monthly: Optional[float], purpose_type: Optional[PurposeTypeEnum], type: Optional[ParkingType]) -> None:
        self.currency = currency
        self.is_free = is_free
        self.location_type = location_type
        self.places_count = places_count
        self.price_monthly = price_monthly
        self.purpose_type = purpose_type
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Parking':
        assert isinstance(obj, dict)
        currency = from_union([Currency, from_none], obj.get("currency"))
        is_free = from_union([from_none, from_bool], obj.get("isFree"))
        location_type = from_union([from_none, from_str], obj.get("locationType"))
        places_count = from_union([from_int, from_none], obj.get("placesCount"))
        price_monthly = from_union([from_float, from_none], obj.get("priceMonthly"))
        purpose_type = from_union([PurposeTypeEnum, from_none], obj.get("purposeType"))
        type = from_union([from_none, ParkingType], obj.get("type"))
        return Parking(currency, is_free, location_type, places_count, price_monthly, purpose_type, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["currency"] = from_union([lambda x: to_enum(Currency, x), from_none], self.currency)
        result["isFree"] = from_union([from_none, from_bool], self.is_free)
        result["locationType"] = from_union([from_none, from_str], self.location_type)
        result["placesCount"] = from_union([from_int, from_none], self.places_count)
        result["priceMonthly"] = from_union([to_float, from_none], self.price_monthly)
        result["purposeType"] = from_union([lambda x: to_enum(PurposeTypeEnum, x), from_none], self.purpose_type)
        result["type"] = from_union([from_none, lambda x: to_enum(ParkingType, x)], self.type)
        return result


class StatusType(Enum):
    OPERATIONAL = "operational"
    PROJECT = "project"
    UNDER_CONSTRUCTION = "underConstruction"


class VentilationType(Enum):
    FORCED = "forced"
    NATURAL = "natural"
    NO = "no"


class Building:
    access_type: Optional[AccessTypeEnum]
    build_year: Optional[int]
    ceiling_height: Optional[str]
    class_type: Optional[ClassType]
    conditioning_type: Optional[ConditioningTypeEnum]
    condition_rating_type: Optional[str]
    cranage_types: Optional[List[CranageTypeElement]]
    developer: Optional[str]
    extinguishing_system_type: Optional[ExtinguishingSystemType]
    floors_count: Optional[int]
    gates_type: Optional[str]
    heating_type: Optional[HeatingType]
    house_line_type: Optional[HouseLineType]
    house_material_type: Optional[HouseMaterialType]
    infrastructure: Optional[Dict[str, bool]]
    lift_types: Optional[List[CranageTypeElement]]
    material_type: Optional[HouseMaterialType]
    name: Optional[str]
    opening_hours: Optional[OpeningHours]
    parking: Optional[Parking]
    shopping_center_scale_type: Optional[str]
    status_type: Optional[StatusType]
    tenants: Optional[str]
    total_area: Optional[str]
    type: Optional[str]
    ventilation_type: Optional[VentilationType]
    working_days_type: Optional[str]

    def __init__(self, access_type: Optional[AccessTypeEnum], build_year: Optional[int], ceiling_height: Optional[str], class_type: Optional[ClassType], conditioning_type: Optional[ConditioningTypeEnum], condition_rating_type: Optional[str], cranage_types: Optional[List[CranageTypeElement]], developer: Optional[str], extinguishing_system_type: Optional[ExtinguishingSystemType], floors_count: Optional[int], gates_type: Optional[str], heating_type: Optional[HeatingType], house_line_type: Optional[HouseLineType], house_material_type: Optional[HouseMaterialType], infrastructure: Optional[Dict[str, bool]], lift_types: Optional[List[CranageTypeElement]], material_type: Optional[HouseMaterialType], name: Optional[str], opening_hours: Optional[OpeningHours], parking: Optional[Parking], shopping_center_scale_type: Optional[str], status_type: Optional[StatusType], tenants: Optional[str], total_area: Optional[str], type: Optional[str], ventilation_type: Optional[VentilationType], working_days_type: Optional[str]) -> None:
        self.access_type = access_type
        self.build_year = build_year
        self.ceiling_height = ceiling_height
        self.class_type = class_type
        self.conditioning_type = conditioning_type
        self.condition_rating_type = condition_rating_type
        self.cranage_types = cranage_types
        self.developer = developer
        self.extinguishing_system_type = extinguishing_system_type
        self.floors_count = floors_count
        self.gates_type = gates_type
        self.heating_type = heating_type
        self.house_line_type = house_line_type
        self.house_material_type = house_material_type
        self.infrastructure = infrastructure
        self.lift_types = lift_types
        self.material_type = material_type
        self.name = name
        self.opening_hours = opening_hours
        self.parking = parking
        self.shopping_center_scale_type = shopping_center_scale_type
        self.status_type = status_type
        self.tenants = tenants
        self.total_area = total_area
        self.type = type
        self.ventilation_type = ventilation_type
        self.working_days_type = working_days_type

    @staticmethod
    def from_dict(obj: Any) -> 'Building':
        assert isinstance(obj, dict)
        access_type = from_union([from_none, AccessTypeEnum], obj.get("accessType"))
        build_year = from_union([from_int, from_none], obj.get("buildYear"))
        ceiling_height = from_union([from_str, from_none], obj.get("ceilingHeight"))
        class_type = from_union([ClassType, from_none], obj.get("classType"))
        conditioning_type = from_union([ConditioningTypeEnum, from_none], obj.get("conditioningType"))
        condition_rating_type = from_union([from_str, from_none], obj.get("conditionRatingType"))
        cranage_types = from_union([lambda x: from_list(CranageTypeElement.from_dict, x), from_none], obj.get("cranageTypes"))
        developer = from_union([from_str, from_none], obj.get("developer"))
        extinguishing_system_type = from_union([ExtinguishingSystemType, from_none], obj.get("extinguishingSystemType"))
        floors_count = from_union([from_int, from_none], obj.get("floorsCount"))
        gates_type = from_union([from_str, from_none], obj.get("gatesType"))
        heating_type = from_union([HeatingType, from_none], obj.get("heatingType"))
        house_line_type = from_union([HouseLineType, from_none], obj.get("houseLineType"))
        house_material_type = from_union([HouseMaterialType, from_none], obj.get("houseMaterialType"))
        infrastructure = from_union([lambda x: from_dict(from_bool, x), from_none], obj.get("infrastructure"))
        lift_types = from_union([lambda x: from_list(CranageTypeElement.from_dict, x), from_none], obj.get("liftTypes"))
        material_type = from_union([HouseMaterialType, from_none], obj.get("materialType"))
        name = from_union([from_str, from_none], obj.get("name"))
        opening_hours = from_union([OpeningHours.from_dict, from_none], obj.get("openingHours"))
        parking = from_union([Parking.from_dict, from_none], obj.get("parking"))
        shopping_center_scale_type = from_union([from_str, from_none], obj.get("shoppingCenterScaleType"))
        status_type = from_union([StatusType, from_none], obj.get("statusType"))
        tenants = from_union([from_str, from_none], obj.get("tenants"))
        total_area = from_union([from_none, from_str], obj.get("totalArea"))
        type = from_union([from_str, from_none], obj.get("type"))
        ventilation_type = from_union([VentilationType, from_none], obj.get("ventilationType"))
        working_days_type = from_union([from_str, from_none], obj.get("workingDaysType"))
        return Building(access_type, build_year, ceiling_height, class_type, conditioning_type, condition_rating_type, cranage_types, developer, extinguishing_system_type, floors_count, gates_type, heating_type, house_line_type, house_material_type, infrastructure, lift_types, material_type, name, opening_hours, parking, shopping_center_scale_type, status_type, tenants, total_area, type, ventilation_type, working_days_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["accessType"] = from_union([from_none, lambda x: to_enum(AccessTypeEnum, x)], self.access_type)
        result["buildYear"] = from_union([from_int, from_none], self.build_year)
        result["ceilingHeight"] = from_union([from_str, from_none], self.ceiling_height)
        result["classType"] = from_union([lambda x: to_enum(ClassType, x), from_none], self.class_type)
        result["conditioningType"] = from_union([lambda x: to_enum(ConditioningTypeEnum, x), from_none], self.conditioning_type)
        result["conditionRatingType"] = from_union([from_str, from_none], self.condition_rating_type)
        result["cranageTypes"] = from_union([lambda x: from_list(lambda x: to_class(CranageTypeElement, x), x), from_none], self.cranage_types)
        result["developer"] = from_union([from_str, from_none], self.developer)
        result["extinguishingSystemType"] = from_union([lambda x: to_enum(ExtinguishingSystemType, x), from_none], self.extinguishing_system_type)
        result["floorsCount"] = from_union([from_int, from_none], self.floors_count)
        result["gatesType"] = from_union([from_str, from_none], self.gates_type)
        result["heatingType"] = from_union([lambda x: to_enum(HeatingType, x), from_none], self.heating_type)
        result["houseLineType"] = from_union([lambda x: to_enum(HouseLineType, x), from_none], self.house_line_type)
        result["houseMaterialType"] = from_union([lambda x: to_enum(HouseMaterialType, x), from_none], self.house_material_type)
        result["infrastructure"] = from_union([lambda x: from_dict(from_bool, x), from_none], self.infrastructure)
        result["liftTypes"] = from_union([lambda x: from_list(lambda x: to_class(CranageTypeElement, x), x), from_none], self.lift_types)
        result["materialType"] = from_union([lambda x: to_enum(HouseMaterialType, x), from_none], self.material_type)
        result["name"] = from_union([from_str, from_none], self.name)
        result["openingHours"] = from_union([lambda x: to_class(OpeningHours, x), from_none], self.opening_hours)
        result["parking"] = from_union([lambda x: to_class(Parking, x), from_none], self.parking)
        result["shoppingCenterScaleType"] = from_union([from_str, from_none], self.shopping_center_scale_type)
        result["statusType"] = from_union([lambda x: to_enum(StatusType, x), from_none], self.status_type)
        result["tenants"] = from_union([from_str, from_none], self.tenants)
        result["totalArea"] = from_union([from_none, from_str], self.total_area)
        result["type"] = from_union([from_str, from_none], self.type)
        result["ventilationType"] = from_union([lambda x: to_enum(VentilationType, x), from_none], self.ventilation_type)
        result["workingDaysType"] = from_union([from_str, from_none], self.working_days_type)
        return result


class BusinessShoppingCenter:
    from_representative: bool
    id: int
    parent_id: Optional[int]
    parent_name: Optional[str]

    def __init__(self, from_representative: bool, id: int, parent_id: Optional[int], parent_name: Optional[str]) -> None:
        self.from_representative = from_representative
        self.id = id
        self.parent_id = parent_id
        self.parent_name = parent_name

    @staticmethod
    def from_dict(obj: Any) -> 'BusinessShoppingCenter':
        assert isinstance(obj, dict)
        from_representative = from_bool(obj.get("fromRepresentative"))
        id = from_int(obj.get("id"))
        parent_id = from_union([from_int, from_none], obj.get("parentId"))
        parent_name = from_union([from_str, from_none], obj.get("parentName"))
        return BusinessShoppingCenter(from_representative, id, parent_id, parent_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fromRepresentative"] = from_bool(self.from_representative)
        result["id"] = from_int(self.id)
        result["parentId"] = from_union([from_int, from_none], self.parent_id)
        result["parentName"] = from_union([from_str, from_none], self.parent_name)
        return result


class CallTrackingProvider(Enum):
    MTS = "mts"


class Category(Enum):
    BUILDING_SALE = "buildingSale"
    BUSINESS_SALE = "businessSale"
    COMMERCIAL_LAND_SALE = "commercialLandSale"
    FLAT_RENT = "flatRent"
    FREE_APPOINTMENT_OBJECT_SALE = "freeAppointmentObjectSale"
    GARAGE_SALE = "garageSale"
    INDUSTRY_SALE = "industrySale"
    OFFICE_SALE = "officeSale"
    SHOPPING_AREA_SALE = "shoppingAreaSale"
    WAREHOUSE_SALE = "warehouseSale"


class ConditionType(Enum):
    COSMETIC_REPAIRS_REQUIRED = "cosmeticRepairsRequired"
    DESIGN = "design"
    FINISHING = "finishing"
    MAJOR_REPAIRS_REQUIRED = "majorRepairsRequired"
    OFFICE = "office"
    TYPICAL = "typical"


class Decoration(Enum):
    FINE = "fine"
    ROUGH = "rough"
    WITHOUT = "without"


class DrivewayType(Enum):
    ASPHALT = "asphalt"
    GROUND = "ground"
    NO = "no"


class Electricity:
    location_type: Optional[ConditioningTypeEnum]
    possible_to_connect: Optional[bool]
    power: Optional[int]

    def __init__(self, location_type: Optional[ConditioningTypeEnum], possible_to_connect: Optional[bool], power: Optional[int]) -> None:
        self.location_type = location_type
        self.possible_to_connect = possible_to_connect
        self.power = power

    @staticmethod
    def from_dict(obj: Any) -> 'Electricity':
        assert isinstance(obj, dict)
        location_type = from_union([ConditioningTypeEnum, from_none], obj.get("locationType"))
        possible_to_connect = from_union([from_none, from_bool], obj.get("possibleToConnect"))
        power = from_union([from_int, from_none], obj.get("power"))
        return Electricity(location_type, possible_to_connect, power)

    def to_dict(self) -> dict:
        result: dict = {}
        result["locationType"] = from_union([lambda x: to_enum(ConditioningTypeEnum, x), from_none], self.location_type)
        result["possibleToConnect"] = from_union([from_none, from_bool], self.possible_to_connect)
        result["power"] = from_union([from_int, from_none], self.power)
        return result


class EstateTypeEnum(Enum):
    OWNED = "owned"
    RENT = "rent"


class Flags:
    is_archived: bool

    def __init__(self, is_archived: bool) -> None:
        self.is_archived = is_archived

    @staticmethod
    def from_dict(obj: Any) -> 'Flags':
        assert isinstance(obj, dict)
        is_archived = from_bool(obj.get("isArchived"))
        return Flags(is_archived)

    def to_dict(self) -> dict:
        result: dict = {}
        result["isArchived"] = from_bool(self.is_archived)
        return result


class GarageType(Enum):
    BUILT_IN = "builtIn"
    CAPITAL = "capital"
    SAMOSTROY = "samostroy"
    SHELL = "shell"


class GarageStatus(Enum):
    BY_PROXY = "byProxy"
    COOPERATIVE = "cooperative"
    OWNERSHIP = "ownership"


class GarageTypeEnum(Enum):
    BOX = "box"
    GARAGE = "garage"
    PARKING_PLACE = "parkingPlace"


class Garage:
    garage_type: Optional[GarageType]
    material: Optional[HouseMaterialType]
    status: Optional[GarageStatus]
    type: Optional[GarageTypeEnum]

    def __init__(self, garage_type: Optional[GarageType], material: Optional[HouseMaterialType], status: Optional[GarageStatus], type: Optional[GarageTypeEnum]) -> None:
        self.garage_type = garage_type
        self.material = material
        self.status = status
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Garage':
        assert isinstance(obj, dict)
        garage_type = from_union([from_none, GarageType], obj.get("garageType"))
        material = from_union([HouseMaterialType, from_none], obj.get("material"))
        status = from_union([from_none, GarageStatus], obj.get("status"))
        type = from_union([GarageTypeEnum, from_none], obj.get("type"))
        return Garage(garage_type, material, status, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["garageType"] = from_union([from_none, lambda x: to_enum(GarageType, x)], self.garage_type)
        result["material"] = from_union([lambda x: to_enum(HouseMaterialType, x), from_none], self.material)
        result["status"] = from_union([from_none, lambda x: to_enum(GarageStatus, x)], self.status)
        result["type"] = from_union([lambda x: to_enum(GarageTypeEnum, x), from_none], self.type)
        return result


class PressureType(Enum):
    HIGH = "high"
    LOW = "low"
    MIDDLE = "middle"


class Gas:
    capacity: Optional[int]
    location_type: Optional[ConditioningTypeEnum]
    possible_to_connect: Optional[bool]
    pressure_type: Optional[PressureType]

    def __init__(self, capacity: Optional[int], location_type: Optional[ConditioningTypeEnum], possible_to_connect: Optional[bool], pressure_type: Optional[PressureType]) -> None:
        self.capacity = capacity
        self.location_type = location_type
        self.possible_to_connect = possible_to_connect
        self.pressure_type = pressure_type

    @staticmethod
    def from_dict(obj: Any) -> 'Gas':
        assert isinstance(obj, dict)
        capacity = from_union([from_int, from_none], obj.get("capacity"))
        location_type = from_union([ConditioningTypeEnum, from_none], obj.get("locationType"))
        possible_to_connect = from_union([from_none, from_bool], obj.get("possibleToConnect"))
        pressure_type = from_union([from_none, PressureType], obj.get("pressureType"))
        return Gas(capacity, location_type, possible_to_connect, pressure_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["capacity"] = from_union([from_int, from_none], self.capacity)
        result["locationType"] = from_union([lambda x: to_enum(ConditioningTypeEnum, x), from_none], self.location_type)
        result["possibleToConnect"] = from_union([from_none, from_bool], self.possible_to_connect)
        result["pressureType"] = from_union([from_none, lambda x: to_enum(PressureType, x)], self.pressure_type)
        return result


class AddressType(Enum):
    HOUSE = "house"
    LOCATION = "location"
    METRO = "metro"
    MIKRORAION = "mikroraion"
    OKRUG = "okrug"
    POSELENIE = "poselenie"
    RAION = "raion"
    STREET = "street"


class Address:
    full_name: str
    id: int
    is_forming_address: Optional[bool]
    location_type_id: Optional[int]
    name: str
    short_name: str
    type: AddressType

    def __init__(self, full_name: str, id: int, is_forming_address: Optional[bool], location_type_id: Optional[int], name: str, short_name: str, type: AddressType) -> None:
        self.full_name = full_name
        self.id = id
        self.is_forming_address = is_forming_address
        self.location_type_id = location_type_id
        self.name = name
        self.short_name = short_name
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Address':
        assert isinstance(obj, dict)
        full_name = from_str(obj.get("fullName"))
        id = from_int(obj.get("id"))
        is_forming_address = from_union([from_none, from_bool], obj.get("isFormingAddress"))
        location_type_id = from_union([from_int, from_none], obj.get("locationTypeId"))
        name = from_str(obj.get("name"))
        short_name = from_str(obj.get("shortName"))
        type = AddressType(obj.get("type"))
        return Address(full_name, id, is_forming_address, location_type_id, name, short_name, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fullName"] = from_str(self.full_name)
        result["id"] = from_int(self.id)
        result["isFormingAddress"] = from_union([from_none, from_bool], self.is_forming_address)
        result["locationTypeId"] = from_union([from_int, from_none], self.location_type_id)
        result["name"] = from_str(self.name)
        result["shortName"] = from_str(self.short_name)
        result["type"] = to_enum(AddressType, self.type)
        return result


class CoordinatesClass:
    lat: float
    lng: float

    def __init__(self, lat: float, lng: float) -> None:
        self.lat = lat
        self.lng = lng

    @staticmethod
    def from_dict(obj: Any) -> 'CoordinatesClass':
        assert isinstance(obj, dict)
        lat = from_float(obj.get("lat"))
        lng = from_float(obj.get("lng"))
        return CoordinatesClass(lat, lng)

    def to_dict(self) -> dict:
        result: dict = {}
        result["lat"] = to_float(self.lat)
        result["lng"] = to_float(self.lng)
        return result


class DistrictType(Enum):
    MIKRORAION = "mikroraion"
    OKRUG = "okrug"
    POSELENIE = "poselenie"
    RAION = "raion"


class District:
    id: int
    location_id: int
    name: str
    parent_id: Optional[int]
    type: DistrictType

    def __init__(self, id: int, location_id: int, name: str, parent_id: Optional[int], type: DistrictType) -> None:
        self.id = id
        self.location_id = location_id
        self.name = name
        self.parent_id = parent_id
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'District':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        location_id = from_int(obj.get("locationId"))
        name = from_str(obj.get("name"))
        parent_id = from_union([from_int, from_none], obj.get("parentId"))
        type = DistrictType(obj.get("type"))
        return District(id, location_id, name, parent_id, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["locationId"] = from_int(self.location_id)
        result["name"] = from_str(self.name)
        result["parentId"] = from_union([from_int, from_none], self.parent_id)
        result["type"] = to_enum(DistrictType, self.type)
        return result


class Highway:
    distance: str
    id: int
    is_default: Optional[bool]
    name: str

    def __init__(self, distance: str, id: int, is_default: Optional[bool], name: str) -> None:
        self.distance = distance
        self.id = id
        self.is_default = is_default
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'Highway':
        assert isinstance(obj, dict)
        distance = from_str(obj.get("distance"))
        id = from_int(obj.get("id"))
        is_default = from_union([from_none, from_bool], obj.get("isDefault"))
        name = from_str(obj.get("name"))
        return Highway(distance, id, is_default, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["distance"] = from_str(self.distance)
        result["id"] = from_int(self.id)
        result["isDefault"] = from_union([from_none, from_bool], self.is_default)
        result["name"] = from_str(self.name)
        return result


class GaGeo:
    city_id: int
    mo_id: int
    obl_id: int

    def __init__(self, city_id: int, mo_id: int, obl_id: int) -> None:
        self.city_id = city_id
        self.mo_id = mo_id
        self.obl_id = obl_id

    @staticmethod
    def from_dict(obj: Any) -> 'GaGeo':
        assert isinstance(obj, dict)
        city_id = from_int(obj.get("cityId"))
        mo_id = from_int(obj.get("moId"))
        obl_id = from_int(obj.get("oblId"))
        return GaGeo(city_id, mo_id, obl_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cityId"] = from_int(self.city_id)
        result["moId"] = from_int(self.mo_id)
        result["oblId"] = from_int(self.obl_id)
        return result


class JkHouse:
    id: int
    name: str

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'JkHouse':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        return JkHouse(id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        return result


class Jk:
    display_name: str
    full_url: Optional[str]
    ga_geo: Optional[GaGeo]
    house: Optional[JkHouse]
    id: int
    name: str
    web_site_url: Optional[str]
    web_site_url_utm: Optional[str]

    def __init__(self, display_name: str, full_url: Optional[str], ga_geo: Optional[GaGeo], house: Optional[JkHouse], id: int, name: str, web_site_url: Optional[str], web_site_url_utm: Optional[str]) -> None:
        self.display_name = display_name
        self.full_url = full_url
        self.ga_geo = ga_geo
        self.house = house
        self.id = id
        self.name = name
        self.web_site_url = web_site_url
        self.web_site_url_utm = web_site_url_utm

    @staticmethod
    def from_dict(obj: Any) -> 'Jk':
        assert isinstance(obj, dict)
        display_name = from_str(obj.get("displayName"))
        full_url = from_union([from_str, from_none], obj.get("fullUrl"))
        ga_geo = from_union([GaGeo.from_dict, from_none], obj.get("gaGeo"))
        house = from_union([JkHouse.from_dict, from_none], obj.get("house"))
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        web_site_url = from_union([from_str, from_none], obj.get("webSiteUrl"))
        web_site_url_utm = from_union([from_str, from_none], obj.get("webSiteUrlUtm"))
        return Jk(display_name, full_url, ga_geo, house, id, name, web_site_url, web_site_url_utm)

    def to_dict(self) -> dict:
        result: dict = {}
        result["displayName"] = from_str(self.display_name)
        result["fullUrl"] = from_union([from_str, from_none], self.full_url)
        result["gaGeo"] = from_union([lambda x: to_class(GaGeo, x), from_none], self.ga_geo)
        result["house"] = from_union([lambda x: to_class(JkHouse, x), from_none], self.house)
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        result["webSiteUrl"] = from_union([from_str, from_none], self.web_site_url)
        result["webSiteUrlUtm"] = from_union([from_str, from_none], self.web_site_url_utm)
        return result


class LocationPath:
    child_to_parent: List[int]
    country_id: int

    def __init__(self, child_to_parent: List[int], country_id: int) -> None:
        self.child_to_parent = child_to_parent
        self.country_id = country_id

    @staticmethod
    def from_dict(obj: Any) -> 'LocationPath':
        assert isinstance(obj, dict)
        child_to_parent = from_list(from_int, obj.get("childToParent"))
        country_id = from_int(obj.get("countryId"))
        return LocationPath(child_to_parent, country_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["childToParent"] = from_list(from_int, self.child_to_parent)
        result["countryId"] = from_int(self.country_id)
        return result


class TransportType(Enum):
    TRANSPORT = "transport"
    WALK = "walk"


class Underground:
    id: int
    is_default: Optional[bool]
    line_color: str
    line_id: int
    name: str
    release_year: Optional[int]
    time: Optional[int]
    transport_type: TransportType
    under_construction: bool

    def __init__(self, id: int, is_default: Optional[bool], line_color: str, line_id: int, name: str, release_year: Optional[int], time: Optional[int], transport_type: TransportType, under_construction: bool) -> None:
        self.id = id
        self.is_default = is_default
        self.line_color = line_color
        self.line_id = line_id
        self.name = name
        self.release_year = release_year
        self.time = time
        self.transport_type = transport_type
        self.under_construction = under_construction

    @staticmethod
    def from_dict(obj: Any) -> 'Underground':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        is_default = from_union([from_none, from_bool], obj.get("isDefault"))
        line_color = from_str(obj.get("lineColor"))
        line_id = from_int(obj.get("lineId"))
        name = from_str(obj.get("name"))
        release_year = from_union([from_int, from_none], obj.get("releaseYear"))
        time = from_union([from_int, from_none], obj.get("time"))
        transport_type = TransportType(obj.get("transportType"))
        under_construction = from_bool(obj.get("underConstruction"))
        return Underground(id, is_default, line_color, line_id, name, release_year, time, transport_type, under_construction)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["isDefault"] = from_union([from_none, from_bool], self.is_default)
        result["lineColor"] = from_str(self.line_color)
        result["lineId"] = from_int(self.line_id)
        result["name"] = from_str(self.name)
        result["releaseYear"] = from_union([from_int, from_none], self.release_year)
        result["time"] = from_union([from_int, from_none], self.time)
        result["transportType"] = to_enum(TransportType, self.transport_type)
        result["underConstruction"] = from_bool(self.under_construction)
        return result


class OffersSerializedGeo:
    address: List[Address]
    coordinates: CoordinatesClass
    country_id: int
    districts: List[District]
    highways: List[Highway]
    jk: Optional[Jk]
    location_path: Optional[LocationPath]
    undergrounds: List[Underground]
    user_input: str

    def __init__(self, address: List[Address], coordinates: CoordinatesClass, country_id: int, districts: List[District], highways: List[Highway], jk: Optional[Jk], location_path: Optional[LocationPath], undergrounds: List[Underground], user_input: str) -> None:
        self.address = address
        self.coordinates = coordinates
        self.country_id = country_id
        self.districts = districts
        self.highways = highways
        self.jk = jk
        self.location_path = location_path
        self.undergrounds = undergrounds
        self.user_input = user_input

    @staticmethod
    def from_dict(obj: Any) -> 'OffersSerializedGeo':
        assert isinstance(obj, dict)
        address = from_list(Address.from_dict, obj.get("address"))
        coordinates = CoordinatesClass.from_dict(obj.get("coordinates"))
        country_id = from_int(obj.get("countryId"))
        districts = from_list(District.from_dict, obj.get("districts"))
        highways = from_list(Highway.from_dict, obj.get("highways"))
        jk = from_union([Jk.from_dict, from_none], obj.get("jk"))
        location_path = from_union([LocationPath.from_dict, from_none], obj.get("locationPath"))
        undergrounds = from_list(Underground.from_dict, obj.get("undergrounds"))
        user_input = from_str(obj.get("userInput"))
        return OffersSerializedGeo(address, coordinates, country_id, districts, highways, jk, location_path, undergrounds, user_input)

    def to_dict(self) -> dict:
        result: dict = {}
        result["address"] = from_list(lambda x: to_class(Address, x), self.address)
        result["coordinates"] = to_class(CoordinatesClass, self.coordinates)
        result["countryId"] = from_int(self.country_id)
        result["districts"] = from_list(lambda x: to_class(District, x), self.districts)
        result["highways"] = from_list(lambda x: to_class(Highway, x), self.highways)
        result["jk"] = from_union([lambda x: to_class(Jk, x), from_none], self.jk)
        result["locationPath"] = from_union([lambda x: to_class(LocationPath, x), from_none], self.location_path)
        result["undergrounds"] = from_list(lambda x: to_class(Underground, x), self.undergrounds)
        result["userInput"] = from_str(self.user_input)
        return result


class InputType(Enum):
    COMMON_FROM_STREET = "commonFromStreet"
    COMMON_FROM_YARD = "commonFromYard"
    SEPARATE_FROM_STREET = "separateFromStreet"
    SEPARATE_FROM_YARD = "separateFromYard"


class AreaUnitType(Enum):
    HECTARE = "hectare"
    SOTKA = "sotka"


class LandStatus(Enum):
    FOR_AGRICULTURAL_PURPOSES = "forAgriculturalPurposes"
    INDUSTRY_TRANSPORT_COMMUNICATIONS = "industryTransportCommunications"
    SETTLEMENTS = "settlements"


class Land:
    area: Optional[str]
    area_unit_type: Optional[AreaUnitType]
    possible_to_change_status: Optional[bool]
    status: Optional[LandStatus]
    type: Optional[EstateTypeEnum]

    def __init__(self, area: Optional[str], area_unit_type: Optional[AreaUnitType], possible_to_change_status: Optional[bool], status: Optional[LandStatus], type: Optional[EstateTypeEnum]) -> None:
        self.area = area
        self.area_unit_type = area_unit_type
        self.possible_to_change_status = possible_to_change_status
        self.status = status
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Land':
        assert isinstance(obj, dict)
        area = from_union([from_none, from_str], obj.get("area"))
        area_unit_type = from_union([from_none, AreaUnitType], obj.get("areaUnitType"))
        possible_to_change_status = from_union([from_none, from_bool], obj.get("possibleToChangeStatus"))
        status = from_union([from_none, LandStatus], obj.get("status"))
        type = from_union([from_none, EstateTypeEnum], obj.get("type"))
        return Land(area, area_unit_type, possible_to_change_status, status, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["area"] = from_union([from_none, from_str], self.area)
        result["areaUnitType"] = from_union([from_none, lambda x: to_enum(AreaUnitType, x)], self.area_unit_type)
        result["possibleToChangeStatus"] = from_union([from_none, from_bool], self.possible_to_change_status)
        result["status"] = from_union([from_none, lambda x: to_enum(LandStatus, x)], self.status)
        result["type"] = from_union([from_none, lambda x: to_enum(EstateTypeEnum, x)], self.type)
        return result


class Layout(Enum):
    CABINET = "cabinet"
    CORRIDORPLAN = "corridorplan"
    MIXED = "mixed"
    OPEN_SPACE = "openSpace"


class MonthlyIncome:
    currency: Currency
    income: Optional[int]

    def __init__(self, currency: Currency, income: Optional[int]) -> None:
        self.currency = currency
        self.income = income

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


class FinishDate:
    quarter: int
    year: int

    def __init__(self, quarter: int, year: int) -> None:
        self.quarter = quarter
        self.year = year

    @staticmethod
    def from_dict(obj: Any) -> 'FinishDate':
        assert isinstance(obj, dict)
        quarter = from_int(obj.get("quarter"))
        year = from_int(obj.get("year"))
        return FinishDate(quarter, year)

    def to_dict(self) -> dict:
        result: dict = {}
        result["quarter"] = from_int(self.quarter)
        result["year"] = from_int(self.year)
        return result


class NewbuildingHouse:
    finish_date: Optional[FinishDate]
    id: int
    is_finished: bool
    is_reliable: bool
    name: str

    def __init__(self, finish_date: Optional[FinishDate], id: int, is_finished: bool, is_reliable: bool, name: str) -> None:
        self.finish_date = finish_date
        self.id = id
        self.is_finished = is_finished
        self.is_reliable = is_reliable
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'NewbuildingHouse':
        assert isinstance(obj, dict)
        finish_date = from_union([FinishDate.from_dict, from_none], obj.get("finishDate"))
        id = from_int(obj.get("id"))
        is_finished = from_bool(obj.get("isFinished"))
        is_reliable = from_bool(obj.get("isReliable"))
        name = from_str(obj.get("name"))
        return NewbuildingHouse(finish_date, id, is_finished, is_reliable, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["finishDate"] = from_union([lambda x: to_class(FinishDate, x), from_none], self.finish_date)
        result["id"] = from_int(self.id)
        result["isFinished"] = from_bool(self.is_finished)
        result["isReliable"] = from_bool(self.is_reliable)
        result["name"] = from_str(self.name)
        return result


class NewbuildingFeatures:
    deadline_info: str
    first_image_url: str
    images_count: int
    reviews_count: int
    videos_count: int

    def __init__(self, deadline_info: str, first_image_url: str, images_count: int, reviews_count: int, videos_count: int) -> None:
        self.deadline_info = deadline_info
        self.first_image_url = first_image_url
        self.images_count = images_count
        self.reviews_count = reviews_count
        self.videos_count = videos_count

    @staticmethod
    def from_dict(obj: Any) -> 'NewbuildingFeatures':
        assert isinstance(obj, dict)
        deadline_info = from_str(obj.get("deadlineInfo"))
        first_image_url = from_str(obj.get("firstImageUrl"))
        images_count = from_int(obj.get("imagesCount"))
        reviews_count = from_int(obj.get("reviewsCount"))
        videos_count = from_int(obj.get("videosCount"))
        return NewbuildingFeatures(deadline_info, first_image_url, images_count, reviews_count, videos_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["deadlineInfo"] = from_str(self.deadline_info)
        result["firstImageUrl"] = from_str(self.first_image_url)
        result["imagesCount"] = from_int(self.images_count)
        result["reviewsCount"] = from_int(self.reviews_count)
        result["videosCount"] = from_int(self.videos_count)
        return result


class Newbuilding:
    house: Optional[NewbuildingHouse]
    id: int
    is_from_builder: Optional[bool]
    is_from_developer: Optional[bool]
    is_from_seller: Optional[bool]
    is_reliable: Optional[bool]
    name: str
    newbuilding_features: Optional[NewbuildingFeatures]
    show_jk_reliable_flag: Optional[bool]

    def __init__(self, house: Optional[NewbuildingHouse], id: int, is_from_builder: Optional[bool], is_from_developer: Optional[bool], is_from_seller: Optional[bool], is_reliable: Optional[bool], name: str, newbuilding_features: Optional[NewbuildingFeatures], show_jk_reliable_flag: Optional[bool]) -> None:
        self.house = house
        self.id = id
        self.is_from_builder = is_from_builder
        self.is_from_developer = is_from_developer
        self.is_from_seller = is_from_seller
        self.is_reliable = is_reliable
        self.name = name
        self.newbuilding_features = newbuilding_features
        self.show_jk_reliable_flag = show_jk_reliable_flag

    @staticmethod
    def from_dict(obj: Any) -> 'Newbuilding':
        assert isinstance(obj, dict)
        house = from_union([NewbuildingHouse.from_dict, from_none], obj.get("house"))
        id = from_int(obj.get("id"))
        is_from_builder = from_union([from_none, from_bool], obj.get("isFromBuilder"))
        is_from_developer = from_union([from_none, from_bool], obj.get("isFromDeveloper"))
        is_from_seller = from_union([from_none, from_bool], obj.get("isFromSeller"))
        is_reliable = from_union([from_none, from_bool], obj.get("isReliable"))
        name = from_str(obj.get("name"))
        newbuilding_features = from_union([NewbuildingFeatures.from_dict, from_none], obj.get("newbuildingFeatures"))
        show_jk_reliable_flag = from_union([from_none, from_bool], obj.get("showJkReliableFlag"))
        return Newbuilding(house, id, is_from_builder, is_from_developer, is_from_seller, is_reliable, name, newbuilding_features, show_jk_reliable_flag)

    def to_dict(self) -> dict:
        result: dict = {}
        result["house"] = from_union([lambda x: to_class(NewbuildingHouse, x), from_none], self.house)
        result["id"] = from_int(self.id)
        result["isFromBuilder"] = from_union([from_none, from_bool], self.is_from_builder)
        result["isFromDeveloper"] = from_union([from_none, from_bool], self.is_from_developer)
        result["isFromSeller"] = from_union([from_none, from_bool], self.is_from_seller)
        result["isReliable"] = from_union([from_none, from_bool], self.is_reliable)
        result["name"] = from_str(self.name)
        result["newbuildingFeatures"] = from_union([lambda x: to_class(NewbuildingFeatures, x), from_none], self.newbuilding_features)
        result["showJkReliableFlag"] = from_union([from_none, from_bool], self.show_jk_reliable_flag)
        return result


class Notes:
    offer: Optional[str]
    realtor: Optional[str]

    def __init__(self, offer: Optional[str], realtor: Optional[str]) -> None:
        self.offer = offer
        self.realtor = realtor

    @staticmethod
    def from_dict(obj: Any) -> 'Notes':
        assert isinstance(obj, dict)
        offer = from_union([from_none, from_str], obj.get("offer"))
        realtor = from_union([from_none, from_str], obj.get("realtor"))
        return Notes(offer, realtor)

    def to_dict(self) -> dict:
        result: dict = {}
        result["offer"] = from_union([from_none, from_str], self.offer)
        result["realtor"] = from_union([from_none, from_str], self.realtor)
        return result


class OfferType(Enum):
    COMMERCIAL = "commercial"


class PermittedUseType(Enum):
    AGRICULTURAL = "agricultural"
    BUSINESS_MANAGEMENT = "businessManagement"
    COMMON_USE_AREA = "commonUseArea"
    HIGHRISE_BUILDINGS = "highriseBuildings"
    HOTEL_AMENITIES = "hotelAmenities"
    INDIVIDUAL_HOUSING_CONSTRUCTION = "individualHousingConstruction"
    INDUSTRY = "industry"
    LOWRISE_HOUSING = "lowriseHousing"
    PUBLIC_USE_OF_CAPITAL_CONSTRUCTION = "publicUseOfCapitalConstruction"
    SERVICE_VEHICLES = "serviceVehicles"
    SHOPPING_CENTERS = "shoppingCenters"
    WAREHOUSES = "warehouses"


class Phone:
    country_code: str
    number: str

    def __init__(self, country_code: str, number: str) -> None:
        self.country_code = country_code
        self.number = number

    @staticmethod
    def from_dict(obj: Any) -> 'Phone':
        assert isinstance(obj, dict)
        country_code = from_str(obj.get("countryCode"))
        number = from_str(obj.get("number"))
        return Phone(country_code, number)

    def to_dict(self) -> dict:
        result: dict = {}
        result["countryCode"] = from_str(self.country_code)
        result["number"] = from_str(self.number)
        return result


class Coordinates:
    lat: float
    lng: float

    def __init__(self, lat: float, lng: float) -> None:
        self.lat = lat
        self.lng = lng

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


class Photo:
    coordinates: Optional[Coordinates]
    full_url: str
    id: int
    is_default: bool
    mini_url: str
    source: Optional[str]
    thumbnail2_url: str
    thumbnail_url: str

    def __init__(self, coordinates: Optional[Coordinates], full_url: str, id: int, is_default: bool, mini_url: str, source: Optional[str], thumbnail2_url: str, thumbnail_url: str) -> None:
        self.coordinates = coordinates
        self.full_url = full_url
        self.id = id
        self.is_default = is_default
        self.mini_url = mini_url
        self.source = source
        self.thumbnail2_url = thumbnail2_url
        self.thumbnail_url = thumbnail_url

    @staticmethod
    def from_dict(obj: Any) -> 'Photo':
        assert isinstance(obj, dict)
        coordinates = from_union([Coordinates.from_dict, from_none], obj.get("coordinates"))
        full_url = from_str(obj.get("fullUrl"))
        id = from_int(obj.get("id"))
        is_default = from_bool(obj.get("isDefault"))
        mini_url = from_str(obj.get("miniUrl"))
        source = from_union([from_none, from_str], obj.get("source"))
        thumbnail2_url = from_str(obj.get("thumbnail2Url"))
        thumbnail_url = from_str(obj.get("thumbnailUrl"))
        return Photo(coordinates, full_url, id, is_default, mini_url, source, thumbnail2_url, thumbnail_url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["coordinates"] = from_union([lambda x: to_class(Coordinates, x), from_none], self.coordinates)
        result["fullUrl"] = from_str(self.full_url)
        result["id"] = from_int(self.id)
        result["isDefault"] = from_bool(self.is_default)
        result["miniUrl"] = from_str(self.mini_url)
        result["source"] = from_union([from_none, from_str], self.source)
        result["thumbnail2Url"] = from_str(self.thumbnail2_url)
        result["thumbnailUrl"] = from_str(self.thumbnail_url)
        return result


class PlacementType(Enum):
    SHOPPING_MALL = "shoppingMall"
    STREET_RETAIL = "streetRetail"


class PlatformType(Enum):
    ANDROID = "android"
    IOS = "ios"
    UPLOAD = "upload"
    WEB_SITE = "webSite"


class Platform:
    type: PlatformType
    version: Optional[str]

    def __init__(self, type: PlatformType, version: Optional[str]) -> None:
        self.type = type
        self.version = version

    @staticmethod
    def from_dict(obj: Any) -> 'Platform':
        assert isinstance(obj, dict)
        type = PlatformType(obj.get("type"))
        version = from_union([from_none, from_str], obj.get("version"))
        return Platform(type, version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = to_enum(PlatformType, self.type)
        result["version"] = from_union([from_none, from_str], self.version)
        return result


class PriceData:
    currency: Currency
    payment_period: Optional[str]
    price: int

    def __init__(self, currency: Currency, payment_period: Optional[str], price: int) -> None:
        self.currency = currency
        self.payment_period = payment_period
        self.price = price

    @staticmethod
    def from_dict(obj: Any) -> 'PriceData':
        assert isinstance(obj, dict)
        currency = Currency(obj.get("currency"))
        payment_period = from_union([from_none, from_str], obj.get("paymentPeriod"))
        price = from_int(obj.get("price"))
        return PriceData(currency, payment_period, price)

    def to_dict(self) -> dict:
        result: dict = {}
        result["currency"] = to_enum(Currency, self.currency)
        result["paymentPeriod"] = from_union([from_none, from_str], self.payment_period)
        result["price"] = from_int(self.price)
        return result


class PriceChange:
    change_time: datetime
    price_data: PriceData

    def __init__(self, change_time: datetime, price_data: PriceData) -> None:
        self.change_time = change_time
        self.price_data = price_data

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


class PropertyType(Enum):
    BUILDING = "building"
    FREE_APPOINTMENT = "freeAppointment"
    GARAGE = "garage"
    INDUSTRY = "industry"
    LAND = "land"
    OFFICE = "office"
    SHOPPING_AREA = "shoppingArea"
    WAREHOUSE = "warehouse"


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


class Term:
    days: int
    dynamic_price: Optional[str]
    is_compulsory: Optional[bool]
    services: List[Service]
    tariff_identificator: Optional[int]
    type: TermType

    def __init__(self, days: int, dynamic_price: Optional[str], is_compulsory: Optional[bool], services: List[Service], tariff_identificator: Optional[int], type: TermType) -> None:
        self.days = days
        self.dynamic_price = dynamic_price
        self.is_compulsory = is_compulsory
        self.services = services
        self.tariff_identificator = tariff_identificator
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Term':
        assert isinstance(obj, dict)
        days = from_int(obj.get("days"))
        dynamic_price = from_union([from_none, from_str], obj.get("dynamicPrice"))
        is_compulsory = from_union([from_none, from_bool], obj.get("isCompulsory"))
        services = from_list(Service, obj.get("services"))
        tariff_identificator = from_union([from_int, from_none], obj.get("tariffIdentificator"))
        type = TermType(obj.get("type"))
        return Term(days, dynamic_price, is_compulsory, services, tariff_identificator, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["days"] = from_int(self.days)
        result["dynamicPrice"] = from_union([from_none, from_str], self.dynamic_price)
        result["isCompulsory"] = from_union([from_none, from_bool], self.is_compulsory)
        result["services"] = from_list(lambda x: to_enum(Service, x), self.services)
        result["tariffIdentificator"] = from_union([from_int, from_none], self.tariff_identificator)
        result["type"] = to_enum(TermType, self.type)
        return result


class PublishTerms:
    autoprolong: bool
    terms: List[Term]

    def __init__(self, autoprolong: bool, terms: List[Term]) -> None:
        self.autoprolong = autoprolong
        self.terms = terms

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


class RepairType(Enum):
    COSMETIC = "cosmetic"
    DESIGN = "design"
    EURO = "euro"
    NO = "no"


class SpecialtyElement:
    eng_name: str
    id: int
    rus_name: str

    def __init__(self, eng_name: str, id: int, rus_name: str) -> None:
        self.eng_name = eng_name
        self.id = id
        self.rus_name = rus_name

    @staticmethod
    def from_dict(obj: Any) -> 'SpecialtyElement':
        assert isinstance(obj, dict)
        eng_name = from_str(obj.get("engName"))
        id = from_int(obj.get("id"))
        rus_name = from_str(obj.get("rusName"))
        return SpecialtyElement(eng_name, id, rus_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["engName"] = from_str(self.eng_name)
        result["id"] = from_int(self.id)
        result["rusName"] = from_str(self.rus_name)
        return result


class OffersSerializedSpecialty:
    additional_types: List[str]
    specialties: Optional[List[SpecialtyElement]]
    types: List[str]

    def __init__(self, additional_types: List[str], specialties: Optional[List[SpecialtyElement]], types: List[str]) -> None:
        self.additional_types = additional_types
        self.specialties = specialties
        self.types = types

    @staticmethod
    def from_dict(obj: Any) -> 'OffersSerializedSpecialty':
        assert isinstance(obj, dict)
        additional_types = from_list(from_str, obj.get("additionalTypes"))
        specialties = from_union([lambda x: from_list(SpecialtyElement.from_dict, x), from_none], obj.get("specialties"))
        types = from_list(from_str, obj.get("types"))
        return OffersSerializedSpecialty(additional_types, specialties, types)

    def to_dict(self) -> dict:
        result: dict = {}
        result["additionalTypes"] = from_list(from_str, self.additional_types)
        result["specialties"] = from_union([lambda x: from_list(lambda x: to_class(SpecialtyElement, x), x), from_none], self.specialties)
        result["types"] = from_list(from_str, self.types)
        return result


class Statistic:
    daily: int
    total: int

    def __init__(self, daily: int, total: int) -> None:
        self.daily = daily
        self.total = total

    @staticmethod
    def from_dict(obj: Any) -> 'Statistic':
        assert isinstance(obj, dict)
        daily = from_int(obj.get("daily"))
        total = from_int(obj.get("total"))
        return Statistic(daily, total)

    def to_dict(self) -> dict:
        result: dict = {}
        result["daily"] = from_int(self.daily)
        result["total"] = from_int(self.total)
        return result


class Status(Enum):
    PUBLISHED = "published"


class AgentAccountType(Enum):
    AGENCY = "agency"
    MANAGEMENT_COMPANY = "managementCompany"
    RENT_DEPARTMENT = "rentDepartment"
    SPECIALIST = "specialist"


class Message(Enum):
    НАПИШИТЕ_ЕМУ_ИЛИ_ПОЗВОНИТЕ_В_РАБОЧЕЕ_ВРЕМЯ = "Напишите ему или позвоните в рабочее время."
    НАПИШИТЕ_ЕМУ_ИЛИ_ПОЗВОНИТЕ_ЗАВТРА = "Напишите ему или позвоните завтра."


class AgentAvailability:
    available: bool
    available_from: Optional[datetime]
    available_to: Optional[datetime]
    message: Optional[Message]
    title: Optional[str]
    user_id: int

    def __init__(self, available: bool, available_from: Optional[datetime], available_to: Optional[datetime], message: Optional[Message], title: Optional[str], user_id: int) -> None:
        self.available = available
        self.available_from = available_from
        self.available_to = available_to
        self.message = message
        self.title = title
        self.user_id = user_id

    @staticmethod
    def from_dict(obj: Any) -> 'AgentAvailability':
        assert isinstance(obj, dict)
        available = from_bool(obj.get("available"))
        available_from = from_union([from_none, from_datetime], obj.get("availableFrom"))
        available_to = from_union([from_none, from_datetime], obj.get("availableTo"))
        message = from_union([Message, from_none], obj.get("message"))
        title = from_union([from_str, from_none], obj.get("title"))
        user_id = from_int(obj.get("userId"))
        return AgentAvailability(available, available_from, available_to, message, title, user_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["available"] = from_bool(self.available)
        result["availableFrom"] = from_union([from_none, lambda x: x.isoformat()], self.available_from)
        result["availableTo"] = from_union([from_none, lambda x: x.isoformat()], self.available_to)
        result["message"] = from_union([lambda x: to_enum(Message, x), from_none], self.message)
        result["title"] = from_union([from_str, from_none], self.title)
        result["userId"] = from_int(self.user_id)
        return result


class AgentReviews:
    approved_reviews_count: int
    entity_rate: Optional[float]
    total_count: int

    def __init__(self, approved_reviews_count: int, entity_rate: Optional[float], total_count: int) -> None:
        self.approved_reviews_count = approved_reviews_count
        self.entity_rate = entity_rate
        self.total_count = total_count

    @staticmethod
    def from_dict(obj: Any) -> 'AgentReviews':
        assert isinstance(obj, dict)
        approved_reviews_count = from_int(obj.get("approvedReviewsCount"))
        entity_rate = from_union([from_float, from_none], obj.get("entityRate"))
        total_count = from_int(obj.get("totalCount"))
        return AgentReviews(approved_reviews_count, entity_rate, total_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["approvedReviewsCount"] = from_int(self.approved_reviews_count)
        result["entityRate"] = from_union([to_float, from_none], self.entity_rate)
        result["totalCount"] = from_int(self.total_count)
        return result


class CianProfileStatus(Enum):
    APPROVED = "approved"
    HIDE = "hide"
    REQUEST = "request"


class UserTrustLevel(Enum):
    INVOLVED = "involved"
    NEW = "new"
    NOT_INVOLVED = "notInvolved"


class UserType(Enum):
    REALTOR_BASED = "realtor_based"
    REALTOR_NOT_COMMERCE = "realtor_not_commerce"
    REALTOR_PROF = "realtor_prof"


class User:
    agency_name: Optional[str]
    agency_name_v2: Optional[str]
    agent_account_type: Optional[AgentAccountType]
    agent_availability: Optional[AgentAvailability]
    agent_avatar_url: Optional[str]
    agent_reviews: Optional[AgentReviews]
    cian_profile_status: Optional[CianProfileStatus]
    cian_user_id: int
    company_name: Optional[str]
    experience: Optional[str]
    is_agent: Optional[bool]
    is_chats_enabled: Optional[bool]
    is_hidden: Optional[bool]
    is_sub_agent: Optional[bool]
    phone_numbers: Optional[List[Phone]]
    user_trust_level: UserTrustLevel
    user_type: Optional[UserType]

    def __init__(self, agency_name: Optional[str], agency_name_v2: Optional[str], agent_account_type: Optional[AgentAccountType], agent_availability: Optional[AgentAvailability], agent_avatar_url: Optional[str], agent_reviews: Optional[AgentReviews], cian_profile_status: Optional[CianProfileStatus], cian_user_id: int, company_name: Optional[str], experience: Optional[str], is_agent: Optional[bool], is_chats_enabled: Optional[bool], is_hidden: Optional[bool], is_sub_agent: Optional[bool], phone_numbers: Optional[List[Phone]], user_trust_level: UserTrustLevel, user_type: Optional[UserType]) -> None:
        self.agency_name = agency_name
        self.agency_name_v2 = agency_name_v2
        self.agent_account_type = agent_account_type
        self.agent_availability = agent_availability
        self.agent_avatar_url = agent_avatar_url
        self.agent_reviews = agent_reviews
        self.cian_profile_status = cian_profile_status
        self.cian_user_id = cian_user_id
        self.company_name = company_name
        self.experience = experience
        self.is_agent = is_agent
        self.is_chats_enabled = is_chats_enabled
        self.is_hidden = is_hidden
        self.is_sub_agent = is_sub_agent
        self.phone_numbers = phone_numbers
        self.user_trust_level = user_trust_level
        self.user_type = user_type

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        agency_name = from_union([from_str, from_none], obj.get("agencyName"))
        agency_name_v2 = from_union([from_str, from_none], obj.get("agencyNameV2"))
        agent_account_type = from_union([AgentAccountType, from_none], obj.get("agentAccountType"))
        agent_availability = from_union([AgentAvailability.from_dict, from_none], obj.get("agentAvailability"))
        agent_avatar_url = from_union([from_str, from_none], obj.get("agentAvatarUrl"))
        agent_reviews = from_union([AgentReviews.from_dict, from_none], obj.get("agentReviews"))
        cian_profile_status = from_union([CianProfileStatus, from_none], obj.get("cianProfileStatus"))
        cian_user_id = int(from_str(obj.get("cianUserId")))
        company_name = from_union([from_str, from_none], obj.get("companyName"))
        experience = from_union([from_str, from_none], obj.get("experience"))
        is_agent = from_union([from_none, from_bool], obj.get("isAgent"))
        is_chats_enabled = from_union([from_none, from_bool], obj.get("isChatsEnabled"))
        is_hidden = from_union([from_none, from_bool], obj.get("isHidden"))
        is_sub_agent = from_union([from_none, from_bool], obj.get("isSubAgent"))
        phone_numbers = from_union([lambda x: from_list(Phone.from_dict, x), from_none], obj.get("phoneNumbers"))
        user_trust_level = UserTrustLevel(obj.get("userTrustLevel"))
        user_type = from_union([UserType, from_none], obj.get("userType"))
        return User(agency_name, agency_name_v2, agent_account_type, agent_availability, agent_avatar_url, agent_reviews, cian_profile_status, cian_user_id, company_name, experience, is_agent, is_chats_enabled, is_hidden, is_sub_agent, phone_numbers, user_trust_level, user_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["agencyName"] = from_union([from_str, from_none], self.agency_name)
        result["agencyNameV2"] = from_union([from_str, from_none], self.agency_name_v2)
        result["agentAccountType"] = from_union([lambda x: to_enum(AgentAccountType, x), from_none], self.agent_account_type)
        result["agentAvailability"] = from_union([lambda x: to_class(AgentAvailability, x), from_none], self.agent_availability)
        result["agentAvatarUrl"] = from_union([from_str, from_none], self.agent_avatar_url)
        result["agentReviews"] = from_union([lambda x: to_class(AgentReviews, x), from_none], self.agent_reviews)
        result["cianProfileStatus"] = from_union([lambda x: to_enum(CianProfileStatus, x), from_none], self.cian_profile_status)
        result["cianUserId"] = from_str(str(self.cian_user_id))
        result["companyName"] = from_union([from_str, from_none], self.company_name)
        result["experience"] = from_union([from_str, from_none], self.experience)
        result["isAgent"] = from_union([from_none, from_bool], self.is_agent)
        result["isChatsEnabled"] = from_union([from_none, from_bool], self.is_chats_enabled)
        result["isHidden"] = from_union([from_none, from_bool], self.is_hidden)
        result["isSubAgent"] = from_union([from_none, from_bool], self.is_sub_agent)
        result["phoneNumbers"] = from_union([lambda x: from_list(lambda x: to_class(Phone, x), x), from_none], self.phone_numbers)
        result["userTrustLevel"] = to_enum(UserTrustLevel, self.user_trust_level)
        result["userType"] = from_union([lambda x: to_enum(UserType, x), from_none], self.user_type)
        return result


class ValueAddedServices:
    is_calltracking: bool
    is_colorized: bool
    is_free: bool
    is_paid: bool
    is_premium: bool
    is_top3: bool

    def __init__(self, is_calltracking: bool, is_colorized: bool, is_free: bool, is_paid: bool, is_premium: bool, is_top3: bool) -> None:
        self.is_calltracking = is_calltracking
        self.is_colorized = is_colorized
        self.is_free = is_free
        self.is_paid = is_paid
        self.is_premium = is_premium
        self.is_top3 = is_top3

    @staticmethod
    def from_dict(obj: Any) -> 'ValueAddedServices':
        assert isinstance(obj, dict)
        is_calltracking = from_bool(obj.get("isCalltracking"))
        is_colorized = from_bool(obj.get("isColorized"))
        is_free = from_bool(obj.get("isFree"))
        is_paid = from_bool(obj.get("isPaid"))
        is_premium = from_bool(obj.get("isPremium"))
        is_top3 = from_bool(obj.get("isTop3"))
        return ValueAddedServices(is_calltracking, is_colorized, is_free, is_paid, is_premium, is_top3)

    def to_dict(self) -> dict:
        result: dict = {}
        result["isCalltracking"] = from_bool(self.is_calltracking)
        result["isColorized"] = from_bool(self.is_colorized)
        result["isFree"] = from_bool(self.is_free)
        result["isPaid"] = from_bool(self.is_paid)
        result["isPremium"] = from_bool(self.is_premium)
        result["isTop3"] = from_bool(self.is_top3)
        return result


class Video:
    duration: int
    id: str
    type: str
    upload_date: datetime
    url: str

    def __init__(self, duration: int, id: str, type: str, upload_date: datetime, url: str) -> None:
        self.duration = duration
        self.id = id
        self.type = type
        self.upload_date = upload_date
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> 'Video':
        assert isinstance(obj, dict)
        duration = from_int(obj.get("duration"))
        id = from_str(obj.get("id"))
        type = from_str(obj.get("type"))
        upload_date = from_datetime(obj.get("uploadDate"))
        url = from_str(obj.get("url"))
        return Video(duration, id, type, upload_date, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["duration"] = from_int(self.duration)
        result["id"] = from_str(self.id)
        result["type"] = from_str(self.type)
        result["uploadDate"] = self.upload_date.isoformat()
        result["url"] = from_str(self.url)
        return result


class WaterType(Enum):
    AUTONOMOUS = "autonomous"
    CENTRAL = "central"
    PUMPING_STATION = "pumpingStation"
    WATER_INTAKE_FACILITY = "waterIntakeFacility"
    WATER_TOWER = "waterTower"


class Water:
    capacity: Optional[int]
    location_type: Optional[ConditioningTypeEnum]
    possible_to_connect: Optional[bool]
    type: Optional[WaterType]

    def __init__(self, capacity: Optional[int], location_type: Optional[ConditioningTypeEnum], possible_to_connect: Optional[bool], type: Optional[WaterType]) -> None:
        self.capacity = capacity
        self.location_type = location_type
        self.possible_to_connect = possible_to_connect
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Water':
        assert isinstance(obj, dict)
        capacity = from_union([from_int, from_none], obj.get("capacity"))
        location_type = from_union([ConditioningTypeEnum, from_none], obj.get("locationType"))
        possible_to_connect = from_union([from_none, from_bool], obj.get("possibleToConnect"))
        type = from_union([from_none, WaterType], obj.get("type"))
        return Water(capacity, location_type, possible_to_connect, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["capacity"] = from_union([from_int, from_none], self.capacity)
        result["locationType"] = from_union([lambda x: to_enum(ConditioningTypeEnum, x), from_none], self.location_type)
        result["possibleToConnect"] = from_union([from_none, from_bool], self.possible_to_connect)
        result["type"] = from_union([from_none, lambda x: to_enum(WaterType, x)], self.type)
        return result


class WcLocationType(Enum):
    INDOORS = "indoors"
    OUTDOORS = "outdoors"


class WindowsViewType(Enum):
    STREET = "street"
    YARD = "yard"
    YARD_AND_STREET = "yardAndStreet"


class OffersSerialized:
    access_type: Optional[AccessTypeEnum]
    added: str
    additional_phone_lines_allowed: Optional[int]
    all_from_offrep: Optional[AllFromOffrep]
    all_rooms_area: Optional[float]
    archived_date: Optional[datetime]
    available_from: Optional[datetime]
    balconies_count: Optional[int]
    bargain_terms: BargainTerms
    bedrooms_count: Optional[int]
    beds_count: Optional[int]
    booking: Optional[str]
    building: Building
    business_shopping_center: Optional[BusinessShoppingCenter]
    call_tracking_provider: Optional[CallTrackingProvider]
    can_parts: Optional[bool]
    categories_ids: List[int]
    category: Category
    chat_id: Optional[str]
    children_allowed: Optional[bool]
    cian_id: int
    cian_user_id: Optional[int]
    combined_wcs_count: Optional[int]
    condition_rating_type: Optional[str]
    condition_type: Optional[ConditionType]
    cpl_moderation: Optional[str]
    deal_type: DealTypeEnum
    decoration: Optional[Decoration]
    demolished_in_moscow_programm: Optional[bool]
    description: str
    description_minhash: Optional[List[int]]
    district: Optional[str]
    drainage: Optional[str]
    drainage_capacity: Optional[float]
    drainage_type: Optional[str]
    driveway_type: Optional[DrivewayType]
    edit_date: Optional[datetime]
    electricity: Optional[Electricity]
    electricity_power: Optional[float]
    electricity_type: Optional[bool]
    estate_type: Optional[EstateTypeEnum]
    external_id: Optional[str]
    external_url: Optional[str]
    feedbox_multi_offer_key: Optional[str]
    flags: Optional[Flags]
    flat_type: Optional[str]
    floor_material_type: Optional[str]
    floor_number: Optional[int]
    from_developer: Optional[bool]
    furniture: Optional[str]
    furniture_presence: Optional[str]
    ga_label: str
    garage: Optional[Garage]
    gas: Optional[Gas]
    gas_capacity: Optional[int]
    gas_pressure: Optional[PressureType]
    gas_type: Optional[str]
    geo: OffersSerializedGeo
    has_bathhouse: Optional[bool]
    has_bathtub: Optional[bool]
    has_check_in_24: Optional[bool]
    has_conditioner: Optional[bool]
    has_dishwasher: Optional[bool]
    has_drainage: Optional[bool]
    has_electricity: Optional[bool]
    has_encumbrances: Optional[bool]
    has_equipment: Optional[bool]
    has_excursions: Optional[bool]
    has_extinguishing_system: Optional[bool]
    has_fridge: Optional[bool]
    has_furniture: Optional[bool]
    has_garage: Optional[bool]
    has_gas: Optional[bool]
    has_hairdryer: Optional[bool]
    has_heating: Optional[bool]
    has_internet: Optional[bool]
    has_investment_project: Optional[bool]
    has_iron: Optional[bool]
    has_jacuzzi: Optional[bool]
    has_kitchen_furniture: Optional[bool]
    has_lift: Optional[bool]
    has_light: Optional[bool]
    has_parking: Optional[bool]
    has_phone: Optional[bool]
    has_pool: Optional[bool]
    has_ramp: Optional[bool]
    has_safe_custody: Optional[bool]
    has_seconded_docs: Optional[bool]
    has_security: Optional[bool]
    has_shop_windows: Optional[bool]
    has_shower: Optional[bool]
    has_tea_coffee_sugar: Optional[bool]
    has_transfer: Optional[bool]
    has_transport_services: Optional[bool]
    has_tv: Optional[bool]
    has_washer: Optional[bool]
    has_water: Optional[bool]
    has_wifi: Optional[bool]
    has_wired_internet: Optional[bool]
    id: int
    input_type: Optional[InputType]
    is_apartments: Optional[bool]
    is_auction: Optional[bool]
    is_by_homeowner: Optional[bool]
    is_colorized: Optional[bool]
    is_customs: Optional[bool]
    is_duplicated_description: Optional[bool]
    is_enabled_call_tracking: Optional[bool]
    is_fairplay: Optional[bool]
    is_favorite: Optional[bool]
    is_from_builder: Optional[bool]
    is_hidden_by_user: Optional[bool]
    is_in_hidden_base: Optional[bool]
    is_legal_address_provided: Optional[bool]
    is_new: Optional[bool]
    is_occupied: Optional[bool]
    is_paid: Optional[bool]
    is_penthouse: Optional[bool]
    is_premium: Optional[bool]
    is_pro: Optional[bool]
    is_rent_by_parts: Optional[bool]
    is_top3: Optional[bool]
    jk_url: Optional[str]
    kitchen_area: Optional[float]
    kp: Optional[str]
    land: Optional[Land]
    layout: Optional[Layout]
    layout_photo: Optional[str]
    leisure: Optional[float]
    living_area: Optional[float]
    loggias_count: Optional[int]
    max_area: Optional[float]
    min_area: Optional[str]
    min_price_total: Optional[float]
    min_price_total_per_month: Optional[float]
    min_price_total_per_month_rur: Optional[float]
    min_price_total_per_month_rur_for_search: Optional[str]
    min_price_total_rur: Optional[int]
    min_price_total_rur_for_search: Optional[float]
    min_vat_price_total_per_month_rur: Optional[float]
    min_vat_price_total_rur: Optional[int]
    monthly_income: Optional[MonthlyIncome]
    name: Optional[str]
    newbuilding: Optional[Newbuilding]
    notes: Optional[Notes]
    object_guid: Optional[UUID]
    offer_type: OfferType
    permitted_use_type: Optional[PermittedUseType]
    pets_allowed: Optional[bool]
    phone_lines_count: Optional[int]
    phones: List[Phone]
    photos: List[Photo]
    placement_type: Optional[PlacementType]
    platform: Optional[Platform]
    possible_to_change_permitted_use_type: Optional[bool]
    price_changes: Optional[List[PriceChange]]
    price_per_unit_area: Optional[float]
    price_per_unit_area_eur: Optional[float]
    price_per_unit_area_per_month: Optional[float]
    price_per_unit_area_per_month_rur: Optional[float]
    price_per_unit_area_per_month_rur_for_search: Optional[float]
    price_per_unit_area_per_year: Optional[float]
    price_per_unit_area_per_year_eur: Optional[float]
    price_per_unit_area_per_year_rur: Optional[float]
    price_per_unit_area_per_year_rur_for_search: Optional[str]
    price_per_unit_area_per_year_usd: Optional[float]
    price_per_unit_area_rur: Optional[float]
    price_per_unit_area_rur_for_search: Optional[float]
    price_per_unit_area_usd: Optional[float]
    price_total: Optional[float]
    price_total_eur: Optional[float]
    price_total_per_month: Optional[float]
    price_total_per_month_eur: Optional[float]
    price_total_per_month_rur: Optional[float]
    price_total_per_month_rur_for_search: Optional[float]
    price_total_per_month_usd: Optional[float]
    price_total_rur: Optional[float]
    price_total_rur_for_search: Optional[float]
    price_total_usd: Optional[float]
    project_declaration_url: Optional[str]
    promo_info: Optional[str]
    property_type: Optional[PropertyType]
    published_user_id: int
    publish_terms: Optional[PublishTerms]
    rent_by_parts_description: Optional[str]
    repair_type: Optional[RepairType]
    room_area: Optional[float]
    rooms_area: Optional[float]
    rooms_count: Optional[int]
    rooms_for_sale_count: Optional[int]
    room_type: Optional[str]
    rosreestr_check: Optional[bool]
    separate_wcs_count: Optional[int]
    settlement_name: Optional[str]
    share_amount: Optional[str]
    similar: Optional[bool]
    specialty: OffersSerializedSpecialty
    statistic: Optional[Statistic]
    status: Status
    tax_number: Optional[int]
    title: Optional[str]
    total_area: Optional[str]
    user: User
    user_id: int
    value_added_services: Optional[ValueAddedServices]
    vas_type: Optional[str]
    vat_price_total_per_month_rur: Optional[float]
    vat_price_total_rur: Optional[int]
    videos: List[Video]
    water: Optional[Water]
    water_capacity: Optional[float]
    water_pipes_count: Optional[int]
    water_type: Optional[bool]
    wc_location_type: Optional[WcLocationType]
    wc_type: Optional[int]
    windows_view_type: Optional[WindowsViewType]
    without_client_fee: Optional[bool]
    work_time_info: Optional[str]

    def __init__(self, access_type: Optional[AccessTypeEnum], added: str, additional_phone_lines_allowed: Optional[int], all_from_offrep: Optional[AllFromOffrep], all_rooms_area: Optional[float], archived_date: Optional[datetime], available_from: Optional[datetime], balconies_count: Optional[int], bargain_terms: BargainTerms, bedrooms_count: Optional[int], beds_count: Optional[int], booking: Optional[str], building: Building, business_shopping_center: Optional[BusinessShoppingCenter], call_tracking_provider: Optional[CallTrackingProvider], can_parts: Optional[bool], categories_ids: List[int], category: Category, chat_id: Optional[str], children_allowed: Optional[bool], cian_id: int, cian_user_id: Optional[int], combined_wcs_count: Optional[int], condition_rating_type: Optional[str], condition_type: Optional[ConditionType], cpl_moderation: Optional[str], deal_type: DealTypeEnum, decoration: Optional[Decoration], demolished_in_moscow_programm: Optional[bool], description: str, description_minhash: Optional[List[int]], district: Optional[str], drainage: Optional[str], drainage_capacity: Optional[float], drainage_type: Optional[str], driveway_type: Optional[DrivewayType], edit_date: Optional[datetime], electricity: Optional[Electricity], electricity_power: Optional[float], electricity_type: Optional[bool], estate_type: Optional[EstateTypeEnum], external_id: Optional[str], external_url: Optional[str], feedbox_multi_offer_key: Optional[str], flags: Optional[Flags], flat_type: Optional[str], floor_material_type: Optional[str], floor_number: Optional[int], from_developer: Optional[bool], furniture: Optional[str], furniture_presence: Optional[str], ga_label: str, garage: Optional[Garage], gas: Optional[Gas], gas_capacity: Optional[int], gas_pressure: Optional[PressureType], gas_type: Optional[str], geo: OffersSerializedGeo, has_bathhouse: Optional[bool], has_bathtub: Optional[bool], has_check_in_24: Optional[bool], has_conditioner: Optional[bool], has_dishwasher: Optional[bool], has_drainage: Optional[bool], has_electricity: Optional[bool], has_encumbrances: Optional[bool], has_equipment: Optional[bool], has_excursions: Optional[bool], has_extinguishing_system: Optional[bool], has_fridge: Optional[bool], has_furniture: Optional[bool], has_garage: Optional[bool], has_gas: Optional[bool], has_hairdryer: Optional[bool], has_heating: Optional[bool], has_internet: Optional[bool], has_investment_project: Optional[bool], has_iron: Optional[bool], has_jacuzzi: Optional[bool], has_kitchen_furniture: Optional[bool], has_lift: Optional[bool], has_light: Optional[bool], has_parking: Optional[bool], has_phone: Optional[bool], has_pool: Optional[bool], has_ramp: Optional[bool], has_safe_custody: Optional[bool], has_seconded_docs: Optional[bool], has_security: Optional[bool], has_shop_windows: Optional[bool], has_shower: Optional[bool], has_tea_coffee_sugar: Optional[bool], has_transfer: Optional[bool], has_transport_services: Optional[bool], has_tv: Optional[bool], has_washer: Optional[bool], has_water: Optional[bool], has_wifi: Optional[bool], has_wired_internet: Optional[bool], id: int, input_type: Optional[InputType], is_apartments: Optional[bool], is_auction: Optional[bool], is_by_homeowner: Optional[bool], is_colorized: Optional[bool], is_customs: Optional[bool], is_duplicated_description: Optional[bool], is_enabled_call_tracking: Optional[bool], is_fairplay: Optional[bool], is_favorite: Optional[bool], is_from_builder: Optional[bool], is_hidden_by_user: Optional[bool], is_in_hidden_base: Optional[bool], is_legal_address_provided: Optional[bool], is_new: Optional[bool], is_occupied: Optional[bool], is_paid: Optional[bool], is_penthouse: Optional[bool], is_premium: Optional[bool], is_pro: Optional[bool], is_rent_by_parts: Optional[bool], is_top3: Optional[bool], jk_url: Optional[str], kitchen_area: Optional[float], kp: Optional[str], land: Optional[Land], layout: Optional[Layout], layout_photo: Optional[str], leisure: Optional[float], living_area: Optional[float], loggias_count: Optional[int], max_area: Optional[float], min_area: Optional[str], min_price_total: Optional[float], min_price_total_per_month: Optional[float], min_price_total_per_month_rur: Optional[float], min_price_total_per_month_rur_for_search: Optional[str], min_price_total_rur: Optional[int], min_price_total_rur_for_search: Optional[float], min_vat_price_total_per_month_rur: Optional[float], min_vat_price_total_rur: Optional[int], monthly_income: Optional[MonthlyIncome], name: Optional[str], newbuilding: Optional[Newbuilding], notes: Optional[Notes], object_guid: Optional[UUID], offer_type: OfferType, permitted_use_type: Optional[PermittedUseType], pets_allowed: Optional[bool], phone_lines_count: Optional[int], phones: List[Phone], photos: List[Photo], placement_type: Optional[PlacementType], platform: Optional[Platform], possible_to_change_permitted_use_type: Optional[bool], price_changes: Optional[List[PriceChange]], price_per_unit_area: Optional[float], price_per_unit_area_eur: Optional[float], price_per_unit_area_per_month: Optional[float], price_per_unit_area_per_month_rur: Optional[float], price_per_unit_area_per_month_rur_for_search: Optional[float], price_per_unit_area_per_year: Optional[float], price_per_unit_area_per_year_eur: Optional[float], price_per_unit_area_per_year_rur: Optional[float], price_per_unit_area_per_year_rur_for_search: Optional[str], price_per_unit_area_per_year_usd: Optional[float], price_per_unit_area_rur: Optional[float], price_per_unit_area_rur_for_search: Optional[float], price_per_unit_area_usd: Optional[float], price_total: Optional[float], price_total_eur: Optional[float], price_total_per_month: Optional[float], price_total_per_month_eur: Optional[float], price_total_per_month_rur: Optional[float], price_total_per_month_rur_for_search: Optional[float], price_total_per_month_usd: Optional[float], price_total_rur: Optional[float], price_total_rur_for_search: Optional[float], price_total_usd: Optional[float], project_declaration_url: Optional[str], promo_info: Optional[str], property_type: Optional[PropertyType], published_user_id: int, publish_terms: Optional[PublishTerms], rent_by_parts_description: Optional[str], repair_type: Optional[RepairType], room_area: Optional[float], rooms_area: Optional[float], rooms_count: Optional[int], rooms_for_sale_count: Optional[int], room_type: Optional[str], rosreestr_check: Optional[bool], separate_wcs_count: Optional[int], settlement_name: Optional[str], share_amount: Optional[str], similar: Optional[bool], specialty: OffersSerializedSpecialty, statistic: Optional[Statistic], status: Status, tax_number: Optional[int], title: Optional[str], total_area: Optional[str], user: User, user_id: int, value_added_services: Optional[ValueAddedServices], vas_type: Optional[str], vat_price_total_per_month_rur: Optional[float], vat_price_total_rur: Optional[int], videos: List[Video], water: Optional[Water], water_capacity: Optional[float], water_pipes_count: Optional[int], water_type: Optional[bool], wc_location_type: Optional[WcLocationType], wc_type: Optional[int], windows_view_type: Optional[WindowsViewType], without_client_fee: Optional[bool], work_time_info: Optional[str]) -> None:
        self.access_type = access_type
        self.added = added
        self.additional_phone_lines_allowed = additional_phone_lines_allowed
        self.all_from_offrep = all_from_offrep
        self.all_rooms_area = all_rooms_area
        self.archived_date = archived_date
        self.available_from = available_from
        self.balconies_count = balconies_count
        self.bargain_terms = bargain_terms
        self.bedrooms_count = bedrooms_count
        self.beds_count = beds_count
        self.booking = booking
        self.building = building
        self.business_shopping_center = business_shopping_center
        self.call_tracking_provider = call_tracking_provider
        self.can_parts = can_parts
        self.categories_ids = categories_ids
        self.category = category
        self.chat_id = chat_id
        self.children_allowed = children_allowed
        self.cian_id = cian_id
        self.cian_user_id = cian_user_id
        self.combined_wcs_count = combined_wcs_count
        self.condition_rating_type = condition_rating_type
        self.condition_type = condition_type
        self.cpl_moderation = cpl_moderation
        self.deal_type = deal_type
        self.decoration = decoration
        self.demolished_in_moscow_programm = demolished_in_moscow_programm
        self.description = description
        self.description_minhash = description_minhash
        self.district = district
        self.drainage = drainage
        self.drainage_capacity = drainage_capacity
        self.drainage_type = drainage_type
        self.driveway_type = driveway_type
        self.edit_date = edit_date
        self.electricity = electricity
        self.electricity_power = electricity_power
        self.electricity_type = electricity_type
        self.estate_type = estate_type
        self.external_id = external_id
        self.external_url = external_url
        self.feedbox_multi_offer_key = feedbox_multi_offer_key
        self.flags = flags
        self.flat_type = flat_type
        self.floor_material_type = floor_material_type
        self.floor_number = floor_number
        self.from_developer = from_developer
        self.furniture = furniture
        self.furniture_presence = furniture_presence
        self.ga_label = ga_label
        self.garage = garage
        self.gas = gas
        self.gas_capacity = gas_capacity
        self.gas_pressure = gas_pressure
        self.gas_type = gas_type
        self.geo = geo
        self.has_bathhouse = has_bathhouse
        self.has_bathtub = has_bathtub
        self.has_check_in_24 = has_check_in_24
        self.has_conditioner = has_conditioner
        self.has_dishwasher = has_dishwasher
        self.has_drainage = has_drainage
        self.has_electricity = has_electricity
        self.has_encumbrances = has_encumbrances
        self.has_equipment = has_equipment
        self.has_excursions = has_excursions
        self.has_extinguishing_system = has_extinguishing_system
        self.has_fridge = has_fridge
        self.has_furniture = has_furniture
        self.has_garage = has_garage
        self.has_gas = has_gas
        self.has_hairdryer = has_hairdryer
        self.has_heating = has_heating
        self.has_internet = has_internet
        self.has_investment_project = has_investment_project
        self.has_iron = has_iron
        self.has_jacuzzi = has_jacuzzi
        self.has_kitchen_furniture = has_kitchen_furniture
        self.has_lift = has_lift
        self.has_light = has_light
        self.has_parking = has_parking
        self.has_phone = has_phone
        self.has_pool = has_pool
        self.has_ramp = has_ramp
        self.has_safe_custody = has_safe_custody
        self.has_seconded_docs = has_seconded_docs
        self.has_security = has_security
        self.has_shop_windows = has_shop_windows
        self.has_shower = has_shower
        self.has_tea_coffee_sugar = has_tea_coffee_sugar
        self.has_transfer = has_transfer
        self.has_transport_services = has_transport_services
        self.has_tv = has_tv
        self.has_washer = has_washer
        self.has_water = has_water
        self.has_wifi = has_wifi
        self.has_wired_internet = has_wired_internet
        self.id = id
        self.input_type = input_type
        self.is_apartments = is_apartments
        self.is_auction = is_auction
        self.is_by_homeowner = is_by_homeowner
        self.is_colorized = is_colorized
        self.is_customs = is_customs
        self.is_duplicated_description = is_duplicated_description
        self.is_enabled_call_tracking = is_enabled_call_tracking
        self.is_fairplay = is_fairplay
        self.is_favorite = is_favorite
        self.is_from_builder = is_from_builder
        self.is_hidden_by_user = is_hidden_by_user
        self.is_in_hidden_base = is_in_hidden_base
        self.is_legal_address_provided = is_legal_address_provided
        self.is_new = is_new
        self.is_occupied = is_occupied
        self.is_paid = is_paid
        self.is_penthouse = is_penthouse
        self.is_premium = is_premium
        self.is_pro = is_pro
        self.is_rent_by_parts = is_rent_by_parts
        self.is_top3 = is_top3
        self.jk_url = jk_url
        self.kitchen_area = kitchen_area
        self.kp = kp
        self.land = land
        self.layout = layout
        self.layout_photo = layout_photo
        self.leisure = leisure
        self.living_area = living_area
        self.loggias_count = loggias_count
        self.max_area = max_area
        self.min_area = min_area
        self.min_price_total = min_price_total
        self.min_price_total_per_month = min_price_total_per_month
        self.min_price_total_per_month_rur = min_price_total_per_month_rur
        self.min_price_total_per_month_rur_for_search = min_price_total_per_month_rur_for_search
        self.min_price_total_rur = min_price_total_rur
        self.min_price_total_rur_for_search = min_price_total_rur_for_search
        self.min_vat_price_total_per_month_rur = min_vat_price_total_per_month_rur
        self.min_vat_price_total_rur = min_vat_price_total_rur
        self.monthly_income = monthly_income
        self.name = name
        self.newbuilding = newbuilding
        self.notes = notes
        self.object_guid = object_guid
        self.offer_type = offer_type
        self.permitted_use_type = permitted_use_type
        self.pets_allowed = pets_allowed
        self.phone_lines_count = phone_lines_count
        self.phones = phones
        self.photos = photos
        self.placement_type = placement_type
        self.platform = platform
        self.possible_to_change_permitted_use_type = possible_to_change_permitted_use_type
        self.price_changes = price_changes
        self.price_per_unit_area = price_per_unit_area
        self.price_per_unit_area_eur = price_per_unit_area_eur
        self.price_per_unit_area_per_month = price_per_unit_area_per_month
        self.price_per_unit_area_per_month_rur = price_per_unit_area_per_month_rur
        self.price_per_unit_area_per_month_rur_for_search = price_per_unit_area_per_month_rur_for_search
        self.price_per_unit_area_per_year = price_per_unit_area_per_year
        self.price_per_unit_area_per_year_eur = price_per_unit_area_per_year_eur
        self.price_per_unit_area_per_year_rur = price_per_unit_area_per_year_rur
        self.price_per_unit_area_per_year_rur_for_search = price_per_unit_area_per_year_rur_for_search
        self.price_per_unit_area_per_year_usd = price_per_unit_area_per_year_usd
        self.price_per_unit_area_rur = price_per_unit_area_rur
        self.price_per_unit_area_rur_for_search = price_per_unit_area_rur_for_search
        self.price_per_unit_area_usd = price_per_unit_area_usd
        self.price_total = price_total
        self.price_total_eur = price_total_eur
        self.price_total_per_month = price_total_per_month
        self.price_total_per_month_eur = price_total_per_month_eur
        self.price_total_per_month_rur = price_total_per_month_rur
        self.price_total_per_month_rur_for_search = price_total_per_month_rur_for_search
        self.price_total_per_month_usd = price_total_per_month_usd
        self.price_total_rur = price_total_rur
        self.price_total_rur_for_search = price_total_rur_for_search
        self.price_total_usd = price_total_usd
        self.project_declaration_url = project_declaration_url
        self.promo_info = promo_info
        self.property_type = property_type
        self.published_user_id = published_user_id
        self.publish_terms = publish_terms
        self.rent_by_parts_description = rent_by_parts_description
        self.repair_type = repair_type
        self.room_area = room_area
        self.rooms_area = rooms_area
        self.rooms_count = rooms_count
        self.rooms_for_sale_count = rooms_for_sale_count
        self.room_type = room_type
        self.rosreestr_check = rosreestr_check
        self.separate_wcs_count = separate_wcs_count
        self.settlement_name = settlement_name
        self.share_amount = share_amount
        self.similar = similar
        self.specialty = specialty
        self.statistic = statistic
        self.status = status
        self.tax_number = tax_number
        self.title = title
        self.total_area = total_area
        self.user = user
        self.user_id = user_id
        self.value_added_services = value_added_services
        self.vas_type = vas_type
        self.vat_price_total_per_month_rur = vat_price_total_per_month_rur
        self.vat_price_total_rur = vat_price_total_rur
        self.videos = videos
        self.water = water
        self.water_capacity = water_capacity
        self.water_pipes_count = water_pipes_count
        self.water_type = water_type
        self.wc_location_type = wc_location_type
        self.wc_type = wc_type
        self.windows_view_type = windows_view_type
        self.without_client_fee = without_client_fee
        self.work_time_info = work_time_info

    @staticmethod
    def from_dict(obj: Any) -> 'OffersSerialized':
        assert isinstance(obj, dict)
        access_type = from_union([from_none, AccessTypeEnum], obj.get("accessType"))
        added = from_str(obj.get("added"))
        additional_phone_lines_allowed = from_union([from_int, from_none], obj.get("additionalPhoneLinesAllowed"))
        all_from_offrep = from_union([AllFromOffrep.from_dict, from_none], obj.get("allFromOffrep"))
        all_rooms_area = from_union([from_float, from_none], obj.get("allRoomsArea"))
        archived_date = from_union([from_none, from_datetime], obj.get("archivedDate"))
        available_from = from_union([from_none, from_datetime], obj.get("availableFrom"))
        balconies_count = from_union([from_int, from_none], obj.get("balconiesCount"))
        bargain_terms = BargainTerms.from_dict(obj.get("bargainTerms"))
        bedrooms_count = from_union([from_int, from_none], obj.get("bedroomsCount"))
        beds_count = from_union([from_int, from_none], obj.get("bedsCount"))
        booking = from_union([from_none, from_str], obj.get("booking"))
        building = Building.from_dict(obj.get("building"))
        business_shopping_center = from_union([BusinessShoppingCenter.from_dict, from_none], obj.get("businessShoppingCenter"))
        call_tracking_provider = from_union([from_none, CallTrackingProvider], obj.get("callTrackingProvider"))
        can_parts = from_union([from_none, from_bool], obj.get("canParts"))
        categories_ids = from_list(from_int, obj.get("categoriesIds"))
        category = Category(obj.get("category"))
        chat_id = from_union([from_none, from_str], obj.get("chatId"))
        children_allowed = from_union([from_none, from_bool], obj.get("childrenAllowed"))
        cian_id = from_int(obj.get("cianId"))
        cian_user_id = from_union([from_int, from_none], obj.get("cianUserId"))
        combined_wcs_count = from_union([from_int, from_none], obj.get("combinedWcsCount"))
        condition_rating_type = from_union([from_none, from_str], obj.get("conditionRatingType"))
        condition_type = from_union([from_none, ConditionType], obj.get("conditionType"))
        cpl_moderation = from_union([from_none, from_str], obj.get("cplModeration"))
        deal_type = DealTypeEnum(obj.get("dealType"))
        decoration = from_union([from_none, Decoration], obj.get("decoration"))
        demolished_in_moscow_programm = from_union([from_none, from_bool], obj.get("demolishedInMoscowProgramm"))
        description = from_str(obj.get("description"))
        description_minhash = from_union([lambda x: from_list(from_int, x), from_none], obj.get("descriptionMinhash"))
        district = from_union([from_none, from_str], obj.get("district"))
        drainage = from_union([from_none, from_str], obj.get("drainage"))
        drainage_capacity = from_union([from_float, from_none], obj.get("drainageCapacity"))
        drainage_type = from_union([from_none, from_str], obj.get("drainageType"))
        driveway_type = from_union([from_none, DrivewayType], obj.get("drivewayType"))
        edit_date = from_union([from_none, from_datetime], obj.get("editDate"))
        electricity = from_union([Electricity.from_dict, from_none], obj.get("electricity"))
        electricity_power = from_union([from_float, from_none], obj.get("electricityPower"))
        electricity_type = from_union([from_none, from_bool], obj.get("electricityType"))
        estate_type = from_union([from_none, EstateTypeEnum], obj.get("estateType"))
        external_id = from_union([from_none, from_str], obj.get("externalId"))
        external_url = from_union([from_none, from_str], obj.get("externalUrl"))
        feedbox_multi_offer_key = from_union([from_none, from_str], obj.get("feedboxMultiOfferKey"))
        flags = from_union([Flags.from_dict, from_none], obj.get("flags"))
        flat_type = from_union([from_none, from_str], obj.get("flatType"))
        floor_material_type = from_union([from_none, from_str], obj.get("floorMaterialType"))
        floor_number = from_union([from_int, from_none], obj.get("floorNumber"))
        from_developer = from_union([from_none, from_bool], obj.get("fromDeveloper"))
        furniture = from_union([from_none, from_str], obj.get("furniture"))
        furniture_presence = from_union([from_none, from_str], obj.get("furniturePresence"))
        ga_label = from_str(obj.get("gaLabel"))
        garage = from_union([Garage.from_dict, from_none], obj.get("garage"))
        gas = from_union([Gas.from_dict, from_none], obj.get("gas"))
        gas_capacity = from_union([from_int, from_none], obj.get("gasCapacity"))
        gas_pressure = from_union([from_none, PressureType], obj.get("gasPressure"))
        gas_type = from_union([from_none, from_str], obj.get("gasType"))
        geo = OffersSerializedGeo.from_dict(obj.get("geo"))
        has_bathhouse = from_union([from_none, from_bool], obj.get("hasBathhouse"))
        has_bathtub = from_union([from_none, from_bool], obj.get("hasBathtub"))
        has_check_in_24 = from_union([from_none, from_bool], obj.get("hasCheckIn_24"))
        has_conditioner = from_union([from_none, from_bool], obj.get("hasConditioner"))
        has_dishwasher = from_union([from_none, from_bool], obj.get("hasDishwasher"))
        has_drainage = from_union([from_none, from_bool], obj.get("hasDrainage"))
        has_electricity = from_union([from_none, from_bool], obj.get("hasElectricity"))
        has_encumbrances = from_union([from_none, from_bool], obj.get("hasEncumbrances"))
        has_equipment = from_union([from_none, from_bool], obj.get("hasEquipment"))
        has_excursions = from_union([from_none, from_bool], obj.get("hasExcursions"))
        has_extinguishing_system = from_union([from_none, from_bool], obj.get("hasExtinguishingSystem"))
        has_fridge = from_union([from_none, from_bool], obj.get("hasFridge"))
        has_furniture = from_union([from_none, from_bool], obj.get("hasFurniture"))
        has_garage = from_union([from_none, from_bool], obj.get("hasGarage"))
        has_gas = from_union([from_none, from_bool], obj.get("hasGas"))
        has_hairdryer = from_union([from_none, from_bool], obj.get("hasHairdryer"))
        has_heating = from_union([from_none, from_bool], obj.get("hasHeating"))
        has_internet = from_union([from_none, from_bool], obj.get("hasInternet"))
        has_investment_project = from_union([from_none, from_bool], obj.get("hasInvestmentProject"))
        has_iron = from_union([from_none, from_bool], obj.get("hasIron"))
        has_jacuzzi = from_union([from_none, from_bool], obj.get("hasJacuzzi"))
        has_kitchen_furniture = from_union([from_none, from_bool], obj.get("hasKitchenFurniture"))
        has_lift = from_union([from_none, from_bool], obj.get("hasLift"))
        has_light = from_union([from_none, from_bool], obj.get("hasLight"))
        has_parking = from_union([from_none, from_bool], obj.get("hasParking"))
        has_phone = from_union([from_none, from_bool], obj.get("hasPhone"))
        has_pool = from_union([from_none, from_bool], obj.get("hasPool"))
        has_ramp = from_union([from_none, from_bool], obj.get("hasRamp"))
        has_safe_custody = from_union([from_none, from_bool], obj.get("hasSafeCustody"))
        has_seconded_docs = from_union([from_none, from_bool], obj.get("hasSecondedDocs"))
        has_security = from_union([from_none, from_bool], obj.get("hasSecurity"))
        has_shop_windows = from_union([from_none, from_bool], obj.get("hasShopWindows"))
        has_shower = from_union([from_none, from_bool], obj.get("hasShower"))
        has_tea_coffee_sugar = from_union([from_none, from_bool], obj.get("hasTeaCoffeeSugar"))
        has_transfer = from_union([from_none, from_bool], obj.get("hasTransfer"))
        has_transport_services = from_union([from_none, from_bool], obj.get("hasTransportServices"))
        has_tv = from_union([from_none, from_bool], obj.get("hasTv"))
        has_washer = from_union([from_none, from_bool], obj.get("hasWasher"))
        has_water = from_union([from_none, from_bool], obj.get("hasWater"))
        has_wifi = from_union([from_none, from_bool], obj.get("hasWifi"))
        has_wired_internet = from_union([from_none, from_bool], obj.get("hasWiredInternet"))
        id = from_int(obj.get("id"))
        input_type = from_union([from_none, InputType], obj.get("inputType"))
        is_apartments = from_union([from_none, from_bool], obj.get("isApartments"))
        is_auction = from_union([from_none, from_bool], obj.get("isAuction"))
        is_by_homeowner = from_union([from_none, from_bool], obj.get("isByHomeowner"))
        is_colorized = from_union([from_none, from_bool], obj.get("isColorized"))
        is_customs = from_union([from_none, from_bool], obj.get("isCustoms"))
        is_duplicated_description = from_union([from_none, from_bool], obj.get("isDuplicatedDescription"))
        is_enabled_call_tracking = from_union([from_none, from_bool], obj.get("isEnabledCallTracking"))
        is_fairplay = from_union([from_none, from_bool], obj.get("isFairplay"))
        is_favorite = from_union([from_none, from_bool], obj.get("isFavorite"))
        is_from_builder = from_union([from_none, from_bool], obj.get("isFromBuilder"))
        is_hidden_by_user = from_union([from_none, from_bool], obj.get("isHiddenByUser"))
        is_in_hidden_base = from_union([from_none, from_bool], obj.get("isInHiddenBase"))
        is_legal_address_provided = from_union([from_none, from_bool], obj.get("isLegalAddressProvided"))
        is_new = from_union([from_none, from_bool], obj.get("isNew"))
        is_occupied = from_union([from_none, from_bool], obj.get("isOccupied"))
        is_paid = from_union([from_none, from_bool], obj.get("isPaid"))
        is_penthouse = from_union([from_none, from_bool], obj.get("isPenthouse"))
        is_premium = from_union([from_none, from_bool], obj.get("isPremium"))
        is_pro = from_union([from_none, from_bool], obj.get("isPro"))
        is_rent_by_parts = from_union([from_none, from_bool], obj.get("isRentByParts"))
        is_top3 = from_union([from_none, from_bool], obj.get("isTop3"))
        jk_url = from_union([from_none, from_str], obj.get("jkUrl"))
        kitchen_area = from_union([from_float, from_none], obj.get("kitchenArea"))
        kp = from_union([from_none, from_str], obj.get("kp"))
        land = from_union([Land.from_dict, from_none], obj.get("land"))
        layout = from_union([from_none, Layout], obj.get("layout"))
        layout_photo = from_union([from_none, from_str], obj.get("layoutPhoto"))
        leisure = from_union([from_float, from_none], obj.get("leisure"))
        living_area = from_union([from_float, from_none], obj.get("livingArea"))
        loggias_count = from_union([from_int, from_none], obj.get("loggiasCount"))
        max_area = from_union([from_float, from_none], obj.get("maxArea"))
        min_area = from_union([from_none, from_str], obj.get("minArea"))
        min_price_total = from_union([from_float, from_none], obj.get("minPriceTotal"))
        min_price_total_per_month = from_union([from_float, from_none], obj.get("minPriceTotalPerMonth"))
        min_price_total_per_month_rur = from_union([from_float, from_none], obj.get("minPriceTotalPerMonthRur"))
        min_price_total_per_month_rur_for_search = from_union([from_none, from_str], obj.get("minPriceTotalPerMonthRurForSearch"))
        min_price_total_rur = from_union([from_int, from_none], obj.get("minPriceTotalRur"))
        min_price_total_rur_for_search = from_union([from_float, from_none], obj.get("minPriceTotalRurForSearch"))
        min_vat_price_total_per_month_rur = from_union([from_float, from_none], obj.get("minVatPriceTotalPerMonthRur"))
        min_vat_price_total_rur = from_union([from_int, from_none], obj.get("minVatPriceTotalRur"))
        monthly_income = from_union([MonthlyIncome.from_dict, from_none], obj.get("monthlyIncome"))
        name = from_union([from_none, from_str], obj.get("name"))
        newbuilding = from_union([Newbuilding.from_dict, from_none], obj.get("newbuilding"))
        notes = from_union([Notes.from_dict, from_none], obj.get("notes"))
        object_guid = from_union([lambda x: UUID(x), from_none], obj.get("objectGuid"))
        offer_type = OfferType(obj.get("offerType"))
        permitted_use_type = from_union([from_none, PermittedUseType], obj.get("permittedUseType"))
        pets_allowed = from_union([from_none, from_bool], obj.get("petsAllowed"))
        phone_lines_count = from_union([from_int, from_none], obj.get("phoneLinesCount"))
        phones = from_list(Phone.from_dict, obj.get("phones"))
        photos = from_list(Photo.from_dict, obj.get("photos"))
        placement_type = from_union([from_none, PlacementType], obj.get("placementType"))
        platform = from_union([Platform.from_dict, from_none], obj.get("platform"))
        possible_to_change_permitted_use_type = from_union([from_none, from_bool], obj.get("possibleToChangePermittedUseType"))
        price_changes = from_union([from_none, lambda x: from_list(PriceChange.from_dict, x)], obj.get("priceChanges"))
        price_per_unit_area = from_union([from_float, from_none], obj.get("pricePerUnitArea"))
        price_per_unit_area_eur = from_union([from_float, from_none], obj.get("pricePerUnitAreaEur"))
        price_per_unit_area_per_month = from_union([from_float, from_none], obj.get("pricePerUnitAreaPerMonth"))
        price_per_unit_area_per_month_rur = from_union([from_float, from_none], obj.get("pricePerUnitAreaPerMonthRur"))
        price_per_unit_area_per_month_rur_for_search = from_union([from_float, from_none], obj.get("pricePerUnitAreaPerMonthRurForSearch"))
        price_per_unit_area_per_year = from_union([from_float, from_none], obj.get("pricePerUnitAreaPerYear"))
        price_per_unit_area_per_year_eur = from_union([from_float, from_none], obj.get("pricePerUnitAreaPerYearEur"))
        price_per_unit_area_per_year_rur = from_union([from_float, from_none], obj.get("pricePerUnitAreaPerYearRur"))
        price_per_unit_area_per_year_rur_for_search = from_union([from_none, from_str], obj.get("pricePerUnitAreaPerYearRurForSearch"))
        price_per_unit_area_per_year_usd = from_union([from_float, from_none], obj.get("pricePerUnitAreaPerYearUsd"))
        price_per_unit_area_rur = from_union([from_float, from_none], obj.get("pricePerUnitAreaRur"))
        price_per_unit_area_rur_for_search = from_union([from_float, from_none], obj.get("pricePerUnitAreaRurForSearch"))
        price_per_unit_area_usd = from_union([from_float, from_none], obj.get("pricePerUnitAreaUsd"))
        price_total = from_union([from_float, from_none], obj.get("priceTotal"))
        price_total_eur = from_union([from_float, from_none], obj.get("priceTotalEur"))
        price_total_per_month = from_union([from_float, from_none], obj.get("priceTotalPerMonth"))
        price_total_per_month_eur = from_union([from_float, from_none], obj.get("priceTotalPerMonthEur"))
        price_total_per_month_rur = from_union([from_float, from_none], obj.get("priceTotalPerMonthRur"))
        price_total_per_month_rur_for_search = from_union([from_float, from_none], obj.get("priceTotalPerMonthRurForSearch"))
        price_total_per_month_usd = from_union([from_float, from_none], obj.get("priceTotalPerMonthUsd"))
        price_total_rur = from_union([from_float, from_none], obj.get("priceTotalRur"))
        price_total_rur_for_search = from_union([from_float, from_none], obj.get("priceTotalRurForSearch"))
        price_total_usd = from_union([from_float, from_none], obj.get("priceTotalUsd"))
        project_declaration_url = from_union([from_none, from_str], obj.get("projectDeclarationUrl"))
        promo_info = from_union([from_none, from_str], obj.get("promoInfo"))
        property_type = from_union([from_none, PropertyType], obj.get("propertyType"))
        published_user_id = from_int(obj.get("publishedUserId"))
        publish_terms = from_union([PublishTerms.from_dict, from_none], obj.get("publishTerms"))
        rent_by_parts_description = from_union([from_none, from_str], obj.get("rentByPartsDescription"))
        repair_type = from_union([from_none, RepairType], obj.get("repairType"))
        room_area = from_union([from_float, from_none], obj.get("roomArea"))
        rooms_area = from_union([from_float, from_none], obj.get("roomsArea"))
        rooms_count = from_union([from_int, from_none], obj.get("roomsCount"))
        rooms_for_sale_count = from_union([from_int, from_none], obj.get("roomsForSaleCount"))
        room_type = from_union([from_none, from_str], obj.get("roomType"))
        rosreestr_check = from_union([from_none, from_bool], obj.get("rosreestrCheck"))
        separate_wcs_count = from_union([from_int, from_none], obj.get("separateWcsCount"))
        settlement_name = from_union([from_none, from_str], obj.get("settlementName"))
        share_amount = from_union([from_none, from_str], obj.get("shareAmount"))
        similar = from_union([from_none, from_bool], obj.get("similar"))
        specialty = OffersSerializedSpecialty.from_dict(obj.get("specialty"))
        statistic = from_union([Statistic.from_dict, from_none], obj.get("statistic"))
        status = Status(obj.get("status"))
        tax_number = from_union([from_int, from_none], obj.get("taxNumber"))
        title = from_union([from_none, from_str], obj.get("title"))
        total_area = from_union([from_none, from_str], obj.get("totalArea"))
        user = User.from_dict(obj.get("user"))
        user_id = from_int(obj.get("userId"))
        value_added_services = from_union([ValueAddedServices.from_dict, from_none], obj.get("valueAddedServices"))
        vas_type = from_union([from_none, from_str], obj.get("vasType"))
        vat_price_total_per_month_rur = from_union([from_float, from_none], obj.get("vatPriceTotalPerMonthRur"))
        vat_price_total_rur = from_union([from_int, from_none], obj.get("vatPriceTotalRur"))
        videos = from_list(Video.from_dict, obj.get("videos"))
        water = from_union([Water.from_dict, from_none], obj.get("water"))
        water_capacity = from_union([from_float, from_none], obj.get("waterCapacity"))
        water_pipes_count = from_union([from_int, from_none], obj.get("waterPipesCount"))
        water_type = from_union([from_none, from_bool], obj.get("waterType"))
        wc_location_type = from_union([from_none, WcLocationType], obj.get("wcLocationType"))
        wc_type = from_union([from_int, from_none], obj.get("wcType"))
        windows_view_type = from_union([from_none, WindowsViewType], obj.get("windowsViewType"))
        without_client_fee = from_union([from_none, from_bool], obj.get("withoutClientFee"))
        work_time_info = from_union([from_none, from_str], obj.get("workTimeInfo"))
        return OffersSerialized(access_type, added, additional_phone_lines_allowed, all_from_offrep, all_rooms_area, archived_date, available_from, balconies_count, bargain_terms, bedrooms_count, beds_count, booking, building, business_shopping_center, call_tracking_provider, can_parts, categories_ids, category, chat_id, children_allowed, cian_id, cian_user_id, combined_wcs_count, condition_rating_type, condition_type, cpl_moderation, deal_type, decoration, demolished_in_moscow_programm, description, description_minhash, district, drainage, drainage_capacity, drainage_type, driveway_type, edit_date, electricity, electricity_power, electricity_type, estate_type, external_id, external_url, feedbox_multi_offer_key, flags, flat_type, floor_material_type, floor_number, from_developer, furniture, furniture_presence, ga_label, garage, gas, gas_capacity, gas_pressure, gas_type, geo, has_bathhouse, has_bathtub, has_check_in_24, has_conditioner, has_dishwasher, has_drainage, has_electricity, has_encumbrances, has_equipment, has_excursions, has_extinguishing_system, has_fridge, has_furniture, has_garage, has_gas, has_hairdryer, has_heating, has_internet, has_investment_project, has_iron, has_jacuzzi, has_kitchen_furniture, has_lift, has_light, has_parking, has_phone, has_pool, has_ramp, has_safe_custody, has_seconded_docs, has_security, has_shop_windows, has_shower, has_tea_coffee_sugar, has_transfer, has_transport_services, has_tv, has_washer, has_water, has_wifi, has_wired_internet, id, input_type, is_apartments, is_auction, is_by_homeowner, is_colorized, is_customs, is_duplicated_description, is_enabled_call_tracking, is_fairplay, is_favorite, is_from_builder, is_hidden_by_user, is_in_hidden_base, is_legal_address_provided, is_new, is_occupied, is_paid, is_penthouse, is_premium, is_pro, is_rent_by_parts, is_top3, jk_url, kitchen_area, kp, land, layout, layout_photo, leisure, living_area, loggias_count, max_area, min_area, min_price_total, min_price_total_per_month, min_price_total_per_month_rur, min_price_total_per_month_rur_for_search, min_price_total_rur, min_price_total_rur_for_search, min_vat_price_total_per_month_rur, min_vat_price_total_rur, monthly_income, name, newbuilding, notes, object_guid, offer_type, permitted_use_type, pets_allowed, phone_lines_count, phones, photos, placement_type, platform, possible_to_change_permitted_use_type, price_changes, price_per_unit_area, price_per_unit_area_eur, price_per_unit_area_per_month, price_per_unit_area_per_month_rur, price_per_unit_area_per_month_rur_for_search, price_per_unit_area_per_year, price_per_unit_area_per_year_eur, price_per_unit_area_per_year_rur, price_per_unit_area_per_year_rur_for_search, price_per_unit_area_per_year_usd, price_per_unit_area_rur, price_per_unit_area_rur_for_search, price_per_unit_area_usd, price_total, price_total_eur, price_total_per_month, price_total_per_month_eur, price_total_per_month_rur, price_total_per_month_rur_for_search, price_total_per_month_usd, price_total_rur, price_total_rur_for_search, price_total_usd, project_declaration_url, promo_info, property_type, published_user_id, publish_terms, rent_by_parts_description, repair_type, room_area, rooms_area, rooms_count, rooms_for_sale_count, room_type, rosreestr_check, separate_wcs_count, settlement_name, share_amount, similar, specialty, statistic, status, tax_number, title, total_area, user, user_id, value_added_services, vas_type, vat_price_total_per_month_rur, vat_price_total_rur, videos, water, water_capacity, water_pipes_count, water_type, wc_location_type, wc_type, windows_view_type, without_client_fee, work_time_info)

    def to_dict(self) -> dict:
        result: dict = {}
        result["accessType"] = from_union([from_none, lambda x: to_enum(AccessTypeEnum, x)], self.access_type)
        result["added"] = from_str(self.added)
        result["additionalPhoneLinesAllowed"] = from_union([from_int, from_none], self.additional_phone_lines_allowed)
        result["allFromOffrep"] = from_union([lambda x: to_class(AllFromOffrep, x), from_none], self.all_from_offrep)
        result["allRoomsArea"] = from_union([to_float, from_none], self.all_rooms_area)
        result["archivedDate"] = from_union([from_none, lambda x: x.isoformat()], self.archived_date)
        result["availableFrom"] = from_union([from_none, lambda x: x.isoformat()], self.available_from)
        result["balconiesCount"] = from_union([from_int, from_none], self.balconies_count)
        result["bargainTerms"] = to_class(BargainTerms, self.bargain_terms)
        result["bedroomsCount"] = from_union([from_int, from_none], self.bedrooms_count)
        result["bedsCount"] = from_union([from_int, from_none], self.beds_count)
        result["booking"] = from_union([from_none, from_str], self.booking)
        result["building"] = to_class(Building, self.building)
        result["businessShoppingCenter"] = from_union([lambda x: to_class(BusinessShoppingCenter, x), from_none], self.business_shopping_center)
        result["callTrackingProvider"] = from_union([from_none, lambda x: to_enum(CallTrackingProvider, x)], self.call_tracking_provider)
        result["canParts"] = from_union([from_none, from_bool], self.can_parts)
        result["categoriesIds"] = from_list(from_int, self.categories_ids)
        result["category"] = to_enum(Category, self.category)
        result["chatId"] = from_union([from_none, from_str], self.chat_id)
        result["childrenAllowed"] = from_union([from_none, from_bool], self.children_allowed)
        result["cianId"] = from_int(self.cian_id)
        result["cianUserId"] = from_union([from_int, from_none], self.cian_user_id)
        result["combinedWcsCount"] = from_union([from_int, from_none], self.combined_wcs_count)
        result["conditionRatingType"] = from_union([from_none, from_str], self.condition_rating_type)
        result["conditionType"] = from_union([from_none, lambda x: to_enum(ConditionType, x)], self.condition_type)
        result["cplModeration"] = from_union([from_none, from_str], self.cpl_moderation)
        result["dealType"] = to_enum(DealTypeEnum, self.deal_type)
        result["decoration"] = from_union([from_none, lambda x: to_enum(Decoration, x)], self.decoration)
        result["demolishedInMoscowProgramm"] = from_union([from_none, from_bool], self.demolished_in_moscow_programm)
        result["description"] = from_str(self.description)
        result["descriptionMinhash"] = from_union([lambda x: from_list(from_int, x), from_none], self.description_minhash)
        result["district"] = from_union([from_none, from_str], self.district)
        result["drainage"] = from_union([from_none, from_str], self.drainage)
        result["drainageCapacity"] = from_union([to_float, from_none], self.drainage_capacity)
        result["drainageType"] = from_union([from_none, from_str], self.drainage_type)
        result["drivewayType"] = from_union([from_none, lambda x: to_enum(DrivewayType, x)], self.driveway_type)
        result["editDate"] = from_union([from_none, lambda x: x.isoformat()], self.edit_date)
        result["electricity"] = from_union([lambda x: to_class(Electricity, x), from_none], self.electricity)
        result["electricityPower"] = from_union([to_float, from_none], self.electricity_power)
        result["electricityType"] = from_union([from_none, from_bool], self.electricity_type)
        result["estateType"] = from_union([from_none, lambda x: to_enum(EstateTypeEnum, x)], self.estate_type)
        result["externalId"] = from_union([from_none, from_str], self.external_id)
        result["externalUrl"] = from_union([from_none, from_str], self.external_url)
        result["feedboxMultiOfferKey"] = from_union([from_none, from_str], self.feedbox_multi_offer_key)
        result["flags"] = from_union([lambda x: to_class(Flags, x), from_none], self.flags)
        result["flatType"] = from_union([from_none, from_str], self.flat_type)
        result["floorMaterialType"] = from_union([from_none, from_str], self.floor_material_type)
        result["floorNumber"] = from_union([from_int, from_none], self.floor_number)
        result["fromDeveloper"] = from_union([from_none, from_bool], self.from_developer)
        result["furniture"] = from_union([from_none, from_str], self.furniture)
        result["furniturePresence"] = from_union([from_none, from_str], self.furniture_presence)
        result["gaLabel"] = from_str(self.ga_label)
        result["garage"] = from_union([lambda x: to_class(Garage, x), from_none], self.garage)
        result["gas"] = from_union([lambda x: to_class(Gas, x), from_none], self.gas)
        result["gasCapacity"] = from_union([from_int, from_none], self.gas_capacity)
        result["gasPressure"] = from_union([from_none, lambda x: to_enum(PressureType, x)], self.gas_pressure)
        result["gasType"] = from_union([from_none, from_str], self.gas_type)
        result["geo"] = to_class(OffersSerializedGeo, self.geo)
        result["hasBathhouse"] = from_union([from_none, from_bool], self.has_bathhouse)
        result["hasBathtub"] = from_union([from_none, from_bool], self.has_bathtub)
        result["hasCheckIn_24"] = from_union([from_none, from_bool], self.has_check_in_24)
        result["hasConditioner"] = from_union([from_none, from_bool], self.has_conditioner)
        result["hasDishwasher"] = from_union([from_none, from_bool], self.has_dishwasher)
        result["hasDrainage"] = from_union([from_none, from_bool], self.has_drainage)
        result["hasElectricity"] = from_union([from_none, from_bool], self.has_electricity)
        result["hasEncumbrances"] = from_union([from_none, from_bool], self.has_encumbrances)
        result["hasEquipment"] = from_union([from_none, from_bool], self.has_equipment)
        result["hasExcursions"] = from_union([from_none, from_bool], self.has_excursions)
        result["hasExtinguishingSystem"] = from_union([from_none, from_bool], self.has_extinguishing_system)
        result["hasFridge"] = from_union([from_none, from_bool], self.has_fridge)
        result["hasFurniture"] = from_union([from_none, from_bool], self.has_furniture)
        result["hasGarage"] = from_union([from_none, from_bool], self.has_garage)
        result["hasGas"] = from_union([from_none, from_bool], self.has_gas)
        result["hasHairdryer"] = from_union([from_none, from_bool], self.has_hairdryer)
        result["hasHeating"] = from_union([from_none, from_bool], self.has_heating)
        result["hasInternet"] = from_union([from_none, from_bool], self.has_internet)
        result["hasInvestmentProject"] = from_union([from_none, from_bool], self.has_investment_project)
        result["hasIron"] = from_union([from_none, from_bool], self.has_iron)
        result["hasJacuzzi"] = from_union([from_none, from_bool], self.has_jacuzzi)
        result["hasKitchenFurniture"] = from_union([from_none, from_bool], self.has_kitchen_furniture)
        result["hasLift"] = from_union([from_none, from_bool], self.has_lift)
        result["hasLight"] = from_union([from_none, from_bool], self.has_light)
        result["hasParking"] = from_union([from_none, from_bool], self.has_parking)
        result["hasPhone"] = from_union([from_none, from_bool], self.has_phone)
        result["hasPool"] = from_union([from_none, from_bool], self.has_pool)
        result["hasRamp"] = from_union([from_none, from_bool], self.has_ramp)
        result["hasSafeCustody"] = from_union([from_none, from_bool], self.has_safe_custody)
        result["hasSecondedDocs"] = from_union([from_none, from_bool], self.has_seconded_docs)
        result["hasSecurity"] = from_union([from_none, from_bool], self.has_security)
        result["hasShopWindows"] = from_union([from_none, from_bool], self.has_shop_windows)
        result["hasShower"] = from_union([from_none, from_bool], self.has_shower)
        result["hasTeaCoffeeSugar"] = from_union([from_none, from_bool], self.has_tea_coffee_sugar)
        result["hasTransfer"] = from_union([from_none, from_bool], self.has_transfer)
        result["hasTransportServices"] = from_union([from_none, from_bool], self.has_transport_services)
        result["hasTv"] = from_union([from_none, from_bool], self.has_tv)
        result["hasWasher"] = from_union([from_none, from_bool], self.has_washer)
        result["hasWater"] = from_union([from_none, from_bool], self.has_water)
        result["hasWifi"] = from_union([from_none, from_bool], self.has_wifi)
        result["hasWiredInternet"] = from_union([from_none, from_bool], self.has_wired_internet)
        result["id"] = from_int(self.id)
        result["inputType"] = from_union([from_none, lambda x: to_enum(InputType, x)], self.input_type)
        result["isApartments"] = from_union([from_none, from_bool], self.is_apartments)
        result["isAuction"] = from_union([from_none, from_bool], self.is_auction)
        result["isByHomeowner"] = from_union([from_none, from_bool], self.is_by_homeowner)
        result["isColorized"] = from_union([from_none, from_bool], self.is_colorized)
        result["isCustoms"] = from_union([from_none, from_bool], self.is_customs)
        result["isDuplicatedDescription"] = from_union([from_none, from_bool], self.is_duplicated_description)
        result["isEnabledCallTracking"] = from_union([from_none, from_bool], self.is_enabled_call_tracking)
        result["isFairplay"] = from_union([from_none, from_bool], self.is_fairplay)
        result["isFavorite"] = from_union([from_none, from_bool], self.is_favorite)
        result["isFromBuilder"] = from_union([from_none, from_bool], self.is_from_builder)
        result["isHiddenByUser"] = from_union([from_none, from_bool], self.is_hidden_by_user)
        result["isInHiddenBase"] = from_union([from_none, from_bool], self.is_in_hidden_base)
        result["isLegalAddressProvided"] = from_union([from_none, from_bool], self.is_legal_address_provided)
        result["isNew"] = from_union([from_none, from_bool], self.is_new)
        result["isOccupied"] = from_union([from_none, from_bool], self.is_occupied)
        result["isPaid"] = from_union([from_none, from_bool], self.is_paid)
        result["isPenthouse"] = from_union([from_none, from_bool], self.is_penthouse)
        result["isPremium"] = from_union([from_none, from_bool], self.is_premium)
        result["isPro"] = from_union([from_none, from_bool], self.is_pro)
        result["isRentByParts"] = from_union([from_none, from_bool], self.is_rent_by_parts)
        result["isTop3"] = from_union([from_none, from_bool], self.is_top3)
        result["jkUrl"] = from_union([from_none, from_str], self.jk_url)
        result["kitchenArea"] = from_union([to_float, from_none], self.kitchen_area)
        result["kp"] = from_union([from_none, from_str], self.kp)
        result["land"] = from_union([lambda x: to_class(Land, x), from_none], self.land)
        result["layout"] = from_union([from_none, lambda x: to_enum(Layout, x)], self.layout)
        result["layoutPhoto"] = from_union([from_none, from_str], self.layout_photo)
        result["leisure"] = from_union([to_float, from_none], self.leisure)
        result["livingArea"] = from_union([to_float, from_none], self.living_area)
        result["loggiasCount"] = from_union([from_int, from_none], self.loggias_count)
        result["maxArea"] = from_union([to_float, from_none], self.max_area)
        result["minArea"] = from_union([from_none, from_str], self.min_area)
        result["minPriceTotal"] = from_union([to_float, from_none], self.min_price_total)
        result["minPriceTotalPerMonth"] = from_union([to_float, from_none], self.min_price_total_per_month)
        result["minPriceTotalPerMonthRur"] = from_union([to_float, from_none], self.min_price_total_per_month_rur)
        result["minPriceTotalPerMonthRurForSearch"] = from_union([from_none, from_str], self.min_price_total_per_month_rur_for_search)
        result["minPriceTotalRur"] = from_union([from_int, from_none], self.min_price_total_rur)
        result["minPriceTotalRurForSearch"] = from_union([to_float, from_none], self.min_price_total_rur_for_search)
        result["minVatPriceTotalPerMonthRur"] = from_union([to_float, from_none], self.min_vat_price_total_per_month_rur)
        result["minVatPriceTotalRur"] = from_union([from_int, from_none], self.min_vat_price_total_rur)
        result["monthlyIncome"] = from_union([lambda x: to_class(MonthlyIncome, x), from_none], self.monthly_income)
        result["name"] = from_union([from_none, from_str], self.name)
        result["newbuilding"] = from_union([lambda x: to_class(Newbuilding, x), from_none], self.newbuilding)
        result["notes"] = from_union([lambda x: to_class(Notes, x), from_none], self.notes)
        result["objectGuid"] = from_union([lambda x: str(x), from_none], self.object_guid)
        result["offerType"] = to_enum(OfferType, self.offer_type)
        result["permittedUseType"] = from_union([from_none, lambda x: to_enum(PermittedUseType, x)], self.permitted_use_type)
        result["petsAllowed"] = from_union([from_none, from_bool], self.pets_allowed)
        result["phoneLinesCount"] = from_union([from_int, from_none], self.phone_lines_count)
        result["phones"] = from_list(lambda x: to_class(Phone, x), self.phones)
        result["photos"] = from_list(lambda x: to_class(Photo, x), self.photos)
        result["placementType"] = from_union([from_none, lambda x: to_enum(PlacementType, x)], self.placement_type)
        result["platform"] = from_union([lambda x: to_class(Platform, x), from_none], self.platform)
        result["possibleToChangePermittedUseType"] = from_union([from_none, from_bool], self.possible_to_change_permitted_use_type)
        result["priceChanges"] = from_union([from_none, lambda x: from_list(lambda x: to_class(PriceChange, x), x)], self.price_changes)
        result["pricePerUnitArea"] = from_union([to_float, from_none], self.price_per_unit_area)
        result["pricePerUnitAreaEur"] = from_union([to_float, from_none], self.price_per_unit_area_eur)
        result["pricePerUnitAreaPerMonth"] = from_union([to_float, from_none], self.price_per_unit_area_per_month)
        result["pricePerUnitAreaPerMonthRur"] = from_union([to_float, from_none], self.price_per_unit_area_per_month_rur)
        result["pricePerUnitAreaPerMonthRurForSearch"] = from_union([to_float, from_none], self.price_per_unit_area_per_month_rur_for_search)
        result["pricePerUnitAreaPerYear"] = from_union([to_float, from_none], self.price_per_unit_area_per_year)
        result["pricePerUnitAreaPerYearEur"] = from_union([to_float, from_none], self.price_per_unit_area_per_year_eur)
        result["pricePerUnitAreaPerYearRur"] = from_union([to_float, from_none], self.price_per_unit_area_per_year_rur)
        result["pricePerUnitAreaPerYearRurForSearch"] = from_union([from_none, from_str], self.price_per_unit_area_per_year_rur_for_search)
        result["pricePerUnitAreaPerYearUsd"] = from_union([to_float, from_none], self.price_per_unit_area_per_year_usd)
        result["pricePerUnitAreaRur"] = from_union([to_float, from_none], self.price_per_unit_area_rur)
        result["pricePerUnitAreaRurForSearch"] = from_union([to_float, from_none], self.price_per_unit_area_rur_for_search)
        result["pricePerUnitAreaUsd"] = from_union([to_float, from_none], self.price_per_unit_area_usd)
        result["priceTotal"] = from_union([to_float, from_none], self.price_total)
        result["priceTotalEur"] = from_union([to_float, from_none], self.price_total_eur)
        result["priceTotalPerMonth"] = from_union([to_float, from_none], self.price_total_per_month)
        result["priceTotalPerMonthEur"] = from_union([to_float, from_none], self.price_total_per_month_eur)
        result["priceTotalPerMonthRur"] = from_union([to_float, from_none], self.price_total_per_month_rur)
        result["priceTotalPerMonthRurForSearch"] = from_union([to_float, from_none], self.price_total_per_month_rur_for_search)
        result["priceTotalPerMonthUsd"] = from_union([to_float, from_none], self.price_total_per_month_usd)
        result["priceTotalRur"] = from_union([to_float, from_none], self.price_total_rur)
        result["priceTotalRurForSearch"] = from_union([to_float, from_none], self.price_total_rur_for_search)
        result["priceTotalUsd"] = from_union([to_float, from_none], self.price_total_usd)
        result["projectDeclarationUrl"] = from_union([from_none, from_str], self.project_declaration_url)
        result["promoInfo"] = from_union([from_none, from_str], self.promo_info)
        result["propertyType"] = from_union([from_none, lambda x: to_enum(PropertyType, x)], self.property_type)
        result["publishedUserId"] = from_int(self.published_user_id)
        result["publishTerms"] = from_union([lambda x: to_class(PublishTerms, x), from_none], self.publish_terms)
        result["rentByPartsDescription"] = from_union([from_none, from_str], self.rent_by_parts_description)
        result["repairType"] = from_union([from_none, lambda x: to_enum(RepairType, x)], self.repair_type)
        result["roomArea"] = from_union([to_float, from_none], self.room_area)
        result["roomsArea"] = from_union([to_float, from_none], self.rooms_area)
        result["roomsCount"] = from_union([from_int, from_none], self.rooms_count)
        result["roomsForSaleCount"] = from_union([from_int, from_none], self.rooms_for_sale_count)
        result["roomType"] = from_union([from_none, from_str], self.room_type)
        result["rosreestrCheck"] = from_union([from_none, from_bool], self.rosreestr_check)
        result["separateWcsCount"] = from_union([from_int, from_none], self.separate_wcs_count)
        result["settlementName"] = from_union([from_none, from_str], self.settlement_name)
        result["shareAmount"] = from_union([from_none, from_str], self.share_amount)
        result["similar"] = from_union([from_none, from_bool], self.similar)
        result["specialty"] = to_class(OffersSerializedSpecialty, self.specialty)
        result["statistic"] = from_union([lambda x: to_class(Statistic, x), from_none], self.statistic)
        result["status"] = to_enum(Status, self.status)
        result["taxNumber"] = from_union([from_int, from_none], self.tax_number)
        result["title"] = from_union([from_none, from_str], self.title)
        result["totalArea"] = from_union([from_none, from_str], self.total_area)
        result["user"] = to_class(User, self.user)
        result["userId"] = from_int(self.user_id)
        result["valueAddedServices"] = from_union([lambda x: to_class(ValueAddedServices, x), from_none], self.value_added_services)
        result["vasType"] = from_union([from_none, from_str], self.vas_type)
        result["vatPriceTotalPerMonthRur"] = from_union([to_float, from_none], self.vat_price_total_per_month_rur)
        result["vatPriceTotalRur"] = from_union([from_int, from_none], self.vat_price_total_rur)
        result["videos"] = from_list(lambda x: to_class(Video, x), self.videos)
        result["water"] = from_union([lambda x: to_class(Water, x), from_none], self.water)
        result["waterCapacity"] = from_union([to_float, from_none], self.water_capacity)
        result["waterPipesCount"] = from_union([from_int, from_none], self.water_pipes_count)
        result["waterType"] = from_union([from_none, from_bool], self.water_type)
        result["wcLocationType"] = from_union([from_none, lambda x: to_enum(WcLocationType, x)], self.wc_location_type)
        result["wcType"] = from_union([from_int, from_none], self.wc_type)
        result["windowsViewType"] = from_union([from_none, lambda x: to_enum(WindowsViewType, x)], self.windows_view_type)
        result["withoutClientFee"] = from_union([from_none, from_bool], self.without_client_fee)
        result["workTimeInfo"] = from_union([from_none, from_str], self.work_time_info)
        return result


class SEOData:
    description: str
    h1: str
    meta_description: str
    noindex: bool
    title: str

    def __init__(self, description: str, h1: str, meta_description: str, noindex: bool, title: str) -> None:
        self.description = description
        self.h1 = h1
        self.meta_description = meta_description
        self.noindex = noindex
        self.title = title

    @staticmethod
    def from_dict(obj: Any) -> 'SEOData':
        assert isinstance(obj, dict)
        description = from_str(obj.get("description"))
        h1 = from_str(obj.get("h1"))
        meta_description = from_str(obj.get("metaDescription"))
        noindex = from_bool(obj.get("noindex"))
        title = from_str(obj.get("title"))
        return SEOData(description, h1, meta_description, noindex, title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_str(self.description)
        result["h1"] = from_str(self.h1)
        result["metaDescription"] = from_str(self.meta_description)
        result["noindex"] = from_bool(self.noindex)
        result["title"] = from_str(self.title)
        return result


class DataClass:
    aggregated_count: int
    breadcrumbs: List[Breadcrumb]
    full_url: Optional[str]
    is_call_button_enabled: Optional[bool]
    is_newobjects_enabled: Optional[bool]
    json_query: JSONQuery
    ml_ranking_guid: Optional[UUID]
    offer_count: int
    offers_serialized: List[OffersSerialized]
    query_string: str
    search_uuid: Optional[str]
    seo_data: SEOData
    suggestions_query: Optional[str]
    top3_is_on: Optional[bool]

    def __init__(self, aggregated_count: int, breadcrumbs: List[Breadcrumb], full_url: Optional[str], is_call_button_enabled: Optional[bool], is_newobjects_enabled: Optional[bool], json_query: JSONQuery, ml_ranking_guid: Optional[UUID], offer_count: int, offers_serialized: List[OffersSerialized], query_string: str, search_uuid: Optional[str], seo_data: SEOData, suggestions_query: Optional[str], top3_is_on: Optional[bool]) -> None:
        self.aggregated_count = aggregated_count
        self.breadcrumbs = breadcrumbs
        self.full_url = full_url
        self.is_call_button_enabled = is_call_button_enabled
        self.is_newobjects_enabled = is_newobjects_enabled
        self.json_query = json_query
        self.ml_ranking_guid = ml_ranking_guid
        self.offer_count = offer_count
        self.offers_serialized = offers_serialized
        self.query_string = query_string
        self.search_uuid = search_uuid
        self.seo_data = seo_data
        self.suggestions_query = suggestions_query
        self.top3_is_on = top3_is_on

    @staticmethod
    def from_dict(obj: Any) -> 'DataClass':
        assert isinstance(obj, dict)
        aggregated_count = from_int(obj.get("aggregatedCount"))
        breadcrumbs = from_list(Breadcrumb.from_dict, obj.get("breadcrumbs"))
        full_url = from_union([from_str, from_none], obj.get("fullUrl"))
        is_call_button_enabled = from_union([from_none, from_bool], obj.get("isCallButtonEnabled"))
        is_newobjects_enabled = from_union([from_none, from_bool], obj.get("isNewobjectsEnabled"))
        json_query = JSONQuery.from_dict(obj.get("jsonQuery"))
        ml_ranking_guid = from_union([lambda x: UUID(x), from_none], obj.get("mlRankingGuid"))
        offer_count = from_int(obj.get("offerCount"))
        offers_serialized = from_list(OffersSerialized.from_dict, obj.get("offersSerialized"))
        query_string = from_str(obj.get("queryString"))
        search_uuid = from_union([from_none, from_str], obj.get("searchUuid"))
        seo_data = SEOData.from_dict(obj.get("seoData"))
        suggestions_query = from_union([from_none, from_str], obj.get("suggestionsQuery"))
        top3_is_on = from_union([from_none, from_bool], obj.get("top3IsOn"))
        return DataClass(aggregated_count, breadcrumbs, full_url, is_call_button_enabled, is_newobjects_enabled, json_query, ml_ranking_guid, offer_count, offers_serialized, query_string, search_uuid, seo_data, suggestions_query, top3_is_on)

    def to_dict(self) -> dict:
        result: dict = {}
        result["aggregatedCount"] = from_int(self.aggregated_count)
        result["breadcrumbs"] = from_list(lambda x: to_class(Breadcrumb, x), self.breadcrumbs)
        result["fullUrl"] = from_union([from_str, from_none], self.full_url)
        result["isCallButtonEnabled"] = from_union([from_none, from_bool], self.is_call_button_enabled)
        result["isNewobjectsEnabled"] = from_union([from_none, from_bool], self.is_newobjects_enabled)
        result["jsonQuery"] = to_class(JSONQuery, self.json_query)
        result["mlRankingGuid"] = from_union([lambda x: str(x), from_none], self.ml_ranking_guid)
        result["offerCount"] = from_int(self.offer_count)
        result["offersSerialized"] = from_list(lambda x: to_class(OffersSerialized, x), self.offers_serialized)
        result["queryString"] = from_str(self.query_string)
        result["searchUuid"] = from_union([from_none, from_str], self.search_uuid)
        result["seoData"] = to_class(SEOData, self.seo_data)
        result["suggestionsQuery"] = from_union([from_none, from_str], self.suggestions_query)
        result["top3IsOn"] = from_union([from_none, from_bool], self.top3_is_on)
        return result


class Data:
    data: DataClass
    status: str

    def __init__(self, data: DataClass, status: str) -> None:
        self.data = data
        self.status = status

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        assert isinstance(obj, dict)
        data = DataClass.from_dict(obj.get("data"))
        status = from_str(obj.get("status"))
        return Data(data, status)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = to_class(DataClass, self.data)
        result["status"] = from_str(self.status)
        return result


def data_from_dict(s: Any) -> Data:
    return Data.from_dict(s)


def data_to_dict(x: Data) -> Any:
    return to_class(Data, x)

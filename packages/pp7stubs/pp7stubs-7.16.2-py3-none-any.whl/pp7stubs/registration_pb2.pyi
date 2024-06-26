from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Success: _ClassVar[Status]
    ExpiredLicense: _ClassVar[Status]
    DeactivatedLicense: _ClassVar[Status]
    DisabledLicense: _ClassVar[Status]
    NoSeats: _ClassVar[Status]
    NoCopies: _ClassVar[Status]
    MissingLicense: _ClassVar[Status]
    TimeDiscrepancy: _ClassVar[Status]
    BibleMissing: _ClassVar[Status]
    BibleNotPurchased: _ClassVar[Status]
    BibleActivationMissing: _ClassVar[Status]
    BibleDeactivated: _ClassVar[Status]
    NetworkError: _ClassVar[Status]
    IOError: _ClassVar[Status]
    NotInitialized: _ClassVar[Status]
    UnknownError: _ClassVar[Status]

class SeatType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Inactive: _ClassVar[SeatType]
    Basic: _ClassVar[SeatType]
    Advanced: _ClassVar[SeatType]

class LicenseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Trial: _ClassVar[LicenseType]
    Rental: _ClassVar[LicenseType]
    Standard: _ClassVar[LicenseType]
    Campus: _ClassVar[LicenseType]

class UpdateChannel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Beta: _ClassVar[UpdateChannel]
    Production: _ClassVar[UpdateChannel]

class AlertType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Info: _ClassVar[AlertType]
    Feature: _ClassVar[AlertType]
    Warning: _ClassVar[AlertType]

class AlertContentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ContentType: _ClassVar[AlertContentType]
    Text: _ClassVar[AlertContentType]
    InternalLink: _ClassVar[AlertContentType]
    ExternalLink: _ClassVar[AlertContentType]

class ReadTokenStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ReadTokenSuccess: _ClassVar[ReadTokenStatus]
    TokenNotPresent: _ClassVar[ReadTokenStatus]

class ProContentLicenseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Free: _ClassVar[ProContentLicenseType]
    Premium: _ClassVar[ProContentLicenseType]

class PopupAlertMessage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NoPopupAlert: _ClassVar[PopupAlertMessage]
    Activation: _ClassVar[PopupAlertMessage]
    ActivationNoSeat: _ClassVar[PopupAlertMessage]
    NotSignedIn: _ClassVar[PopupAlertMessage]
    SignedInNoSubscription: _ClassVar[PopupAlertMessage]

class BannerMessage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NoBanner: _ClassVar[BannerMessage]
    ActivateProPresenter: _ClassVar[BannerMessage]
Success: Status
ExpiredLicense: Status
DeactivatedLicense: Status
DisabledLicense: Status
NoSeats: Status
NoCopies: Status
MissingLicense: Status
TimeDiscrepancy: Status
BibleMissing: Status
BibleNotPurchased: Status
BibleActivationMissing: Status
BibleDeactivated: Status
NetworkError: Status
IOError: Status
NotInitialized: Status
UnknownError: Status
Inactive: SeatType
Basic: SeatType
Advanced: SeatType
Trial: LicenseType
Rental: LicenseType
Standard: LicenseType
Campus: LicenseType
Beta: UpdateChannel
Production: UpdateChannel
Info: AlertType
Feature: AlertType
Warning: AlertType
ContentType: AlertContentType
Text: AlertContentType
InternalLink: AlertContentType
ExternalLink: AlertContentType
ReadTokenSuccess: ReadTokenStatus
TokenNotPresent: ReadTokenStatus
Free: ProContentLicenseType
Premium: ProContentLicenseType
NoPopupAlert: PopupAlertMessage
Activation: PopupAlertMessage
ActivationNoSeat: PopupAlertMessage
NotSignedIn: PopupAlertMessage
SignedInNoSubscription: PopupAlertMessage
NoBanner: BannerMessage
ActivateProPresenter: BannerMessage

class Request(_message.Message):
    __slots__ = ("register", "unregister", "change_seat_type", "get_free_bibles", "get_purchased_bibles", "activate_bible", "deactivate_bible", "download_bible", "registration_data", "product_information", "get_upgrades_available", "get_downgrade_available", "download_new_version", "refresh", "activate_link", "update_token", "old_token_data")
    REGISTER_FIELD_NUMBER: _ClassVar[int]
    UNREGISTER_FIELD_NUMBER: _ClassVar[int]
    CHANGE_SEAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    GET_FREE_BIBLES_FIELD_NUMBER: _ClassVar[int]
    GET_PURCHASED_BIBLES_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_BIBLE_FIELD_NUMBER: _ClassVar[int]
    DEACTIVATE_BIBLE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_BIBLE_FIELD_NUMBER: _ClassVar[int]
    REGISTRATION_DATA_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_INFORMATION_FIELD_NUMBER: _ClassVar[int]
    GET_UPGRADES_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    GET_DOWNGRADE_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_NEW_VERSION_FIELD_NUMBER: _ClassVar[int]
    REFRESH_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_LINK_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    OLD_TOKEN_DATA_FIELD_NUMBER: _ClassVar[int]
    register: Register
    unregister: Unregister
    change_seat_type: ChangeSeatType
    get_free_bibles: GetFreeBibles
    get_purchased_bibles: GetPurchasedBibles
    activate_bible: ActivateBible
    deactivate_bible: DeactivateBible
    download_bible: DownloadBible
    registration_data: RegistrationData
    product_information: ProductInformation
    get_upgrades_available: GetAvailableVersion
    get_downgrade_available: GetAvailableVersion
    download_new_version: DownloadNewVersion
    refresh: Refresh
    activate_link: ActivateLink
    update_token: UpdateToken
    old_token_data: OldTokenData
    def __init__(self, register: _Optional[_Union[Register, _Mapping]] = ..., unregister: _Optional[_Union[Unregister, _Mapping]] = ..., change_seat_type: _Optional[_Union[ChangeSeatType, _Mapping]] = ..., get_free_bibles: _Optional[_Union[GetFreeBibles, _Mapping]] = ..., get_purchased_bibles: _Optional[_Union[GetPurchasedBibles, _Mapping]] = ..., activate_bible: _Optional[_Union[ActivateBible, _Mapping]] = ..., deactivate_bible: _Optional[_Union[DeactivateBible, _Mapping]] = ..., download_bible: _Optional[_Union[DownloadBible, _Mapping]] = ..., registration_data: _Optional[_Union[RegistrationData, _Mapping]] = ..., product_information: _Optional[_Union[ProductInformation, _Mapping]] = ..., get_upgrades_available: _Optional[_Union[GetAvailableVersion, _Mapping]] = ..., get_downgrade_available: _Optional[_Union[GetAvailableVersion, _Mapping]] = ..., download_new_version: _Optional[_Union[DownloadNewVersion, _Mapping]] = ..., refresh: _Optional[_Union[Refresh, _Mapping]] = ..., activate_link: _Optional[_Union[ActivateLink, _Mapping]] = ..., update_token: _Optional[_Union[UpdateToken, _Mapping]] = ..., old_token_data: _Optional[_Union[OldTokenData, _Mapping]] = ...) -> None: ...

class Callback(_message.Message):
    __slots__ = ("set_watermark", "deactivation_complete", "free_bibles", "purchased_bibles", "bible_activation_complete", "bible_deactivation_complete", "bible_download_progress", "hard_exit", "read_registration_data", "write_registration_data", "get_product_information", "log", "upgrades_available", "downgrade_available", "download_progress", "alerts", "show_expiration_dialog", "read_old_token", "token", "verification_complete")
    SET_WATERMARK_FIELD_NUMBER: _ClassVar[int]
    DEACTIVATION_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    FREE_BIBLES_FIELD_NUMBER: _ClassVar[int]
    PURCHASED_BIBLES_FIELD_NUMBER: _ClassVar[int]
    BIBLE_ACTIVATION_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    BIBLE_DEACTIVATION_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    BIBLE_DOWNLOAD_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    HARD_EXIT_FIELD_NUMBER: _ClassVar[int]
    READ_REGISTRATION_DATA_FIELD_NUMBER: _ClassVar[int]
    WRITE_REGISTRATION_DATA_FIELD_NUMBER: _ClassVar[int]
    GET_PRODUCT_INFORMATION_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    UPGRADES_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    DOWNGRADE_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    ALERTS_FIELD_NUMBER: _ClassVar[int]
    SHOW_EXPIRATION_DIALOG_FIELD_NUMBER: _ClassVar[int]
    READ_OLD_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    VERIFICATION_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    set_watermark: SetWatermark
    deactivation_complete: DeactivationComplete
    free_bibles: FreeBibles
    purchased_bibles: PurchasedBibles
    bible_activation_complete: BibleActivationComplete
    bible_deactivation_complete: BibleDeactivationComplete
    bible_download_progress: BibleDownloadProgress
    hard_exit: HardExit
    read_registration_data: ReadRegistrationData
    write_registration_data: WriteRegistrationData
    get_product_information: GetProductInformation
    log: Log
    upgrades_available: UpgradesAvailable
    downgrade_available: DowngradeAvailable
    download_progress: DownloadProgress
    alerts: Alerts
    show_expiration_dialog: ShowExpirationDialog
    read_old_token: ReadOldToken
    token: Token
    verification_complete: VerificationComplete
    def __init__(self, set_watermark: _Optional[_Union[SetWatermark, _Mapping]] = ..., deactivation_complete: _Optional[_Union[DeactivationComplete, _Mapping]] = ..., free_bibles: _Optional[_Union[FreeBibles, _Mapping]] = ..., purchased_bibles: _Optional[_Union[PurchasedBibles, _Mapping]] = ..., bible_activation_complete: _Optional[_Union[BibleActivationComplete, _Mapping]] = ..., bible_deactivation_complete: _Optional[_Union[BibleDeactivationComplete, _Mapping]] = ..., bible_download_progress: _Optional[_Union[BibleDownloadProgress, _Mapping]] = ..., hard_exit: _Optional[_Union[HardExit, _Mapping]] = ..., read_registration_data: _Optional[_Union[ReadRegistrationData, _Mapping]] = ..., write_registration_data: _Optional[_Union[WriteRegistrationData, _Mapping]] = ..., get_product_information: _Optional[_Union[GetProductInformation, _Mapping]] = ..., log: _Optional[_Union[Log, _Mapping]] = ..., upgrades_available: _Optional[_Union[UpgradesAvailable, _Mapping]] = ..., downgrade_available: _Optional[_Union[DowngradeAvailable, _Mapping]] = ..., download_progress: _Optional[_Union[DownloadProgress, _Mapping]] = ..., alerts: _Optional[_Union[Alerts, _Mapping]] = ..., show_expiration_dialog: _Optional[_Union[ShowExpirationDialog, _Mapping]] = ..., read_old_token: _Optional[_Union[ReadOldToken, _Mapping]] = ..., token: _Optional[_Union[Token, _Mapping]] = ..., verification_complete: _Optional[_Union[VerificationComplete, _Mapping]] = ...) -> None: ...

class Register(_message.Message):
    __slots__ = ("user_name", "registration_key", "display_name", "seat_type", "channel")
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    REGISTRATION_KEY_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    SEAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    user_name: str
    registration_key: str
    display_name: str
    seat_type: SeatType
    channel: UpdateChannel
    def __init__(self, user_name: _Optional[str] = ..., registration_key: _Optional[str] = ..., display_name: _Optional[str] = ..., seat_type: _Optional[_Union[SeatType, str]] = ..., channel: _Optional[_Union[UpdateChannel, str]] = ...) -> None: ...

class ActivateLink(_message.Message):
    __slots__ = ("identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    def __init__(self, identifier: _Optional[str] = ...) -> None: ...

class Unregister(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ChangeSeatType(_message.Message):
    __slots__ = ("seat_type", "channel")
    SEAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    seat_type: SeatType
    channel: UpdateChannel
    def __init__(self, seat_type: _Optional[_Union[SeatType, str]] = ..., channel: _Optional[_Union[UpdateChannel, str]] = ...) -> None: ...

class GetFreeBibles(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetPurchasedBibles(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ActivateBible(_message.Message):
    __slots__ = ("bible_id",)
    BIBLE_ID_FIELD_NUMBER: _ClassVar[int]
    bible_id: str
    def __init__(self, bible_id: _Optional[str] = ...) -> None: ...

class DeactivateBible(_message.Message):
    __slots__ = ("bible_id",)
    BIBLE_ID_FIELD_NUMBER: _ClassVar[int]
    bible_id: str
    def __init__(self, bible_id: _Optional[str] = ...) -> None: ...

class DownloadBible(_message.Message):
    __slots__ = ("bible_id", "filename")
    BIBLE_ID_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    bible_id: str
    filename: str
    def __init__(self, bible_id: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class RegistrationData(_message.Message):
    __slots__ = ("data", "channel")
    DATA_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    channel: UpdateChannel
    def __init__(self, data: _Optional[bytes] = ..., channel: _Optional[_Union[UpdateChannel, str]] = ...) -> None: ...

class ProductInformation(_message.Message):
    __slots__ = ("product_name", "major_version", "minor_version", "patch_version", "build_number", "build_date")
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    MAJOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    MINOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    PATCH_VERSION_FIELD_NUMBER: _ClassVar[int]
    BUILD_NUMBER_FIELD_NUMBER: _ClassVar[int]
    BUILD_DATE_FIELD_NUMBER: _ClassVar[int]
    product_name: str
    major_version: str
    minor_version: str
    patch_version: str
    build_number: str
    build_date: int
    def __init__(self, product_name: _Optional[str] = ..., major_version: _Optional[str] = ..., minor_version: _Optional[str] = ..., patch_version: _Optional[str] = ..., build_number: _Optional[str] = ..., build_date: _Optional[int] = ...) -> None: ...

class GetAvailableVersion(_message.Message):
    __slots__ = ("include_notes", "channel", "format")
    INCLUDE_NOTES_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    include_notes: bool
    channel: str
    format: str
    def __init__(self, include_notes: bool = ..., channel: _Optional[str] = ..., format: _Optional[str] = ...) -> None: ...

class DownloadNewVersion(_message.Message):
    __slots__ = ("url", "filename")
    URL_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    url: str
    filename: str
    def __init__(self, url: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class Refresh(_message.Message):
    __slots__ = ("channel",)
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    channel: UpdateChannel
    def __init__(self, channel: _Optional[_Union[UpdateChannel, str]] = ...) -> None: ...

class UpdateToken(_message.Message):
    __slots__ = ("token_metadata",)
    TOKEN_METADATA_FIELD_NUMBER: _ClassVar[int]
    token_metadata: TokenMetadata
    def __init__(self, token_metadata: _Optional[_Union[TokenMetadata, _Mapping]] = ...) -> None: ...

class OldTokenData(_message.Message):
    __slots__ = ("status", "token")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    status: ReadTokenStatus
    token: TokenMetadata
    def __init__(self, status: _Optional[_Union[ReadTokenStatus, str]] = ..., token: _Optional[_Union[TokenMetadata, _Mapping]] = ...) -> None: ...

class Token(_message.Message):
    __slots__ = ("token_metadata",)
    TOKEN_METADATA_FIELD_NUMBER: _ClassVar[int]
    token_metadata: TokenMetadata
    def __init__(self, token_metadata: _Optional[_Union[TokenMetadata, _Mapping]] = ...) -> None: ...

class SetWatermark(_message.Message):
    __slots__ = ("is_registered", "active_seat")
    IS_REGISTERED_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_SEAT_FIELD_NUMBER: _ClassVar[int]
    is_registered: bool
    active_seat: bool
    def __init__(self, is_registered: bool = ..., active_seat: bool = ...) -> None: ...

class ActivationComplete(_message.Message):
    __slots__ = ("result", "registration_info", "available_seats", "total_seats")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REGISTRATION_INFO_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_SEATS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SEATS_FIELD_NUMBER: _ClassVar[int]
    result: Status
    registration_info: RegistrationInfo
    available_seats: Seats
    total_seats: Seats
    def __init__(self, result: _Optional[_Union[Status, str]] = ..., registration_info: _Optional[_Union[RegistrationInfo, _Mapping]] = ..., available_seats: _Optional[_Union[Seats, _Mapping]] = ..., total_seats: _Optional[_Union[Seats, _Mapping]] = ...) -> None: ...

class DeactivationComplete(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Status
    def __init__(self, result: _Optional[_Union[Status, str]] = ...) -> None: ...

class ChangeSeatTypeComplete(_message.Message):
    __slots__ = ("result", "available_seats", "total_seats", "seat_type")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_SEATS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SEATS_FIELD_NUMBER: _ClassVar[int]
    SEAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    result: Status
    available_seats: Seats
    total_seats: Seats
    seat_type: SeatType
    def __init__(self, result: _Optional[_Union[Status, str]] = ..., available_seats: _Optional[_Union[Seats, _Mapping]] = ..., total_seats: _Optional[_Union[Seats, _Mapping]] = ..., seat_type: _Optional[_Union[SeatType, str]] = ...) -> None: ...

class FreeBibles(_message.Message):
    __slots__ = ("status", "bibles")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BIBLES_FIELD_NUMBER: _ClassVar[int]
    status: Status
    bibles: _containers.RepeatedCompositeFieldContainer[Bible]
    def __init__(self, status: _Optional[_Union[Status, str]] = ..., bibles: _Optional[_Iterable[_Union[Bible, _Mapping]]] = ...) -> None: ...

class PurchasedBibles(_message.Message):
    __slots__ = ("status", "bibles")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BIBLES_FIELD_NUMBER: _ClassVar[int]
    status: Status
    bibles: _containers.RepeatedCompositeFieldContainer[PurchasedBible]
    def __init__(self, status: _Optional[_Union[Status, str]] = ..., bibles: _Optional[_Iterable[_Union[PurchasedBible, _Mapping]]] = ...) -> None: ...

class BibleActivationComplete(_message.Message):
    __slots__ = ("status", "bible_id", "download_link", "bibles")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BIBLE_ID_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_LINK_FIELD_NUMBER: _ClassVar[int]
    BIBLES_FIELD_NUMBER: _ClassVar[int]
    status: Status
    bible_id: str
    download_link: str
    bibles: _containers.RepeatedCompositeFieldContainer[PurchasedBible]
    def __init__(self, status: _Optional[_Union[Status, str]] = ..., bible_id: _Optional[str] = ..., download_link: _Optional[str] = ..., bibles: _Optional[_Iterable[_Union[PurchasedBible, _Mapping]]] = ...) -> None: ...

class BibleDeactivationComplete(_message.Message):
    __slots__ = ("status", "bible_id", "bibles")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BIBLE_ID_FIELD_NUMBER: _ClassVar[int]
    BIBLES_FIELD_NUMBER: _ClassVar[int]
    status: Status
    bible_id: str
    bibles: _containers.RepeatedCompositeFieldContainer[PurchasedBible]
    def __init__(self, status: _Optional[_Union[Status, str]] = ..., bible_id: _Optional[str] = ..., bibles: _Optional[_Iterable[_Union[PurchasedBible, _Mapping]]] = ...) -> None: ...

class BibleDownloadProgress(_message.Message):
    __slots__ = ("status", "complete", "progress", "bible_id", "file_name", "download_link")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COMPLETE_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    BIBLE_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_LINK_FIELD_NUMBER: _ClassVar[int]
    status: Status
    complete: bool
    progress: float
    bible_id: str
    file_name: str
    download_link: str
    def __init__(self, status: _Optional[_Union[Status, str]] = ..., complete: bool = ..., progress: _Optional[float] = ..., bible_id: _Optional[str] = ..., file_name: _Optional[str] = ..., download_link: _Optional[str] = ...) -> None: ...

class HardExit(_message.Message):
    __slots__ = ("reason",)
    class Reason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        HostsFile: _ClassVar[HardExit.Reason]
        SystemTime: _ClassVar[HardExit.Reason]
    HostsFile: HardExit.Reason
    SystemTime: HardExit.Reason
    REASON_FIELD_NUMBER: _ClassVar[int]
    reason: HardExit.Reason
    def __init__(self, reason: _Optional[_Union[HardExit.Reason, str]] = ...) -> None: ...

class ReadRegistrationData(_message.Message):
    __slots__ = ("fingerprint", "identifier")
    FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    fingerprint: str
    identifier: str
    def __init__(self, fingerprint: _Optional[str] = ..., identifier: _Optional[str] = ...) -> None: ...

class ReadOldToken(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WriteRegistrationData(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class GetProductInformation(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Log(_message.Message):
    __slots__ = ("level", "message")
    class Level(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Debug: _ClassVar[Log.Level]
        Info: _ClassVar[Log.Level]
        Warning: _ClassVar[Log.Level]
        Error: _ClassVar[Log.Level]
    Debug: Log.Level
    Info: Log.Level
    Warning: Log.Level
    Error: Log.Level
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    level: Log.Level
    message: str
    def __init__(self, level: _Optional[_Union[Log.Level, str]] = ..., message: _Optional[str] = ...) -> None: ...

class UpgradesAvailable(_message.Message):
    __slots__ = ("status", "is_non_production_active", "active_channel", "release_notes", "upgrades")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    IS_NON_PRODUCTION_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    RELEASE_NOTES_FIELD_NUMBER: _ClassVar[int]
    UPGRADES_FIELD_NUMBER: _ClassVar[int]
    status: Status
    is_non_production_active: bool
    active_channel: str
    release_notes: str
    upgrades: _containers.RepeatedCompositeFieldContainer[BuildInformation]
    def __init__(self, status: _Optional[_Union[Status, str]] = ..., is_non_production_active: bool = ..., active_channel: _Optional[str] = ..., release_notes: _Optional[str] = ..., upgrades: _Optional[_Iterable[_Union[BuildInformation, _Mapping]]] = ...) -> None: ...

class DowngradeAvailable(_message.Message):
    __slots__ = ("status", "downgrade", "release_notes")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DOWNGRADE_FIELD_NUMBER: _ClassVar[int]
    RELEASE_NOTES_FIELD_NUMBER: _ClassVar[int]
    status: Status
    downgrade: BuildInformation
    release_notes: str
    def __init__(self, status: _Optional[_Union[Status, str]] = ..., downgrade: _Optional[_Union[BuildInformation, _Mapping]] = ..., release_notes: _Optional[str] = ...) -> None: ...

class DownloadProgress(_message.Message):
    __slots__ = ("status", "complete", "progress")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COMPLETE_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    status: Status
    complete: bool
    progress: float
    def __init__(self, status: _Optional[_Union[Status, str]] = ..., complete: bool = ..., progress: _Optional[float] = ...) -> None: ...

class Alerts(_message.Message):
    __slots__ = ("alerts",)
    ALERTS_FIELD_NUMBER: _ClassVar[int]
    alerts: _containers.RepeatedCompositeFieldContainer[Alert]
    def __init__(self, alerts: _Optional[_Iterable[_Union[Alert, _Mapping]]] = ...) -> None: ...

class ShowExpirationDialog(_message.Message):
    __slots__ = ("days",)
    DAYS_FIELD_NUMBER: _ClassVar[int]
    days: int
    def __init__(self, days: _Optional[int] = ...) -> None: ...

class LicenseInfo(_message.Message):
    __slots__ = ("registration_info", "available_seats", "total_seats", "legacy")
    REGISTRATION_INFO_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_SEATS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SEATS_FIELD_NUMBER: _ClassVar[int]
    LEGACY_FIELD_NUMBER: _ClassVar[int]
    registration_info: RegistrationInfo
    available_seats: Seats
    total_seats: Seats
    legacy: bool
    def __init__(self, registration_info: _Optional[_Union[RegistrationInfo, _Mapping]] = ..., available_seats: _Optional[_Union[Seats, _Mapping]] = ..., total_seats: _Optional[_Union[Seats, _Mapping]] = ..., legacy: bool = ...) -> None: ...

class VerificationComplete(_message.Message):
    __slots__ = ("result", "license", "bibles", "token", "subscription_info", "alert", "banner")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    LICENSE_FIELD_NUMBER: _ClassVar[int]
    BIBLES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_INFO_FIELD_NUMBER: _ClassVar[int]
    ALERT_FIELD_NUMBER: _ClassVar[int]
    BANNER_FIELD_NUMBER: _ClassVar[int]
    result: Status
    license: LicenseInfo
    bibles: Bibles
    token: TokenMetadata
    subscription_info: SubscriptionInfo
    alert: PopupAlertMessage
    banner: BannerMessage
    def __init__(self, result: _Optional[_Union[Status, str]] = ..., license: _Optional[_Union[LicenseInfo, _Mapping]] = ..., bibles: _Optional[_Union[Bibles, _Mapping]] = ..., token: _Optional[_Union[TokenMetadata, _Mapping]] = ..., subscription_info: _Optional[_Union[SubscriptionInfo, _Mapping]] = ..., alert: _Optional[_Union[PopupAlertMessage, str]] = ..., banner: _Optional[_Union[BannerMessage, str]] = ...) -> None: ...

class Seats(_message.Message):
    __slots__ = ("basic", "advanced")
    BASIC_FIELD_NUMBER: _ClassVar[int]
    ADVANCED_FIELD_NUMBER: _ClassVar[int]
    basic: int
    advanced: int
    def __init__(self, basic: _Optional[int] = ..., advanced: _Optional[int] = ...) -> None: ...

class SupplementalInformation(_message.Message):
    __slots__ = ("download_link",)
    DOWNLOAD_LINK_FIELD_NUMBER: _ClassVar[int]
    download_link: str
    def __init__(self, download_link: _Optional[str] = ...) -> None: ...

class Bible(_message.Message):
    __slots__ = ("id", "name", "language", "publisher", "copyright", "display_abbreviation", "internal_abbreviation", "version", "info")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    PUBLISHER_FIELD_NUMBER: _ClassVar[int]
    COPYRIGHT_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_ABBREVIATION_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_ABBREVIATION_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    language: str
    publisher: str
    copyright: str
    display_abbreviation: str
    internal_abbreviation: str
    version: str
    info: SupplementalInformation
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., language: _Optional[str] = ..., publisher: _Optional[str] = ..., copyright: _Optional[str] = ..., display_abbreviation: _Optional[str] = ..., internal_abbreviation: _Optional[str] = ..., version: _Optional[str] = ..., info: _Optional[_Union[SupplementalInformation, _Mapping]] = ...) -> None: ...

class PurchasedBible(_message.Message):
    __slots__ = ("metadata", "licensing_info")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    LICENSING_INFO_FIELD_NUMBER: _ClassVar[int]
    metadata: Bible
    licensing_info: LicensingInfo
    def __init__(self, metadata: _Optional[_Union[Bible, _Mapping]] = ..., licensing_info: _Optional[_Union[LicensingInfo, _Mapping]] = ...) -> None: ...

class LicensingInfo(_message.Message):
    __slots__ = ("available_copies", "total_copies", "is_active_locally", "other_active_copies")
    AVAILABLE_COPIES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COPIES_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_LOCALLY_FIELD_NUMBER: _ClassVar[int]
    OTHER_ACTIVE_COPIES_FIELD_NUMBER: _ClassVar[int]
    available_copies: int
    total_copies: int
    is_active_locally: bool
    other_active_copies: _containers.RepeatedCompositeFieldContainer[ActiveCopy]
    def __init__(self, available_copies: _Optional[int] = ..., total_copies: _Optional[int] = ..., is_active_locally: bool = ..., other_active_copies: _Optional[_Iterable[_Union[ActiveCopy, _Mapping]]] = ...) -> None: ...

class ActiveCopy(_message.Message):
    __slots__ = ("display_name", "hostname")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    hostname: str
    def __init__(self, display_name: _Optional[str] = ..., hostname: _Optional[str] = ...) -> None: ...

class RegistrationInfo(_message.Message):
    __slots__ = ("user_name", "display_key", "display_name", "expiration_date", "activation_key", "license_type", "registration_date", "seat_type", "latest_available_build_number", "latest_available_version", "has_worship_house_media_subscription", "maintenance_expiration_date", "non_extended_maintenance_expiration_date", "is_auto_renewal_active")
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_KEY_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_DATE_FIELD_NUMBER: _ClassVar[int]
    ACTIVATION_KEY_FIELD_NUMBER: _ClassVar[int]
    LICENSE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REGISTRATION_DATE_FIELD_NUMBER: _ClassVar[int]
    SEAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    LATEST_AVAILABLE_BUILD_NUMBER_FIELD_NUMBER: _ClassVar[int]
    LATEST_AVAILABLE_VERSION_FIELD_NUMBER: _ClassVar[int]
    HAS_WORSHIP_HOUSE_MEDIA_SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_EXPIRATION_DATE_FIELD_NUMBER: _ClassVar[int]
    NON_EXTENDED_MAINTENANCE_EXPIRATION_DATE_FIELD_NUMBER: _ClassVar[int]
    IS_AUTO_RENEWAL_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    user_name: str
    display_key: str
    display_name: str
    expiration_date: int
    activation_key: str
    license_type: LicenseType
    registration_date: int
    seat_type: SeatType
    latest_available_build_number: int
    latest_available_version: str
    has_worship_house_media_subscription: bool
    maintenance_expiration_date: int
    non_extended_maintenance_expiration_date: int
    is_auto_renewal_active: bool
    def __init__(self, user_name: _Optional[str] = ..., display_key: _Optional[str] = ..., display_name: _Optional[str] = ..., expiration_date: _Optional[int] = ..., activation_key: _Optional[str] = ..., license_type: _Optional[_Union[LicenseType, str]] = ..., registration_date: _Optional[int] = ..., seat_type: _Optional[_Union[SeatType, str]] = ..., latest_available_build_number: _Optional[int] = ..., latest_available_version: _Optional[str] = ..., has_worship_house_media_subscription: bool = ..., maintenance_expiration_date: _Optional[int] = ..., non_extended_maintenance_expiration_date: _Optional[int] = ..., is_auto_renewal_active: bool = ...) -> None: ...

class BuildInformation(_message.Message):
    __slots__ = ("build_number", "version", "min_os_version", "release_date", "registration_date", "download_size", "download_url", "channel", "is_beta", "is_available")
    BUILD_NUMBER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    MIN_OS_VERSION_FIELD_NUMBER: _ClassVar[int]
    RELEASE_DATE_FIELD_NUMBER: _ClassVar[int]
    REGISTRATION_DATE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_SIZE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    IS_BETA_FIELD_NUMBER: _ClassVar[int]
    IS_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    build_number: int
    version: str
    min_os_version: str
    release_date: int
    registration_date: int
    download_size: int
    download_url: str
    channel: str
    is_beta: bool
    is_available: bool
    def __init__(self, build_number: _Optional[int] = ..., version: _Optional[str] = ..., min_os_version: _Optional[str] = ..., release_date: _Optional[int] = ..., registration_date: _Optional[int] = ..., download_size: _Optional[int] = ..., download_url: _Optional[str] = ..., channel: _Optional[str] = ..., is_beta: bool = ..., is_available: bool = ...) -> None: ...

class Alert(_message.Message):
    __slots__ = ("alert_type", "title", "content_type", "content")
    ALERT_TYPE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    alert_type: AlertType
    title: str
    content_type: AlertContentType
    content: str
    def __init__(self, alert_type: _Optional[_Union[AlertType, str]] = ..., title: _Optional[str] = ..., content_type: _Optional[_Union[AlertContentType, str]] = ..., content: _Optional[str] = ...) -> None: ...

class TokenMetadata(_message.Message):
    __slots__ = ("access_token", "refresh_token", "expires_at")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    refresh_token: str
    expires_at: int
    def __init__(self, access_token: _Optional[str] = ..., refresh_token: _Optional[str] = ..., expires_at: _Optional[int] = ...) -> None: ...

class SubscriptionInfo(_message.Message):
    __slots__ = ("organization_name", "procontent_license_type", "procontent_license_expiration")
    ORGANIZATION_NAME_FIELD_NUMBER: _ClassVar[int]
    PROCONTENT_LICENSE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROCONTENT_LICENSE_EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    organization_name: str
    procontent_license_type: ProContentLicenseType
    procontent_license_expiration: int
    def __init__(self, organization_name: _Optional[str] = ..., procontent_license_type: _Optional[_Union[ProContentLicenseType, str]] = ..., procontent_license_expiration: _Optional[int] = ...) -> None: ...

class DownloadLink(_message.Message):
    __slots__ = ("id", "url")
    ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    id: str
    url: str
    def __init__(self, id: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class Bibles(_message.Message):
    __slots__ = ("free_bibles", "purchased_bibles")
    FREE_BIBLES_FIELD_NUMBER: _ClassVar[int]
    PURCHASED_BIBLES_FIELD_NUMBER: _ClassVar[int]
    free_bibles: _containers.RepeatedCompositeFieldContainer[Bible]
    purchased_bibles: _containers.RepeatedCompositeFieldContainer[PurchasedBible]
    def __init__(self, free_bibles: _Optional[_Iterable[_Union[Bible, _Mapping]]] = ..., purchased_bibles: _Optional[_Iterable[_Union[PurchasedBible, _Mapping]]] = ...) -> None: ...

class FeatureFlags(_message.Message):
    __slots__ = ("use_staging", "use_subscription")
    USE_STAGING_FIELD_NUMBER: _ClassVar[int]
    USE_SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    use_staging: bool
    use_subscription: bool
    def __init__(self, use_staging: bool = ..., use_subscription: bool = ...) -> None: ...

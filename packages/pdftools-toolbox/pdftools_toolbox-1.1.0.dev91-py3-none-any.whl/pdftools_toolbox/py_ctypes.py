from ctypes import *
from enum import Enum
from enum import Flag
from enum import IntEnum
try:
    # When using as package
    from .streams import *
    from .utils import *
except ImportError:
    # When using locally
    from streams import *
    from utils import *

# Load library
_lib = load_library()

# ErrorCode type definition
class ErrorCode(IntEnum):
    SUCCESS = 0
    GENERIC = 10
    LICENSE = 12
    UNKNOWN_FORMAT = 15
    CORRUPT = 16
    PASSWORD = 17
    CONFORMANCE = 18
    UNSUPPORTED_FEATURE = 19
    EXISTS = 22
    HTTP = 24
    UNSUPPORTED_OPERATION = 1
    ILLEGAL_STATE = 2
    ILLEGAL_ARGUMENT = 3
    NOT_FOUND = 5
    I_O = 4


# Enumerations type definitions

class GeomHorizontalAlignment(IntEnum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2


class GeomRotation(IntEnum):
    NONE = 0
    CLOCKWISE = 90
    UPSIDE_DOWN = 180
    COUNTER_CLOCKWISE = 270


class PdfPermission(Flag):
    NONE = 0
    PRINT = 4
    MODIFY = 8
    COPY = 16
    ANNOTATE = 32
    FILL_FORMS = 256
    SUPPORT_DISABILITIES = 512
    ASSEMBLE = 1024
    DIGITAL_PRINT = 2048

    ALL = 3900

class PdfConformance(IntEnum):
    PDF10 = 0x1000
    PDF11 = 0x1100
    PDF12 = 0x1200
    PDF13 = 0x1300
    PDF14 = 0x1400
    PDF15 = 0x1500
    PDF16 = 0x1600
    PDF17 = 0x1700
    PDF20 = 0x2000
    PDF_A1_B = 0x1401
    PDF_A1_A = 0x1402
    PDF_A2_B = 0x1701
    PDF_A2_U = 0x1702
    PDF_A2_A = 0x1703
    PDF_A3_B = 0x1711
    PDF_A3_U = 0x1712
    PDF_A3_A = 0x1713


class PdfCopyStrategy(IntEnum):
    COPY = 1
    FLATTEN = 2
    REMOVE = 3


class PdfRemovalStrategy(IntEnum):
    FLATTEN = 2
    REMOVE = 3


class PdfNameConflictResolution(IntEnum):
    MERGE = 1
    RENAME = 2


class PdfContentProcessColorSpaceType(IntEnum):
    GRAY = 1
    RGB = 2
    CMYK = 3


class PdfContentLineCapStyle(IntEnum):
    BUTT = 0
    ROUND = 1
    SQUARE = 2


class PdfContentLineJoinStyle(IntEnum):
    MITER = 0
    ROUND = 1
    BEVEL = 2


class PdfContentInsideRule(IntEnum):
    NONZERO_WINDING_NUMBER = 0
    EVEN_ODD = 1


class PdfContentBlendMode(IntEnum):
    NORMAL = 0
    MULTIPLY = 1
    SCREEN = 2
    DARKEN = 4
    LIGHTEN = 5
    COLOR_DODGE = 6
    COLOR_BURN = 7
    HARD_LIGHT = 8
    SOFT_LIGHT = 9
    OVERLAY = 3
    DIFFERENCE = 10
    EXCLUSION = 11
    HUE = 12
    SATURATION = 13
    COLOR = 14
    LUMINOSITY = 15


class PdfContentUngroupingSelection(IntEnum):
    NONE = 0
    SAFELY_UNGROUPABLE = 1
    ALL = 2


class PdfContentWritingMode(IntEnum):
    HORIZONTAL = 0
    VERTICAL = 1


class PdfContentFontWeight(IntEnum):
    THIN = 100
    EXTRA_LIGHT = 200
    LIGHT = 300
    NORMAL = 400
    MEDIUM = 500
    SEMI_BOLD = 600
    BOLD = 700
    EXTRA_BOLD = 800
    BLACK = 900


class PdfContentPathSegmentType(IntEnum):
    LINEAR = 0
    CUBIC = 1


class PdfContentImageType(IntEnum):
    BMP = 0
    JPEG = 1
    JPEG2000 = 2
    JBIG2 = 3
    PNG = 4
    GIF = 5
    TIFF = 6


class PdfFormsFormFieldCopyStrategy(IntEnum):
    COPY = 1
    FLATTEN = 2
    REMOVE = 3
    COPY_AND_UPDATE_WIDGETS = 4


class PdfFormsMdpPermissions(IntEnum):
    NO_CHANGES = 1
    FORM_FILLING = 2
    ANNOTATE = 3


class PdfNavViewerNavigationPane(IntEnum):
    NONE = 0
    OUTLINES = 1
    THUMBNAILS = 2
    LAYERS = 3
    EMBEDDED_FILES = 4


class PdfNavPageLayout(IntEnum):
    ONE_PAGE = 0
    TWO_PAGE = 1
    TWO_PAGE_FIRST_PAGE_SINGLE = 2


class PdfNavNamedDestinationCopyStrategy(IntEnum):
    COPY = 1
    RESOLVE = 2


class PdfAnnotsLineEnding(IntEnum):
    NONE = 0
    OPEN_ARROW = 1
    CLOSED_ARROW = 2
    SQUARE = 3
    CIRCLE = 4
    DIAMOND = 5
    BUTT = 6
    OPEN_ARROW_TAIL = 7
    CLOSED_ARROW_TAIL = 8
    SLASH = 9


class PdfAnnotsTextStampType(IntEnum):
    APPROVED = 0
    EXPERIMENTAL = 1
    NOT_APPROVED = 2
    AS_IS = 3
    EXPIRED = 4
    NOT_FOR_PUBLIC_RELEASE = 5
    CONFIDENTIAL = 6
    FINAL = 7
    SOLD = 8
    DEPARTMENTAL = 9
    FOR_COMMENT = 10
    TOP_SECRET = 11
    DRAFT = 12
    FOR_PUBLIC_RELEASE = 13
    CUSTOM_STAMP_TEXT = 127


class PdfAnnotsFileAttachmentIcon(IntEnum):
    GRAPH = 0
    PUSH_PIN = 1
    PAPERCLIP = 2
    TAG = 3
    CUSTOM_ICON = 127



# Derived types enumerations
class PdfContentColorSpaceType(IntEnum):
    PDF_CONTENT_COLOR_SPACE = 1
    PDF_CONTENT_DEVICE_GRAY_COLOR_SPACE = 2
    PDF_CONTENT_DEVICE_RGB_COLOR_SPACE = 3
    PDF_CONTENT_DEVICE_CMYK_COLOR_SPACE = 4
    PDF_CONTENT_CALIBRATED_GRAY_COLOR_SPACE = 5
    PDF_CONTENT_CALIBRATED_RGB_COLOR_SPACE = 6
    PDF_CONTENT_LAB_COLOR_SPACE = 7
    PDF_CONTENT_ICC_BASED_COLOR_SPACE = 8
    PDF_CONTENT_INDEXED_COLOR_SPACE = 9
    PDF_CONTENT_SEPARATION_COLOR_SPACE = 10
    PDF_CONTENT_N_CHANNEL_COLOR_SPACE = 11

class PdfContentContentElementType(IntEnum):
    PDF_CONTENT_CONTENT_ELEMENT = 1
    PDF_CONTENT_TEXT_ELEMENT = 2
    PDF_CONTENT_GROUP_ELEMENT = 3
    PDF_CONTENT_PATH_ELEMENT = 4
    PDF_CONTENT_IMAGE_ELEMENT = 5
    PDF_CONTENT_IMAGE_MASK_ELEMENT = 6
    PDF_CONTENT_SHADING_ELEMENT = 7

class PdfFormsFieldNodeType(IntEnum):
    PDF_FORMS_FIELD_NODE = 1
    PDF_FORMS_SUB_FORM = 2
    PDF_FORMS_FIELD = 3
    PDF_FORMS_TEXT_FIELD = 4
    PDF_FORMS_GENERAL_TEXT_FIELD = 5
    PDF_FORMS_COMB_TEXT_FIELD = 6
    PDF_FORMS_PUSH_BUTTON = 7
    PDF_FORMS_CHECK_BOX = 8
    PDF_FORMS_RADIO_BUTTON_GROUP = 9
    PDF_FORMS_CHOICE_FIELD = 10
    PDF_FORMS_LIST_BOX = 11
    PDF_FORMS_COMBO_BOX = 12

class PdfFormsFieldType(IntEnum):
    PDF_FORMS_FIELD = 1
    PDF_FORMS_TEXT_FIELD = 2
    PDF_FORMS_GENERAL_TEXT_FIELD = 3
    PDF_FORMS_COMB_TEXT_FIELD = 4
    PDF_FORMS_PUSH_BUTTON = 5
    PDF_FORMS_CHECK_BOX = 6
    PDF_FORMS_RADIO_BUTTON_GROUP = 7
    PDF_FORMS_CHOICE_FIELD = 8
    PDF_FORMS_LIST_BOX = 9
    PDF_FORMS_COMBO_BOX = 10

class PdfFormsTextFieldType(IntEnum):
    PDF_FORMS_TEXT_FIELD = 1
    PDF_FORMS_GENERAL_TEXT_FIELD = 2
    PDF_FORMS_COMB_TEXT_FIELD = 3

class PdfFormsChoiceFieldType(IntEnum):
    PDF_FORMS_CHOICE_FIELD = 1
    PDF_FORMS_LIST_BOX = 2
    PDF_FORMS_COMBO_BOX = 3

class PdfFormsSignatureFieldType(IntEnum):
    PDF_FORMS_SIGNATURE_FIELD = 1
    PDF_FORMS_SIGNED_SIGNATURE_FIELD = 2
    PDF_FORMS_SIGNATURE = 3
    PDF_FORMS_DOCUMENT_SIGNATURE = 4
    PDF_FORMS_DOC_MDP_SIGNATURE = 5
    PDF_FORMS_DOCUMENT_TIME_STAMP = 6

class PdfFormsSignedSignatureFieldType(IntEnum):
    PDF_FORMS_SIGNED_SIGNATURE_FIELD = 1
    PDF_FORMS_SIGNATURE = 2
    PDF_FORMS_DOCUMENT_SIGNATURE = 3
    PDF_FORMS_DOC_MDP_SIGNATURE = 4
    PDF_FORMS_DOCUMENT_TIME_STAMP = 5

class PdfFormsSignatureType(IntEnum):
    PDF_FORMS_SIGNATURE = 1
    PDF_FORMS_DOCUMENT_SIGNATURE = 2
    PDF_FORMS_DOC_MDP_SIGNATURE = 3

class PdfNavDestinationType(IntEnum):
    PDF_NAV_DESTINATION = 1
    PDF_NAV_NAMED_DESTINATION = 2
    PDF_NAV_DIRECT_DESTINATION = 3
    PDF_NAV_LOCATION_ZOOM_DESTINATION = 4
    PDF_NAV_FIT_PAGE_DESTINATION = 5
    PDF_NAV_FIT_WIDTH_DESTINATION = 6
    PDF_NAV_FIT_HEIGHT_DESTINATION = 7
    PDF_NAV_FIT_RECTANGLE_DESTINATION = 8

class PdfNavDirectDestinationType(IntEnum):
    PDF_NAV_DIRECT_DESTINATION = 1
    PDF_NAV_LOCATION_ZOOM_DESTINATION = 2
    PDF_NAV_FIT_PAGE_DESTINATION = 3
    PDF_NAV_FIT_WIDTH_DESTINATION = 4
    PDF_NAV_FIT_HEIGHT_DESTINATION = 5
    PDF_NAV_FIT_RECTANGLE_DESTINATION = 6

class PdfNavLinkType(IntEnum):
    PDF_NAV_LINK = 1
    PDF_NAV_INTERNAL_LINK = 2
    PDF_NAV_WEB_LINK = 3
    PDF_NAV_EMBEDDED_PDF_LINK = 4

class PdfAnnotsAnnotationType(IntEnum):
    PDF_ANNOTS_ANNOTATION = 1
    PDF_ANNOTS_MARKUP_ANNOTATION = 2
    PDF_ANNOTS_STICKY_NOTE = 3
    PDF_ANNOTS_FILE_ATTACHMENT = 4
    PDF_ANNOTS_STAMP = 5
    PDF_ANNOTS_TEXT_STAMP = 6
    PDF_ANNOTS_CUSTOM_STAMP = 7
    PDF_ANNOTS_FREE_TEXT = 8
    PDF_ANNOTS_DRAWING_ANNOTATION = 9
    PDF_ANNOTS_LINE_ANNOTATION = 10
    PDF_ANNOTS_INK_ANNOTATION = 11
    PDF_ANNOTS_POLY_LINE_ANNOTATION = 12
    PDF_ANNOTS_POLYGON_ANNOTATION = 13
    PDF_ANNOTS_RECTANGLE_ANNOTATION = 14
    PDF_ANNOTS_ELLIPSE_ANNOTATION = 15
    PDF_ANNOTS_TEXT_MARKUP = 16
    PDF_ANNOTS_HIGHLIGHT = 17
    PDF_ANNOTS_UNDERLINE = 18
    PDF_ANNOTS_STRIKE_THROUGH = 19
    PDF_ANNOTS_SQUIGGLY = 20
    PDF_ANNOTS_TEXT_INSERT = 21

class PdfAnnotsMarkupAnnotationType(IntEnum):
    PDF_ANNOTS_MARKUP_ANNOTATION = 1
    PDF_ANNOTS_STICKY_NOTE = 2
    PDF_ANNOTS_FILE_ATTACHMENT = 3
    PDF_ANNOTS_STAMP = 4
    PDF_ANNOTS_TEXT_STAMP = 5
    PDF_ANNOTS_CUSTOM_STAMP = 6
    PDF_ANNOTS_FREE_TEXT = 7
    PDF_ANNOTS_DRAWING_ANNOTATION = 8
    PDF_ANNOTS_LINE_ANNOTATION = 9
    PDF_ANNOTS_INK_ANNOTATION = 10
    PDF_ANNOTS_POLY_LINE_ANNOTATION = 11
    PDF_ANNOTS_POLYGON_ANNOTATION = 12
    PDF_ANNOTS_RECTANGLE_ANNOTATION = 13
    PDF_ANNOTS_ELLIPSE_ANNOTATION = 14
    PDF_ANNOTS_TEXT_MARKUP = 15
    PDF_ANNOTS_HIGHLIGHT = 16
    PDF_ANNOTS_UNDERLINE = 17
    PDF_ANNOTS_STRIKE_THROUGH = 18
    PDF_ANNOTS_SQUIGGLY = 19
    PDF_ANNOTS_TEXT_INSERT = 20

class PdfAnnotsStampType(IntEnum):
    PDF_ANNOTS_STAMP = 1
    PDF_ANNOTS_TEXT_STAMP = 2
    PDF_ANNOTS_CUSTOM_STAMP = 3

class PdfAnnotsDrawingAnnotationType(IntEnum):
    PDF_ANNOTS_DRAWING_ANNOTATION = 1
    PDF_ANNOTS_LINE_ANNOTATION = 2
    PDF_ANNOTS_INK_ANNOTATION = 3
    PDF_ANNOTS_POLY_LINE_ANNOTATION = 4
    PDF_ANNOTS_POLYGON_ANNOTATION = 5
    PDF_ANNOTS_RECTANGLE_ANNOTATION = 6
    PDF_ANNOTS_ELLIPSE_ANNOTATION = 7

class PdfAnnotsTextMarkupType(IntEnum):
    PDF_ANNOTS_TEXT_MARKUP = 1
    PDF_ANNOTS_HIGHLIGHT = 2
    PDF_ANNOTS_UNDERLINE = 3
    PDF_ANNOTS_STRIKE_THROUGH = 4
    PDF_ANNOTS_SQUIGGLY = 5



# Structs type definitions

class GeomRealPoint(Structure):
    _fields_ = [
        ("x", c_double),
        ("y", c_double),
    ]
class GeomRealSize(Structure):
    _fields_ = [
        ("width", c_double),
        ("height", c_double),
    ]
class GeomRealRectangle(Structure):
    _fields_ = [
        ("left", c_double),
        ("bottom", c_double),
        ("right", c_double),
        ("top", c_double),
    ]
class GeomRealQuadrilateral(Structure):
    _fields_ = [
        ("bottom_left", GeomRealPoint),
        ("bottom_right", GeomRealPoint),
        ("top_right", GeomRealPoint),
        ("top_left", GeomRealPoint),
    ]
class GeomRealAffineTransform(Structure):
    _fields_ = [
        ("a", c_double),
        ("b", c_double),
        ("c", c_double),
        ("d", c_double),
        ("e", c_double),
        ("f", c_double),
    ]
class GeomIntSize(Structure):
    _fields_ = [
        ("width", c_int),
        ("height", c_int),
    ]
class PdfContentPathSegment(Structure):
    _fields_ = [
        ("end_point", GeomRealPoint),
        ("segment_type", c_int),
        ("control_point1", GeomRealPoint),
        ("control_point2", GeomRealPoint),
    ]
class PdfNavPageDisplay(Structure):
    _fields_ = [
        ("page_layout", c_int),
        ("continuous", c_bool),
    ]

class SysDate(Structure):
    _fields_ = [
        ("year", c_short),
        ("month", c_short),
        ("day", c_short),
        ("hour", c_short),
        ("minute", c_short),
        ("second", c_short),
        ("tz_sign", c_short),
        ("tz_hour", c_short),
        ("tz_minute", c_short),
    ]


# General library functions

_lib.PdfTools_Toolbox_Initialize.restype = None
_lib.PdfTools_Toolbox_Initialize.argtypes = []

def initialize():
    return _lib.PdfTools_Toolbox_Initialize()

_lib.PdfTools_Toolbox_Uninitialize.restype = None
_lib.PdfTools_Toolbox_Uninitialize.argtypes = []

def uninitialize():
    return _lib.PdfTools_Toolbox_Uninitialize()

_lib.PdfTools_Toolbox_GetLastError.argtypes = None
_lib.PdfTools_Toolbox_GetLastError.restype = c_int

def getlasterror():
    return _lib.PdfTools_Toolbox_GetLastError()

_lib.PdfTools_Toolbox_GetLastErrorMessageW.restype = c_size_t
_lib.PdfTools_Toolbox_GetLastErrorMessageW.argtypes = [POINTER(c_wchar), c_size_t]

def getlasterrormessage():
    buffer_size = _lib.PdfTools_Toolbox_GetLastErrorMessageW(None, 0)
    buffer = create_unicode_buffer(buffer_size)
    _lib.PdfTools_Toolbox_GetLastErrorMessageW(buffer, buffer_size)
    return utf16_to_string(buffer, buffer_size)

_lib.PdfTools_Toolbox_SetLastErrorW.argtypes = [c_int, c_wchar_p]
_lib.PdfTools_Toolbox_SetLastErrorW.restype = None

def setlasterror(error_code, error_message):
    return _lib.PdfTools_Toolbox_SetLastErrorW(error_code, string_to_utf16(error_message))

# General object functions

_lib.PdfTools_Toolbox_Release.restype = None
_lib.PdfTools_Toolbox_Release.argtypes = [c_void_p]

def release(object):
    _lib.PdfTools_Toolbox_Release(object)

_lib.PdfTools_Toolbox_AddRef.restype = None
_lib.PdfTools_Toolbox_AddRef.argtypes = [c_void_p]

def addref(object):
    _lib.PdfTools_Toolbox_AddRef(object)

_lib.PdfTools_Toolbox_Equals.restype = c_bool
_lib.PdfTools_Toolbox_Equals.argtypes = [c_void_p, c_void_p]

def equals(object, other):
    _lib.PdfTools_Toolbox_Equals(object, other)

_lib.PdfTools_Toolbox_GetHashCode.restype = c_int
_lib.PdfTools_Toolbox_GetHashCode.argtypes = [c_void_p]

def gethashcode(object):
    _lib.PdfTools_Toolbox_GetHashCode(object)

# Class functions
_lib.PdfTools_Toolbox_Sdk_InitializeW.argtypes = [c_wchar_p, c_wchar_p]
_lib.PdfTools_Toolbox_Sdk_InitializeW.restype = c_bool

def sdk_initialize(license, producer_suffix):
    return _lib.PdfTools_Toolbox_Sdk_InitializeW(string_to_utf16(license), string_to_utf16(producer_suffix))

_lib.PdfTools_Toolbox_Sdk_AddFontDirectoryW.argtypes = [c_wchar_p]
_lib.PdfTools_Toolbox_Sdk_AddFontDirectoryW.restype = c_bool

def sdk_addfontdirectory(directory):
    return _lib.PdfTools_Toolbox_Sdk_AddFontDirectoryW(string_to_utf16(directory))


_lib.PdfTools_Toolbox_Sdk_GetVersionW.argtypes = [POINTER(c_wchar), c_size_t]
_lib.PdfTools_Toolbox_Sdk_GetVersionW.restype = c_size_t

def sdk_getversion():
    ret_buffer_size = _lib.PdfTools_Toolbox_Sdk_GetVersionW(None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_Toolbox_Sdk_GetVersionW(ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_Toolbox_Sdk_GetProducerFullNameW.argtypes = [POINTER(c_wchar), c_size_t]
_lib.PdfTools_Toolbox_Sdk_GetProducerFullNameW.restype = c_size_t

def sdk_getproducerfullname():
    ret_buffer_size = _lib.PdfTools_Toolbox_Sdk_GetProducerFullNameW(None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_Toolbox_Sdk_GetProducerFullNameW(ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)


_lib.PdfTools_Toolbox_StringMap_GetCount.argtypes = [c_void_p]
_lib.PdfTools_Toolbox_StringMap_GetCount.restype = c_int

def stringmap_getcount(string_map):
    return _lib.PdfTools_Toolbox_StringMap_GetCount(string_map)
_lib.PdfTools_Toolbox_StringMap_GetSize.argtypes = [c_void_p]
_lib.PdfTools_Toolbox_StringMap_GetSize.restype = c_int

def stringmap_getsize(string_map):
    return _lib.PdfTools_Toolbox_StringMap_GetSize(string_map)
_lib.PdfTools_Toolbox_StringMap_GetBegin.argtypes = [c_void_p]
_lib.PdfTools_Toolbox_StringMap_GetBegin.restype = c_int

def stringmap_getbegin(string_map):
    return _lib.PdfTools_Toolbox_StringMap_GetBegin(string_map)
_lib.PdfTools_Toolbox_StringMap_GetEnd.argtypes = [c_void_p]
_lib.PdfTools_Toolbox_StringMap_GetEnd.restype = c_int

def stringmap_getend(string_map):
    return _lib.PdfTools_Toolbox_StringMap_GetEnd(string_map)
_lib.PdfTools_Toolbox_StringMap_GetNext.argtypes = [c_void_p, c_int]
_lib.PdfTools_Toolbox_StringMap_GetNext.restype = c_int

def stringmap_getnext(string_map, it):
    return _lib.PdfTools_Toolbox_StringMap_GetNext(string_map, it)
_lib.PdfTools_Toolbox_StringMap_GetW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_Toolbox_StringMap_GetW.restype = c_int

def stringmap_get(string_map, key):
    return _lib.PdfTools_Toolbox_StringMap_GetW(string_map, string_to_utf16(key))
_lib.PdfTools_Toolbox_StringMap_GetKeyW.argtypes = [c_void_p, c_int, POINTER(c_wchar), c_size_t]
_lib.PdfTools_Toolbox_StringMap_GetKeyW.restype = c_size_t

def stringmap_getkey(string_map, it):
    ret_buffer_size = _lib.PdfTools_Toolbox_StringMap_GetKeyW(string_map, it, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_Toolbox_StringMap_GetKeyW(string_map, it, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_Toolbox_StringMap_GetValueW.argtypes = [c_void_p, c_int, POINTER(c_wchar), c_size_t]
_lib.PdfTools_Toolbox_StringMap_GetValueW.restype = c_size_t

def stringmap_getvalue(string_map, it):
    ret_buffer_size = _lib.PdfTools_Toolbox_StringMap_GetValueW(string_map, it, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_Toolbox_StringMap_GetValueW(string_map, it, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_Toolbox_StringMap_SetW.argtypes = [c_void_p, c_wchar_p, c_wchar_p]
_lib.PdfTools_Toolbox_StringMap_SetW.restype = c_bool

def stringmap_set(string_map, key, value):
    return _lib.PdfTools_Toolbox_StringMap_SetW(string_map, string_to_utf16(key), string_to_utf16(value))

_lib.PdfTools_Toolbox_StringMap_SetValueW.argtypes = [c_void_p, c_int, c_wchar_p]
_lib.PdfTools_Toolbox_StringMap_SetValueW.restype = c_bool

def stringmap_setvalue(string_map, it, value):
    return _lib.PdfTools_Toolbox_StringMap_SetValueW(string_map, it, string_to_utf16(value))

_lib.PdfTools_Toolbox_StringMap_Clear.argtypes = [c_void_p]
_lib.PdfTools_Toolbox_StringMap_Clear.restype = c_bool

def stringmap_clear(string_map):
    return _lib.PdfTools_Toolbox_StringMap_Clear(string_map)

_lib.PdfTools_Toolbox_StringMap_Remove.argtypes = [c_void_p, c_int]
_lib.PdfTools_Toolbox_StringMap_Remove.restype = c_bool

def stringmap_remove(string_map, it):
    return _lib.PdfTools_Toolbox_StringMap_Remove(string_map, it)



_lib.PdfTools_ToolboxGeomReal_QuadrilateralList_GetCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxGeomReal_QuadrilateralList_GetCount.restype = c_int

def geomreal_quadrilaterallist_getcount(quadrilateral_list):
    return _lib.PdfTools_ToolboxGeomReal_QuadrilateralList_GetCount(quadrilateral_list)
_lib.PdfTools_ToolboxGeomReal_QuadrilateralList_Get.argtypes = [c_void_p, c_int, POINTER(GeomRealQuadrilateral)]
_lib.PdfTools_ToolboxGeomReal_QuadrilateralList_Get.restype = c_bool

def geomreal_quadrilaterallist_get(quadrilateral_list, i_index, ret_val):
    return _lib.PdfTools_ToolboxGeomReal_QuadrilateralList_Get(quadrilateral_list, i_index, byref(ret_val))
_lib.PdfTools_ToolboxGeomReal_QuadrilateralList_Add.argtypes = [c_void_p, POINTER(GeomRealQuadrilateral)]
_lib.PdfTools_ToolboxGeomReal_QuadrilateralList_Add.restype = c_bool

def geomreal_quadrilaterallist_add(quadrilateral_list, quadrilateral):
    return _lib.PdfTools_ToolboxGeomReal_QuadrilateralList_Add(quadrilateral_list, quadrilateral)
_lib.PdfTools_ToolboxGeomReal_QuadrilateralList_Clear.argtypes = [c_void_p]
_lib.PdfTools_ToolboxGeomReal_QuadrilateralList_Clear.restype = c_bool

def geomreal_quadrilaterallist_clear(quadrilateral_list):
    return _lib.PdfTools_ToolboxGeomReal_QuadrilateralList_Clear(quadrilateral_list)

_lib.PdfTools_ToolboxGeomReal_QuadrilateralList_Remove.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxGeomReal_QuadrilateralList_Remove.restype = c_bool

def geomreal_quadrilaterallist_remove(quadrilateral_list, index):
    return _lib.PdfTools_ToolboxGeomReal_QuadrilateralList_Remove(quadrilateral_list, index)

_lib.PdfTools_ToolboxGeomReal_QuadrilateralList_Set.argtypes = [c_void_p, c_int, POINTER(GeomRealQuadrilateral)]
_lib.PdfTools_ToolboxGeomReal_QuadrilateralList_Set.restype = c_bool

def geomreal_quadrilaterallist_set(quadrilateral_list, index, value):
    return _lib.PdfTools_ToolboxGeomReal_QuadrilateralList_Set(quadrilateral_list, index, value)


_lib.PdfTools_ToolboxGeomReal_QuadrilateralList_New.argtypes = []
_lib.PdfTools_ToolboxGeomReal_QuadrilateralList_New.restype = c_void_p

def geomreal_quadrilaterallist_new():
    return _lib.PdfTools_ToolboxGeomReal_QuadrilateralList_New()


_lib.PdfTools_ToolboxPdf_PageCopyOptions_New.argtypes = []
_lib.PdfTools_ToolboxPdf_PageCopyOptions_New.restype = c_void_p

def pdf_pagecopyoptions_new():
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_New()

_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetLinks.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetLinks.restype = c_int

def pdf_pagecopyoptions_getlinks(page_copy_options):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_GetLinks(page_copy_options)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetLinks.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetLinks.restype = c_bool

def pdf_pagecopyoptions_setlinks(page_copy_options, val):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_SetLinks(page_copy_options, val)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetFormFields.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetFormFields.restype = c_int

def pdf_pagecopyoptions_getformfields(page_copy_options):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_GetFormFields(page_copy_options)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetFormFields.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetFormFields.restype = c_bool

def pdf_pagecopyoptions_setformfields(page_copy_options, val):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_SetFormFields(page_copy_options, val)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetSignedSignatures.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetSignedSignatures.restype = c_int

def pdf_pagecopyoptions_getsignedsignatures(page_copy_options):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_GetSignedSignatures(page_copy_options)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetSignedSignatures.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetSignedSignatures.restype = c_bool

def pdf_pagecopyoptions_setsignedsignatures(page_copy_options, val):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_SetSignedSignatures(page_copy_options, val)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetUnsignedSignatures.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetUnsignedSignatures.restype = c_int

def pdf_pagecopyoptions_getunsignedsignatures(page_copy_options):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_GetUnsignedSignatures(page_copy_options)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetUnsignedSignatures.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetUnsignedSignatures.restype = c_bool

def pdf_pagecopyoptions_setunsignedsignatures(page_copy_options, val):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_SetUnsignedSignatures(page_copy_options, val)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetAnnotations.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetAnnotations.restype = c_int

def pdf_pagecopyoptions_getannotations(page_copy_options):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_GetAnnotations(page_copy_options)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetAnnotations.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetAnnotations.restype = c_bool

def pdf_pagecopyoptions_setannotations(page_copy_options, val):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_SetAnnotations(page_copy_options, val)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetCopyOutlineItems.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetCopyOutlineItems.restype = c_bool

def pdf_pagecopyoptions_getcopyoutlineitems(page_copy_options):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_GetCopyOutlineItems(page_copy_options)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetCopyOutlineItems.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetCopyOutlineItems.restype = c_bool

def pdf_pagecopyoptions_setcopyoutlineitems(page_copy_options, val):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_SetCopyOutlineItems(page_copy_options, val)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetCopyAssociatedFiles.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetCopyAssociatedFiles.restype = c_bool

def pdf_pagecopyoptions_getcopyassociatedfiles(page_copy_options):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_GetCopyAssociatedFiles(page_copy_options)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetCopyAssociatedFiles.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetCopyAssociatedFiles.restype = c_bool

def pdf_pagecopyoptions_setcopyassociatedfiles(page_copy_options, val):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_SetCopyAssociatedFiles(page_copy_options, val)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetCopyLogicalStructure.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetCopyLogicalStructure.restype = c_bool

def pdf_pagecopyoptions_getcopylogicalstructure(page_copy_options):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_GetCopyLogicalStructure(page_copy_options)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetCopyLogicalStructure.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetCopyLogicalStructure.restype = c_bool

def pdf_pagecopyoptions_setcopylogicalstructure(page_copy_options, val):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_SetCopyLogicalStructure(page_copy_options, val)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetFormFieldConflictResolution.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetFormFieldConflictResolution.restype = c_int

def pdf_pagecopyoptions_getformfieldconflictresolution(page_copy_options):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_GetFormFieldConflictResolution(page_copy_options)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetFormFieldConflictResolution.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetFormFieldConflictResolution.restype = c_bool

def pdf_pagecopyoptions_setformfieldconflictresolution(page_copy_options, val):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_SetFormFieldConflictResolution(page_copy_options, val)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetOcgConflictResolution.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetOcgConflictResolution.restype = c_int

def pdf_pagecopyoptions_getocgconflictresolution(page_copy_options):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_GetOcgConflictResolution(page_copy_options)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetOcgConflictResolution.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetOcgConflictResolution.restype = c_bool

def pdf_pagecopyoptions_setocgconflictresolution(page_copy_options, val):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_SetOcgConflictResolution(page_copy_options, val)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetNamedDestinations.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetNamedDestinations.restype = c_int

def pdf_pagecopyoptions_getnameddestinations(page_copy_options):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_GetNamedDestinations(page_copy_options)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetNamedDestinations.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetNamedDestinations.restype = c_bool

def pdf_pagecopyoptions_setnameddestinations(page_copy_options, val):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_SetNamedDestinations(page_copy_options, val)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetOptimizeResources.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_GetOptimizeResources.restype = c_bool

def pdf_pagecopyoptions_getoptimizeresources(page_copy_options):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_GetOptimizeResources(page_copy_options)
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetOptimizeResources.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdf_PageCopyOptions_SetOptimizeResources.restype = c_bool

def pdf_pagecopyoptions_setoptimizeresources(page_copy_options, val):
    return _lib.PdfTools_ToolboxPdf_PageCopyOptions_SetOptimizeResources(page_copy_options, val)


_lib.PdfTools_ToolboxPdf_Encryption_NewW.argtypes = [c_wchar_p, c_wchar_p, c_int]
_lib.PdfTools_ToolboxPdf_Encryption_NewW.restype = c_void_p

def pdf_encryption_new(user_password, owner_password, permissions):
    return _lib.PdfTools_ToolboxPdf_Encryption_NewW(string_to_utf16(user_password), string_to_utf16(owner_password), permissions)

_lib.PdfTools_ToolboxPdf_Encryption_GetUserPasswordW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdf_Encryption_GetUserPasswordW.restype = c_size_t

def pdf_encryption_getuserpassword(encryption):
    ret_buffer_size = _lib.PdfTools_ToolboxPdf_Encryption_GetUserPasswordW(encryption, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdf_Encryption_GetUserPasswordW(encryption, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdf_Encryption_SetUserPasswordW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdf_Encryption_SetUserPasswordW.restype = c_bool

def pdf_encryption_setuserpassword(encryption, val):
    return _lib.PdfTools_ToolboxPdf_Encryption_SetUserPasswordW(encryption, string_to_utf16(val))
_lib.PdfTools_ToolboxPdf_Encryption_GetOwnerPasswordW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdf_Encryption_GetOwnerPasswordW.restype = c_size_t

def pdf_encryption_getownerpassword(encryption):
    ret_buffer_size = _lib.PdfTools_ToolboxPdf_Encryption_GetOwnerPasswordW(encryption, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdf_Encryption_GetOwnerPasswordW(encryption, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdf_Encryption_SetOwnerPasswordW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdf_Encryption_SetOwnerPasswordW.restype = c_bool

def pdf_encryption_setownerpassword(encryption, val):
    return _lib.PdfTools_ToolboxPdf_Encryption_SetOwnerPasswordW(encryption, string_to_utf16(val))
_lib.PdfTools_ToolboxPdf_Encryption_GetPermissions.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Encryption_GetPermissions.restype = c_int

def pdf_encryption_getpermissions(encryption):
    return _lib.PdfTools_ToolboxPdf_Encryption_GetPermissions(encryption)
_lib.PdfTools_ToolboxPdf_Encryption_SetPermissions.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdf_Encryption_SetPermissions.restype = c_bool

def pdf_encryption_setpermissions(encryption, val):
    return _lib.PdfTools_ToolboxPdf_Encryption_SetPermissions(encryption, val)


_lib.PdfTools_ToolboxPdf_PageList_Copy.argtypes = [c_void_p, c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdf_PageList_Copy.restype = c_void_p

def pdf_pagelist_copy(target_document, page_list, options):
    return _lib.PdfTools_ToolboxPdf_PageList_Copy(target_document, page_list, options)
_lib.PdfTools_ToolboxPdf_PageList_GetCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_PageList_GetCount.restype = c_int

def pdf_pagelist_getcount(page_list):
    return _lib.PdfTools_ToolboxPdf_PageList_GetCount(page_list)
_lib.PdfTools_ToolboxPdf_PageList_Get.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdf_PageList_Get.restype = c_void_p

def pdf_pagelist_get(page_list, i_index):
    return _lib.PdfTools_ToolboxPdf_PageList_Get(page_list, i_index)
_lib.PdfTools_ToolboxPdf_PageList_GetRange.argtypes = [c_void_p, c_int, c_int]
_lib.PdfTools_ToolboxPdf_PageList_GetRange.restype = c_void_p

def pdf_pagelist_getrange(page_list, i_index, i_count):
    return _lib.PdfTools_ToolboxPdf_PageList_GetRange(page_list, i_index, i_count)
_lib.PdfTools_ToolboxPdf_PageList_Add.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdf_PageList_Add.restype = c_bool

def pdf_pagelist_add(page_list, page):
    return _lib.PdfTools_ToolboxPdf_PageList_Add(page_list, page)
_lib.PdfTools_ToolboxPdf_PageList_AddRange.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdf_PageList_AddRange.restype = c_bool

def pdf_pagelist_addrange(page_list, input):
    return _lib.PdfTools_ToolboxPdf_PageList_AddRange(page_list, input)


_lib.PdfTools_ToolboxPdf_FileReferenceList_GetCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_FileReferenceList_GetCount.restype = c_int

def pdf_filereferencelist_getcount(file_reference_list):
    return _lib.PdfTools_ToolboxPdf_FileReferenceList_GetCount(file_reference_list)
_lib.PdfTools_ToolboxPdf_FileReferenceList_Get.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdf_FileReferenceList_Get.restype = c_void_p

def pdf_filereferencelist_get(file_reference_list, i_index):
    return _lib.PdfTools_ToolboxPdf_FileReferenceList_Get(file_reference_list, i_index)
_lib.PdfTools_ToolboxPdf_FileReferenceList_Add.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdf_FileReferenceList_Add.restype = c_bool

def pdf_filereferencelist_add(file_reference_list, file_reference):
    return _lib.PdfTools_ToolboxPdf_FileReferenceList_Add(file_reference_list, file_reference)


_lib.PdfTools_ToolboxPdf_Document_OpenW.argtypes = [POINTER(StreamDescriptor), c_wchar_p]
_lib.PdfTools_ToolboxPdf_Document_OpenW.restype = c_void_p

def pdf_document_open(stream, password):
    return _lib.PdfTools_ToolboxPdf_Document_OpenW(stream, string_to_utf16(password))
_lib.PdfTools_ToolboxPdf_Document_OpenWithFdfW.argtypes = [POINTER(StreamDescriptor), POINTER(StreamDescriptor), c_wchar_p]
_lib.PdfTools_ToolboxPdf_Document_OpenWithFdfW.restype = c_void_p

def pdf_document_openwithfdf(pdf_stream, fdf_stream, password):
    return _lib.PdfTools_ToolboxPdf_Document_OpenWithFdfW(pdf_stream, fdf_stream, string_to_utf16(password))
_lib.PdfTools_ToolboxPdf_Document_Create.argtypes = [POINTER(StreamDescriptor), POINTER(c_int), c_void_p]
_lib.PdfTools_ToolboxPdf_Document_Create.restype = c_void_p

def pdf_document_create(stream, conformance, encryption):
    return _lib.PdfTools_ToolboxPdf_Document_Create(stream, byref(c_int(conformance)) if conformance is not None else None, encryption)
_lib.PdfTools_ToolboxPdf_Document_CreateWithFdf.argtypes = [POINTER(StreamDescriptor), POINTER(StreamDescriptor), POINTER(c_int), c_void_p]
_lib.PdfTools_ToolboxPdf_Document_CreateWithFdf.restype = c_void_p

def pdf_document_createwithfdf(pdf_stream, fdf_stream, conformance, encryption):
    return _lib.PdfTools_ToolboxPdf_Document_CreateWithFdf(pdf_stream, fdf_stream, byref(c_int(conformance)) if conformance is not None else None, encryption)

_lib.PdfTools_ToolboxPdf_Document_GetConformance.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Document_GetConformance.restype = c_int

def pdf_document_getconformance(document):
    return _lib.PdfTools_ToolboxPdf_Document_GetConformance(document)
_lib.PdfTools_ToolboxPdf_Document_GetMetadata.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Document_GetMetadata.restype = c_void_p

def pdf_document_getmetadata(document):
    return _lib.PdfTools_ToolboxPdf_Document_GetMetadata(document)
_lib.PdfTools_ToolboxPdf_Document_SetMetadata.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdf_Document_SetMetadata.restype = c_bool

def pdf_document_setmetadata(document, val):
    return _lib.PdfTools_ToolboxPdf_Document_SetMetadata(document, val)
_lib.PdfTools_ToolboxPdf_Document_GetPages.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Document_GetPages.restype = c_void_p

def pdf_document_getpages(document):
    return _lib.PdfTools_ToolboxPdf_Document_GetPages(document)
_lib.PdfTools_ToolboxPdf_Document_GetOutputIntent.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Document_GetOutputIntent.restype = c_void_p

def pdf_document_getoutputintent(document):
    return _lib.PdfTools_ToolboxPdf_Document_GetOutputIntent(document)
_lib.PdfTools_ToolboxPdf_Document_SetOutputIntent.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdf_Document_SetOutputIntent.restype = c_bool

def pdf_document_setoutputintent(document, val):
    return _lib.PdfTools_ToolboxPdf_Document_SetOutputIntent(document, val)
_lib.PdfTools_ToolboxPdf_Document_GetFormFields.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Document_GetFormFields.restype = c_void_p

def pdf_document_getformfields(document):
    return _lib.PdfTools_ToolboxPdf_Document_GetFormFields(document)
_lib.PdfTools_ToolboxPdf_Document_GetSignatureFields.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Document_GetSignatureFields.restype = c_void_p

def pdf_document_getsignaturefields(document):
    return _lib.PdfTools_ToolboxPdf_Document_GetSignatureFields(document)
_lib.PdfTools_ToolboxPdf_Document_GetPlainEmbeddedFiles.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Document_GetPlainEmbeddedFiles.restype = c_void_p

def pdf_document_getplainembeddedfiles(document):
    return _lib.PdfTools_ToolboxPdf_Document_GetPlainEmbeddedFiles(document)
_lib.PdfTools_ToolboxPdf_Document_GetAssociatedFiles.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Document_GetAssociatedFiles.restype = c_void_p

def pdf_document_getassociatedfiles(document):
    return _lib.PdfTools_ToolboxPdf_Document_GetAssociatedFiles(document)
_lib.PdfTools_ToolboxPdf_Document_GetAllEmbeddedFiles.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Document_GetAllEmbeddedFiles.restype = c_void_p

def pdf_document_getallembeddedfiles(document):
    return _lib.PdfTools_ToolboxPdf_Document_GetAllEmbeddedFiles(document)
_lib.PdfTools_ToolboxPdf_Document_GetOutline.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Document_GetOutline.restype = c_void_p

def pdf_document_getoutline(document):
    return _lib.PdfTools_ToolboxPdf_Document_GetOutline(document)
_lib.PdfTools_ToolboxPdf_Document_GetOpenDestination.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Document_GetOpenDestination.restype = c_void_p

def pdf_document_getopendestination(document):
    return _lib.PdfTools_ToolboxPdf_Document_GetOpenDestination(document)
_lib.PdfTools_ToolboxPdf_Document_SetOpenDestination.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdf_Document_SetOpenDestination.restype = c_bool

def pdf_document_setopendestination(document, val):
    return _lib.PdfTools_ToolboxPdf_Document_SetOpenDestination(document, val)
_lib.PdfTools_ToolboxPdf_Document_GetPermissions.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfTools_ToolboxPdf_Document_GetPermissions.restype = c_bool

def pdf_document_getpermissions(document, ret_val):
    return _lib.PdfTools_ToolboxPdf_Document_GetPermissions(document, byref(ret_val))
_lib.PdfTools_ToolboxPdf_Document_GetViewerSettings.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Document_GetViewerSettings.restype = c_void_p

def pdf_document_getviewersettings(document):
    return _lib.PdfTools_ToolboxPdf_Document_GetViewerSettings(document)
_lib.PdfTools_ToolboxPdf_Document_SetViewerSettings.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdf_Document_SetViewerSettings.restype = c_bool

def pdf_document_setviewersettings(document, val):
    return _lib.PdfTools_ToolboxPdf_Document_SetViewerSettings(document, val)
_lib.PdfTools_ToolboxPdf_Document_IsLinearized.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Document_IsLinearized.restype = c_bool

def pdf_document_islinearized(document):
    return _lib.PdfTools_ToolboxPdf_Document_IsLinearized(document)

_lib.PdfTools_ToolboxPdf_Document_Close.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Document_Close.restype = c_bool

def pdf_document_close(object):
    return _lib.PdfTools_ToolboxPdf_Document_Close(object)


_lib.PdfTools_ToolboxPdf_Page_Create.argtypes = [c_void_p, POINTER(GeomRealSize)]
_lib.PdfTools_ToolboxPdf_Page_Create.restype = c_void_p

def pdf_page_create(target_document, size):
    return _lib.PdfTools_ToolboxPdf_Page_Create(target_document, size)
_lib.PdfTools_ToolboxPdf_Page_Copy.argtypes = [c_void_p, c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdf_Page_Copy.restype = c_void_p

def pdf_page_copy(target_document, page, options):
    return _lib.PdfTools_ToolboxPdf_Page_Copy(target_document, page, options)
_lib.PdfTools_ToolboxPdf_Page_UpdateSize.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdf_Page_UpdateSize.restype = c_bool

def pdf_page_updatesize(page, rectangle):
    return _lib.PdfTools_ToolboxPdf_Page_UpdateSize(page, rectangle)

_lib.PdfTools_ToolboxPdf_Page_Rotate.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdf_Page_Rotate.restype = c_bool

def pdf_page_rotate(page, rotate):
    return _lib.PdfTools_ToolboxPdf_Page_Rotate(page, rotate)


_lib.PdfTools_ToolboxPdf_Page_GetSize.argtypes = [c_void_p, POINTER(GeomRealSize)]
_lib.PdfTools_ToolboxPdf_Page_GetSize.restype = c_bool

def pdf_page_getsize(page, ret_val):
    return _lib.PdfTools_ToolboxPdf_Page_GetSize(page, byref(ret_val))
_lib.PdfTools_ToolboxPdf_Page_GetMediaBox.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdf_Page_GetMediaBox.restype = c_bool

def pdf_page_getmediabox(page, ret_val):
    return _lib.PdfTools_ToolboxPdf_Page_GetMediaBox(page, byref(ret_val))
_lib.PdfTools_ToolboxPdf_Page_GetBleedBox.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdf_Page_GetBleedBox.restype = c_bool

def pdf_page_getbleedbox(page, ret_val):
    return _lib.PdfTools_ToolboxPdf_Page_GetBleedBox(page, byref(ret_val))
_lib.PdfTools_ToolboxPdf_Page_GetTrimBox.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdf_Page_GetTrimBox.restype = c_bool

def pdf_page_gettrimbox(page, ret_val):
    return _lib.PdfTools_ToolboxPdf_Page_GetTrimBox(page, byref(ret_val))
_lib.PdfTools_ToolboxPdf_Page_GetArtBox.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdf_Page_GetArtBox.restype = c_bool

def pdf_page_getartbox(page, ret_val):
    return _lib.PdfTools_ToolboxPdf_Page_GetArtBox(page, byref(ret_val))
_lib.PdfTools_ToolboxPdf_Page_GetContent.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Page_GetContent.restype = c_void_p

def pdf_page_getcontent(page):
    return _lib.PdfTools_ToolboxPdf_Page_GetContent(page)
_lib.PdfTools_ToolboxPdf_Page_GetAnnotations.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Page_GetAnnotations.restype = c_void_p

def pdf_page_getannotations(page):
    return _lib.PdfTools_ToolboxPdf_Page_GetAnnotations(page)
_lib.PdfTools_ToolboxPdf_Page_GetLinks.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Page_GetLinks.restype = c_void_p

def pdf_page_getlinks(page):
    return _lib.PdfTools_ToolboxPdf_Page_GetLinks(page)
_lib.PdfTools_ToolboxPdf_Page_GetWidgets.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Page_GetWidgets.restype = c_void_p

def pdf_page_getwidgets(page):
    return _lib.PdfTools_ToolboxPdf_Page_GetWidgets(page)
_lib.PdfTools_ToolboxPdf_Page_GetMetadata.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Page_GetMetadata.restype = c_void_p

def pdf_page_getmetadata(page):
    return _lib.PdfTools_ToolboxPdf_Page_GetMetadata(page)
_lib.PdfTools_ToolboxPdf_Page_SetMetadata.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdf_Page_SetMetadata.restype = c_bool

def pdf_page_setmetadata(page, val):
    return _lib.PdfTools_ToolboxPdf_Page_SetMetadata(page, val)
_lib.PdfTools_ToolboxPdf_Page_GetPageLabelW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdf_Page_GetPageLabelW.restype = c_size_t

def pdf_page_getpagelabel(page):
    ret_buffer_size = _lib.PdfTools_ToolboxPdf_Page_GetPageLabelW(page, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdf_Page_GetPageLabelW(page, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)


_lib.PdfTools_ToolboxPdf_Metadata_Create.argtypes = [c_void_p, POINTER(StreamDescriptor)]
_lib.PdfTools_ToolboxPdf_Metadata_Create.restype = c_void_p

def pdf_metadata_create(target_document, xmp):
    return _lib.PdfTools_ToolboxPdf_Metadata_Create(target_document, xmp)
_lib.PdfTools_ToolboxPdf_Metadata_Copy.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdf_Metadata_Copy.restype = c_void_p

def pdf_metadata_copy(target_document, metadata):
    return _lib.PdfTools_ToolboxPdf_Metadata_Copy(target_document, metadata)

_lib.PdfTools_ToolboxPdf_Metadata_GetTitleW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdf_Metadata_GetTitleW.restype = c_size_t

def pdf_metadata_gettitle(metadata):
    ret_buffer_size = _lib.PdfTools_ToolboxPdf_Metadata_GetTitleW(metadata, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdf_Metadata_GetTitleW(metadata, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdf_Metadata_SetTitleW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdf_Metadata_SetTitleW.restype = c_bool

def pdf_metadata_settitle(metadata, val):
    return _lib.PdfTools_ToolboxPdf_Metadata_SetTitleW(metadata, string_to_utf16(val))
_lib.PdfTools_ToolboxPdf_Metadata_GetAuthorW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdf_Metadata_GetAuthorW.restype = c_size_t

def pdf_metadata_getauthor(metadata):
    ret_buffer_size = _lib.PdfTools_ToolboxPdf_Metadata_GetAuthorW(metadata, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdf_Metadata_GetAuthorW(metadata, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdf_Metadata_SetAuthorW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdf_Metadata_SetAuthorW.restype = c_bool

def pdf_metadata_setauthor(metadata, val):
    return _lib.PdfTools_ToolboxPdf_Metadata_SetAuthorW(metadata, string_to_utf16(val))
_lib.PdfTools_ToolboxPdf_Metadata_GetSubjectW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdf_Metadata_GetSubjectW.restype = c_size_t

def pdf_metadata_getsubject(metadata):
    ret_buffer_size = _lib.PdfTools_ToolboxPdf_Metadata_GetSubjectW(metadata, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdf_Metadata_GetSubjectW(metadata, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdf_Metadata_SetSubjectW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdf_Metadata_SetSubjectW.restype = c_bool

def pdf_metadata_setsubject(metadata, val):
    return _lib.PdfTools_ToolboxPdf_Metadata_SetSubjectW(metadata, string_to_utf16(val))
_lib.PdfTools_ToolboxPdf_Metadata_GetKeywordsW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdf_Metadata_GetKeywordsW.restype = c_size_t

def pdf_metadata_getkeywords(metadata):
    ret_buffer_size = _lib.PdfTools_ToolboxPdf_Metadata_GetKeywordsW(metadata, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdf_Metadata_GetKeywordsW(metadata, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdf_Metadata_SetKeywordsW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdf_Metadata_SetKeywordsW.restype = c_bool

def pdf_metadata_setkeywords(metadata, val):
    return _lib.PdfTools_ToolboxPdf_Metadata_SetKeywordsW(metadata, string_to_utf16(val))
_lib.PdfTools_ToolboxPdf_Metadata_GetCreatorW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdf_Metadata_GetCreatorW.restype = c_size_t

def pdf_metadata_getcreator(metadata):
    ret_buffer_size = _lib.PdfTools_ToolboxPdf_Metadata_GetCreatorW(metadata, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdf_Metadata_GetCreatorW(metadata, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdf_Metadata_SetCreatorW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdf_Metadata_SetCreatorW.restype = c_bool

def pdf_metadata_setcreator(metadata, val):
    return _lib.PdfTools_ToolboxPdf_Metadata_SetCreatorW(metadata, string_to_utf16(val))
_lib.PdfTools_ToolboxPdf_Metadata_GetProducerW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdf_Metadata_GetProducerW.restype = c_size_t

def pdf_metadata_getproducer(metadata):
    ret_buffer_size = _lib.PdfTools_ToolboxPdf_Metadata_GetProducerW(metadata, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdf_Metadata_GetProducerW(metadata, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdf_Metadata_GetCreationDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfTools_ToolboxPdf_Metadata_GetCreationDate.restype = c_bool

def pdf_metadata_getcreationdate(metadata, ret_val):
    return _lib.PdfTools_ToolboxPdf_Metadata_GetCreationDate(metadata, byref(ret_val))
_lib.PdfTools_ToolboxPdf_Metadata_SetCreationDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfTools_ToolboxPdf_Metadata_SetCreationDate.restype = c_bool

def pdf_metadata_setcreationdate(metadata, val):
    return _lib.PdfTools_ToolboxPdf_Metadata_SetCreationDate(metadata, val)
_lib.PdfTools_ToolboxPdf_Metadata_GetModificationDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfTools_ToolboxPdf_Metadata_GetModificationDate.restype = c_bool

def pdf_metadata_getmodificationdate(metadata, ret_val):
    return _lib.PdfTools_ToolboxPdf_Metadata_GetModificationDate(metadata, byref(ret_val))
_lib.PdfTools_ToolboxPdf_Metadata_GetXmp.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Metadata_GetXmp.restype = POINTER(StreamDescriptor)

def pdf_metadata_getxmp(metadata):
    return _lib.PdfTools_ToolboxPdf_Metadata_GetXmp(metadata)
_lib.PdfTools_ToolboxPdf_Metadata_GetCustomEntries.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_Metadata_GetCustomEntries.restype = c_void_p

def pdf_metadata_getcustomentries(metadata):
    return _lib.PdfTools_ToolboxPdf_Metadata_GetCustomEntries(metadata)


_lib.PdfTools_ToolboxPdf_FileReference_CreateW.argtypes = [c_void_p, POINTER(StreamDescriptor), c_wchar_p, c_wchar_p, c_wchar_p, POINTER(SysDate)]
_lib.PdfTools_ToolboxPdf_FileReference_CreateW.restype = c_void_p

def pdf_filereference_create(target_document, data, name, media_type, description, modification_date):
    return _lib.PdfTools_ToolboxPdf_FileReference_CreateW(target_document, data, string_to_utf16(name), string_to_utf16(media_type), string_to_utf16(description), modification_date)
_lib.PdfTools_ToolboxPdf_FileReference_Copy.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdf_FileReference_Copy.restype = c_void_p

def pdf_filereference_copy(target_document, file_reference):
    return _lib.PdfTools_ToolboxPdf_FileReference_Copy(target_document, file_reference)

_lib.PdfTools_ToolboxPdf_FileReference_GetAssociationRelationshipW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdf_FileReference_GetAssociationRelationshipW.restype = c_size_t

def pdf_filereference_getassociationrelationship(file_reference):
    ret_buffer_size = _lib.PdfTools_ToolboxPdf_FileReference_GetAssociationRelationshipW(file_reference, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdf_FileReference_GetAssociationRelationshipW(file_reference, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdf_FileReference_SetAssociationRelationshipW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdf_FileReference_SetAssociationRelationshipW.restype = c_bool

def pdf_filereference_setassociationrelationship(file_reference, val):
    return _lib.PdfTools_ToolboxPdf_FileReference_SetAssociationRelationshipW(file_reference, string_to_utf16(val))
_lib.PdfTools_ToolboxPdf_FileReference_GetDescriptionW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdf_FileReference_GetDescriptionW.restype = c_size_t

def pdf_filereference_getdescription(file_reference):
    ret_buffer_size = _lib.PdfTools_ToolboxPdf_FileReference_GetDescriptionW(file_reference, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdf_FileReference_GetDescriptionW(file_reference, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdf_FileReference_GetMediaTypeW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdf_FileReference_GetMediaTypeW.restype = c_size_t

def pdf_filereference_getmediatype(file_reference):
    ret_buffer_size = _lib.PdfTools_ToolboxPdf_FileReference_GetMediaTypeW(file_reference, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdf_FileReference_GetMediaTypeW(file_reference, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdf_FileReference_GetModificationDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfTools_ToolboxPdf_FileReference_GetModificationDate.restype = c_bool

def pdf_filereference_getmodificationdate(file_reference, ret_val):
    return _lib.PdfTools_ToolboxPdf_FileReference_GetModificationDate(file_reference, byref(ret_val))
_lib.PdfTools_ToolboxPdf_FileReference_GetNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdf_FileReference_GetNameW.restype = c_size_t

def pdf_filereference_getname(file_reference):
    ret_buffer_size = _lib.PdfTools_ToolboxPdf_FileReference_GetNameW(file_reference, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdf_FileReference_GetNameW(file_reference, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdf_FileReference_GetData.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdf_FileReference_GetData.restype = POINTER(StreamDescriptor)

def pdf_filereference_getdata(file_reference):
    return _lib.PdfTools_ToolboxPdf_FileReference_GetData(file_reference)


_lib.PdfTools_ToolboxPdfContent_Transparency_New.argtypes = [c_double]
_lib.PdfTools_ToolboxPdfContent_Transparency_New.restype = c_void_p

def pdfcontent_transparency_new(alpha):
    return _lib.PdfTools_ToolboxPdfContent_Transparency_New(alpha)

_lib.PdfTools_ToolboxPdfContent_Transparency_GetBlendMode.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Transparency_GetBlendMode.restype = c_int

def pdfcontent_transparency_getblendmode(transparency):
    return _lib.PdfTools_ToolboxPdfContent_Transparency_GetBlendMode(transparency)
_lib.PdfTools_ToolboxPdfContent_Transparency_SetBlendMode.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfContent_Transparency_SetBlendMode.restype = c_bool

def pdfcontent_transparency_setblendmode(transparency, val):
    return _lib.PdfTools_ToolboxPdfContent_Transparency_SetBlendMode(transparency, val)
_lib.PdfTools_ToolboxPdfContent_Transparency_GetAlpha.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Transparency_GetAlpha.restype = c_double

def pdfcontent_transparency_getalpha(transparency):
    return _lib.PdfTools_ToolboxPdfContent_Transparency_GetAlpha(transparency)
_lib.PdfTools_ToolboxPdfContent_Transparency_SetAlpha.argtypes = [c_void_p, c_double]
_lib.PdfTools_ToolboxPdfContent_Transparency_SetAlpha.restype = c_bool

def pdfcontent_transparency_setalpha(transparency, val):
    return _lib.PdfTools_ToolboxPdfContent_Transparency_SetAlpha(transparency, val)


_lib.PdfTools_ToolboxPdfContent_Stroke_New.argtypes = [c_void_p, c_double]
_lib.PdfTools_ToolboxPdfContent_Stroke_New.restype = c_void_p

def pdfcontent_stroke_new(paint, line_width):
    return _lib.PdfTools_ToolboxPdfContent_Stroke_New(paint, line_width)

_lib.PdfTools_ToolboxPdfContent_Stroke_GetPaint.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Stroke_GetPaint.restype = c_void_p

def pdfcontent_stroke_getpaint(stroke):
    return _lib.PdfTools_ToolboxPdfContent_Stroke_GetPaint(stroke)
_lib.PdfTools_ToolboxPdfContent_Stroke_SetPaint.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfContent_Stroke_SetPaint.restype = c_bool

def pdfcontent_stroke_setpaint(stroke, val):
    return _lib.PdfTools_ToolboxPdfContent_Stroke_SetPaint(stroke, val)
_lib.PdfTools_ToolboxPdfContent_Stroke_GetLineWidth.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Stroke_GetLineWidth.restype = c_double

def pdfcontent_stroke_getlinewidth(stroke):
    return _lib.PdfTools_ToolboxPdfContent_Stroke_GetLineWidth(stroke)
_lib.PdfTools_ToolboxPdfContent_Stroke_SetLineWidth.argtypes = [c_void_p, c_double]
_lib.PdfTools_ToolboxPdfContent_Stroke_SetLineWidth.restype = c_bool

def pdfcontent_stroke_setlinewidth(stroke, val):
    return _lib.PdfTools_ToolboxPdfContent_Stroke_SetLineWidth(stroke, val)
_lib.PdfTools_ToolboxPdfContent_Stroke_GetLineCapStyle.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Stroke_GetLineCapStyle.restype = c_int

def pdfcontent_stroke_getlinecapstyle(stroke):
    return _lib.PdfTools_ToolboxPdfContent_Stroke_GetLineCapStyle(stroke)
_lib.PdfTools_ToolboxPdfContent_Stroke_SetLineCapStyle.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfContent_Stroke_SetLineCapStyle.restype = c_bool

def pdfcontent_stroke_setlinecapstyle(stroke, val):
    return _lib.PdfTools_ToolboxPdfContent_Stroke_SetLineCapStyle(stroke, val)
_lib.PdfTools_ToolboxPdfContent_Stroke_GetLineJoinStyle.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Stroke_GetLineJoinStyle.restype = c_int

def pdfcontent_stroke_getlinejoinstyle(stroke):
    return _lib.PdfTools_ToolboxPdfContent_Stroke_GetLineJoinStyle(stroke)
_lib.PdfTools_ToolboxPdfContent_Stroke_SetLineJoinStyle.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfContent_Stroke_SetLineJoinStyle.restype = c_bool

def pdfcontent_stroke_setlinejoinstyle(stroke, val):
    return _lib.PdfTools_ToolboxPdfContent_Stroke_SetLineJoinStyle(stroke, val)
_lib.PdfTools_ToolboxPdfContent_Stroke_GetDashArray.argtypes = [c_void_p, POINTER(c_double), c_size_t]
_lib.PdfTools_ToolboxPdfContent_Stroke_GetDashArray.restype = c_size_t

def pdfcontent_stroke_getdasharray(stroke, ret_val, ret_val_buffer):
    return _lib.PdfTools_ToolboxPdfContent_Stroke_GetDashArray(stroke, ret_val, ret_val_buffer)
_lib.PdfTools_ToolboxPdfContent_Stroke_SetDashArray.argtypes = [c_void_p, POINTER(c_double), c_size_t]
_lib.PdfTools_ToolboxPdfContent_Stroke_SetDashArray.restype = c_bool

def pdfcontent_stroke_setdasharray(stroke, val, val_buffer):
    return _lib.PdfTools_ToolboxPdfContent_Stroke_SetDashArray(stroke, val, val_buffer)
_lib.PdfTools_ToolboxPdfContent_Stroke_GetDashPhase.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Stroke_GetDashPhase.restype = c_double

def pdfcontent_stroke_getdashphase(stroke):
    return _lib.PdfTools_ToolboxPdfContent_Stroke_GetDashPhase(stroke)
_lib.PdfTools_ToolboxPdfContent_Stroke_SetDashPhase.argtypes = [c_void_p, c_double]
_lib.PdfTools_ToolboxPdfContent_Stroke_SetDashPhase.restype = c_bool

def pdfcontent_stroke_setdashphase(stroke, val):
    return _lib.PdfTools_ToolboxPdfContent_Stroke_SetDashPhase(stroke, val)
_lib.PdfTools_ToolboxPdfContent_Stroke_GetMiterLimit.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Stroke_GetMiterLimit.restype = c_double

def pdfcontent_stroke_getmiterlimit(stroke):
    return _lib.PdfTools_ToolboxPdfContent_Stroke_GetMiterLimit(stroke)
_lib.PdfTools_ToolboxPdfContent_Stroke_SetMiterLimit.argtypes = [c_void_p, c_double]
_lib.PdfTools_ToolboxPdfContent_Stroke_SetMiterLimit.restype = c_bool

def pdfcontent_stroke_setmiterlimit(stroke, val):
    return _lib.PdfTools_ToolboxPdfContent_Stroke_SetMiterLimit(stroke, val)


_lib.PdfTools_ToolboxPdfContent_Fill_New.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Fill_New.restype = c_void_p

def pdfcontent_fill_new(paint):
    return _lib.PdfTools_ToolboxPdfContent_Fill_New(paint)

_lib.PdfTools_ToolboxPdfContent_Fill_GetPaint.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Fill_GetPaint.restype = c_void_p

def pdfcontent_fill_getpaint(fill):
    return _lib.PdfTools_ToolboxPdfContent_Fill_GetPaint(fill)
_lib.PdfTools_ToolboxPdfContent_Fill_SetPaint.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfContent_Fill_SetPaint.restype = c_bool

def pdfcontent_fill_setpaint(fill, val):
    return _lib.PdfTools_ToolboxPdfContent_Fill_SetPaint(fill, val)
_lib.PdfTools_ToolboxPdfContent_Fill_GetInsideRule.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Fill_GetInsideRule.restype = c_int

def pdfcontent_fill_getinsiderule(fill):
    return _lib.PdfTools_ToolboxPdfContent_Fill_GetInsideRule(fill)
_lib.PdfTools_ToolboxPdfContent_Fill_SetInsideRule.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfContent_Fill_SetInsideRule.restype = c_bool

def pdfcontent_fill_setinsiderule(fill, val):
    return _lib.PdfTools_ToolboxPdfContent_Fill_SetInsideRule(fill, val)


_lib.PdfTools_ToolboxPdfContent_Image_Create.argtypes = [c_void_p, POINTER(StreamDescriptor)]
_lib.PdfTools_ToolboxPdfContent_Image_Create.restype = c_void_p

def pdfcontent_image_create(target_document, stream):
    return _lib.PdfTools_ToolboxPdfContent_Image_Create(target_document, stream)
_lib.PdfTools_ToolboxPdfContent_Image_Extract.argtypes = [c_void_p, POINTER(StreamDescriptor), POINTER(c_int)]
_lib.PdfTools_ToolboxPdfContent_Image_Extract.restype = c_bool

def pdfcontent_image_extract(image, stream, image_type):
    return _lib.PdfTools_ToolboxPdfContent_Image_Extract(image, stream, byref(c_int(image_type)) if image_type is not None else None)


_lib.PdfTools_ToolboxPdfContent_Image_GetDefaultImageType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Image_GetDefaultImageType.restype = c_int

def pdfcontent_image_getdefaultimagetype(image):
    return _lib.PdfTools_ToolboxPdfContent_Image_GetDefaultImageType(image)
_lib.PdfTools_ToolboxPdfContent_Image_GetSize.argtypes = [c_void_p, POINTER(GeomIntSize)]
_lib.PdfTools_ToolboxPdfContent_Image_GetSize.restype = c_bool

def pdfcontent_image_getsize(image, ret_val):
    return _lib.PdfTools_ToolboxPdfContent_Image_GetSize(image, byref(ret_val))
_lib.PdfTools_ToolboxPdfContent_Image_GetSamples.argtypes = [c_void_p, POINTER(c_ubyte), c_size_t]
_lib.PdfTools_ToolboxPdfContent_Image_GetSamples.restype = c_size_t

def pdfcontent_image_getsamples(image, ret_val, ret_val_buffer):
    return _lib.PdfTools_ToolboxPdfContent_Image_GetSamples(image, ret_val, ret_val_buffer)
_lib.PdfTools_ToolboxPdfContent_Image_GetBitsPerComponent.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Image_GetBitsPerComponent.restype = c_int

def pdfcontent_image_getbitspercomponent(image):
    return _lib.PdfTools_ToolboxPdfContent_Image_GetBitsPerComponent(image)
_lib.PdfTools_ToolboxPdfContent_Image_GetColorSpace.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Image_GetColorSpace.restype = c_void_p

def pdfcontent_image_getcolorspace(image):
    return _lib.PdfTools_ToolboxPdfContent_Image_GetColorSpace(image)


_lib.PdfTools_ToolboxPdfContent_ImageMask_Create.argtypes = [c_void_p, POINTER(StreamDescriptor)]
_lib.PdfTools_ToolboxPdfContent_ImageMask_Create.restype = c_void_p

def pdfcontent_imagemask_create(target_document, stream):
    return _lib.PdfTools_ToolboxPdfContent_ImageMask_Create(target_document, stream)
_lib.PdfTools_ToolboxPdfContent_ImageMask_Extract.argtypes = [c_void_p, POINTER(StreamDescriptor), POINTER(c_int)]
_lib.PdfTools_ToolboxPdfContent_ImageMask_Extract.restype = c_bool

def pdfcontent_imagemask_extract(image_mask, stream, image_type):
    return _lib.PdfTools_ToolboxPdfContent_ImageMask_Extract(image_mask, stream, byref(c_int(image_type)) if image_type is not None else None)


_lib.PdfTools_ToolboxPdfContent_ImageMask_GetSize.argtypes = [c_void_p, POINTER(GeomIntSize)]
_lib.PdfTools_ToolboxPdfContent_ImageMask_GetSize.restype = c_bool

def pdfcontent_imagemask_getsize(image_mask, ret_val):
    return _lib.PdfTools_ToolboxPdfContent_ImageMask_GetSize(image_mask, byref(ret_val))


_lib.PdfTools_ToolboxPdfContent_Font_Create.argtypes = [c_void_p, POINTER(StreamDescriptor), c_bool]
_lib.PdfTools_ToolboxPdfContent_Font_Create.restype = c_void_p

def pdfcontent_font_create(target_document, stream, embedded):
    return _lib.PdfTools_ToolboxPdfContent_Font_Create(target_document, stream, embedded)
_lib.PdfTools_ToolboxPdfContent_Font_CreateFromSystemW.argtypes = [c_void_p, c_wchar_p, c_wchar_p, c_bool]
_lib.PdfTools_ToolboxPdfContent_Font_CreateFromSystemW.restype = c_void_p

def pdfcontent_font_createfromsystem(target_document, family, style, embedded):
    return _lib.PdfTools_ToolboxPdfContent_Font_CreateFromSystemW(target_document, string_to_utf16(family), string_to_utf16(style), embedded)
_lib.PdfTools_ToolboxPdfContent_Font_GetCharacterWidth.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfContent_Font_GetCharacterWidth.restype = c_double

def pdfcontent_font_getcharacterwidth(font, character):
    return _lib.PdfTools_ToolboxPdfContent_Font_GetCharacterWidth(font, character)

_lib.PdfTools_ToolboxPdfContent_Font_GetBaseFontW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfContent_Font_GetBaseFontW.restype = c_size_t

def pdfcontent_font_getbasefont(font):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfContent_Font_GetBaseFontW(font, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfContent_Font_GetBaseFontW(font, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfContent_Font_GetWeight.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfTools_ToolboxPdfContent_Font_GetWeight.restype = c_bool

def pdfcontent_font_getweight(font, ret_val):
    return _lib.PdfTools_ToolboxPdfContent_Font_GetWeight(font, byref(ret_val))
_lib.PdfTools_ToolboxPdfContent_Font_GetItalicAngle.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Font_GetItalicAngle.restype = c_double

def pdfcontent_font_getitalicangle(font):
    return _lib.PdfTools_ToolboxPdfContent_Font_GetItalicAngle(font)
_lib.PdfTools_ToolboxPdfContent_Font_GetAscent.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Font_GetAscent.restype = c_double

def pdfcontent_font_getascent(font):
    return _lib.PdfTools_ToolboxPdfContent_Font_GetAscent(font)
_lib.PdfTools_ToolboxPdfContent_Font_GetDescent.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Font_GetDescent.restype = c_double

def pdfcontent_font_getdescent(font):
    return _lib.PdfTools_ToolboxPdfContent_Font_GetDescent(font)
_lib.PdfTools_ToolboxPdfContent_Font_GetCapHeight.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Font_GetCapHeight.restype = c_double

def pdfcontent_font_getcapheight(font):
    return _lib.PdfTools_ToolboxPdfContent_Font_GetCapHeight(font)
_lib.PdfTools_ToolboxPdfContent_Font_GetLeading.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfTools_ToolboxPdfContent_Font_GetLeading.restype = c_bool

def pdfcontent_font_getleading(font, ret_val):
    return _lib.PdfTools_ToolboxPdfContent_Font_GetLeading(font, byref(ret_val))


_lib.PdfTools_ToolboxPdfContent_Group_Create.argtypes = [c_void_p, POINTER(GeomRealSize)]
_lib.PdfTools_ToolboxPdfContent_Group_Create.restype = c_void_p

def pdfcontent_group_create(target_document, size):
    return _lib.PdfTools_ToolboxPdfContent_Group_Create(target_document, size)
_lib.PdfTools_ToolboxPdfContent_Group_CopyFromPage.argtypes = [c_void_p, c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfContent_Group_CopyFromPage.restype = c_void_p

def pdfcontent_group_copyfrompage(target_document, page, options):
    return _lib.PdfTools_ToolboxPdfContent_Group_CopyFromPage(target_document, page, options)

_lib.PdfTools_ToolboxPdfContent_Group_GetSize.argtypes = [c_void_p, POINTER(GeomRealSize)]
_lib.PdfTools_ToolboxPdfContent_Group_GetSize.restype = c_bool

def pdfcontent_group_getsize(group, ret_val):
    return _lib.PdfTools_ToolboxPdfContent_Group_GetSize(group, byref(ret_val))
_lib.PdfTools_ToolboxPdfContent_Group_GetContent.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Group_GetContent.restype = c_void_p

def pdfcontent_group_getcontent(group):
    return _lib.PdfTools_ToolboxPdfContent_Group_GetContent(group)
_lib.PdfTools_ToolboxPdfContent_Group_GetIsolated.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Group_GetIsolated.restype = c_bool

def pdfcontent_group_getisolated(group):
    return _lib.PdfTools_ToolboxPdfContent_Group_GetIsolated(group)
_lib.PdfTools_ToolboxPdfContent_Group_SetIsolated.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfContent_Group_SetIsolated.restype = c_bool

def pdfcontent_group_setisolated(group, val):
    return _lib.PdfTools_ToolboxPdfContent_Group_SetIsolated(group, val)
_lib.PdfTools_ToolboxPdfContent_Group_GetKnockout.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Group_GetKnockout.restype = c_bool

def pdfcontent_group_getknockout(group):
    return _lib.PdfTools_ToolboxPdfContent_Group_GetKnockout(group)
_lib.PdfTools_ToolboxPdfContent_Group_SetKnockout.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfContent_Group_SetKnockout.restype = c_bool

def pdfcontent_group_setknockout(group, val):
    return _lib.PdfTools_ToolboxPdfContent_Group_SetKnockout(group, val)


_lib.PdfTools_ToolboxPdfContent_ColorSpace_CreateProcessColorSpace.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfContent_ColorSpace_CreateProcessColorSpace.restype = c_void_p

def pdfcontent_colorspace_createprocesscolorspace(target_document, type):
    return _lib.PdfTools_ToolboxPdfContent_ColorSpace_CreateProcessColorSpace(target_document, type)
_lib.PdfTools_ToolboxPdfContent_ColorSpace_Copy.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfContent_ColorSpace_Copy.restype = c_void_p

def pdfcontent_colorspace_copy(target_document, color_space):
    return _lib.PdfTools_ToolboxPdfContent_ColorSpace_Copy(target_document, color_space)

_lib.PdfTools_ToolboxPdfContent_ColorSpace_GetComponentCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_ColorSpace_GetComponentCount.restype = c_int

def pdfcontent_colorspace_getcomponentcount(color_space):
    return _lib.PdfTools_ToolboxPdfContent_ColorSpace_GetComponentCount(color_space)

_lib.PdfTools_ToolboxPdfContent_ColorSpace_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_ColorSpace_GetType.restype = c_int

def pdfcontent_colorspace_gettype(object):
    return _lib.PdfTools_ToolboxPdfContent_ColorSpace_GetType(object)

_lib.PdfTools_ToolboxPdfContent_IccBasedColorSpace_Create.argtypes = [c_void_p, POINTER(StreamDescriptor)]
_lib.PdfTools_ToolboxPdfContent_IccBasedColorSpace_Create.restype = c_void_p

def pdfcontent_iccbasedcolorspace_create(target_document, profile):
    return _lib.PdfTools_ToolboxPdfContent_IccBasedColorSpace_Create(target_document, profile)
_lib.PdfTools_ToolboxPdfContent_IccBasedColorSpace_Copy.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfContent_IccBasedColorSpace_Copy.restype = c_void_p

def pdfcontent_iccbasedcolorspace_copy(target_document, color_space):
    return _lib.PdfTools_ToolboxPdfContent_IccBasedColorSpace_Copy(target_document, color_space)


_lib.PdfTools_ToolboxPdfContent_Subpath_GetCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Subpath_GetCount.restype = c_int

def pdfcontent_subpath_getcount(subpath):
    return _lib.PdfTools_ToolboxPdfContent_Subpath_GetCount(subpath)
_lib.PdfTools_ToolboxPdfContent_Subpath_Get.argtypes = [c_void_p, c_int, POINTER(PdfContentPathSegment)]
_lib.PdfTools_ToolboxPdfContent_Subpath_Get.restype = c_bool

def pdfcontent_subpath_get(subpath, i_index, ret_val):
    return _lib.PdfTools_ToolboxPdfContent_Subpath_Get(subpath, i_index, byref(ret_val))

_lib.PdfTools_ToolboxPdfContent_Subpath_GetStartPoint.argtypes = [c_void_p, POINTER(GeomRealPoint)]
_lib.PdfTools_ToolboxPdfContent_Subpath_GetStartPoint.restype = c_bool

def pdfcontent_subpath_getstartpoint(subpath, ret_val):
    return _lib.PdfTools_ToolboxPdfContent_Subpath_GetStartPoint(subpath, byref(ret_val))
_lib.PdfTools_ToolboxPdfContent_Subpath_IsClosed.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Subpath_IsClosed.restype = c_bool

def pdfcontent_subpath_isclosed(subpath):
    return _lib.PdfTools_ToolboxPdfContent_Subpath_IsClosed(subpath)


_lib.PdfTools_ToolboxPdfContent_Path_GetIterator.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Path_GetIterator.restype = c_void_p

def pdfcontent_path_getiterator(path):
    return _lib.PdfTools_ToolboxPdfContent_Path_GetIterator(path)

_lib.PdfTools_ToolboxPdfContent_Path_New.argtypes = []
_lib.PdfTools_ToolboxPdfContent_Path_New.restype = c_void_p

def pdfcontent_path_new():
    return _lib.PdfTools_ToolboxPdfContent_Path_New()


_lib.PdfTools_ToolboxPdfContent_ContentGenerator_Save.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_ContentGenerator_Save.restype = c_bool

def pdfcontent_contentgenerator_save(content_generator):
    return _lib.PdfTools_ToolboxPdfContent_ContentGenerator_Save(content_generator)

_lib.PdfTools_ToolboxPdfContent_ContentGenerator_Restore.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_ContentGenerator_Restore.restype = c_bool

def pdfcontent_contentgenerator_restore(content_generator):
    return _lib.PdfTools_ToolboxPdfContent_ContentGenerator_Restore(content_generator)

_lib.PdfTools_ToolboxPdfContent_ContentGenerator_Transform.argtypes = [c_void_p, POINTER(GeomRealAffineTransform)]
_lib.PdfTools_ToolboxPdfContent_ContentGenerator_Transform.restype = c_bool

def pdfcontent_contentgenerator_transform(content_generator, transform):
    return _lib.PdfTools_ToolboxPdfContent_ContentGenerator_Transform(content_generator, transform)

_lib.PdfTools_ToolboxPdfContent_ContentGenerator_PaintImage.argtypes = [c_void_p, c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdfContent_ContentGenerator_PaintImage.restype = c_bool

def pdfcontent_contentgenerator_paintimage(content_generator, image, target_rect):
    return _lib.PdfTools_ToolboxPdfContent_ContentGenerator_PaintImage(content_generator, image, target_rect)

_lib.PdfTools_ToolboxPdfContent_ContentGenerator_PaintImageMask.argtypes = [c_void_p, c_void_p, POINTER(GeomRealRectangle), c_void_p]
_lib.PdfTools_ToolboxPdfContent_ContentGenerator_PaintImageMask.restype = c_bool

def pdfcontent_contentgenerator_paintimagemask(content_generator, image_mask, target_rect, paint):
    return _lib.PdfTools_ToolboxPdfContent_ContentGenerator_PaintImageMask(content_generator, image_mask, target_rect, paint)

_lib.PdfTools_ToolboxPdfContent_ContentGenerator_PaintPath.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfContent_ContentGenerator_PaintPath.restype = c_bool

def pdfcontent_contentgenerator_paintpath(content_generator, path, fill, stroke):
    return _lib.PdfTools_ToolboxPdfContent_ContentGenerator_PaintPath(content_generator, path, fill, stroke)

_lib.PdfTools_ToolboxPdfContent_ContentGenerator_PaintText.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfContent_ContentGenerator_PaintText.restype = c_bool

def pdfcontent_contentgenerator_painttext(content_generator, text):
    return _lib.PdfTools_ToolboxPdfContent_ContentGenerator_PaintText(content_generator, text)

_lib.PdfTools_ToolboxPdfContent_ContentGenerator_ClipWithPath.argtypes = [c_void_p, c_void_p, c_int]
_lib.PdfTools_ToolboxPdfContent_ContentGenerator_ClipWithPath.restype = c_bool

def pdfcontent_contentgenerator_clipwithpath(content_generator, path, inside_rule):
    return _lib.PdfTools_ToolboxPdfContent_ContentGenerator_ClipWithPath(content_generator, path, inside_rule)

_lib.PdfTools_ToolboxPdfContent_ContentGenerator_ClipWithText.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfContent_ContentGenerator_ClipWithText.restype = c_bool

def pdfcontent_contentgenerator_clipwithtext(content_generator, text):
    return _lib.PdfTools_ToolboxPdfContent_ContentGenerator_ClipWithText(content_generator, text)

_lib.PdfTools_ToolboxPdfContent_ContentGenerator_PaintGroup.argtypes = [c_void_p, c_void_p, POINTER(GeomRealRectangle), c_void_p]
_lib.PdfTools_ToolboxPdfContent_ContentGenerator_PaintGroup.restype = c_bool

def pdfcontent_contentgenerator_paintgroup(content_generator, group, target_rect, transparency):
    return _lib.PdfTools_ToolboxPdfContent_ContentGenerator_PaintGroup(content_generator, group, target_rect, transparency)

_lib.PdfTools_ToolboxPdfContent_ContentGenerator_AppendContentElement.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfContent_ContentGenerator_AppendContentElement.restype = c_bool

def pdfcontent_contentgenerator_appendcontentelement(content_generator, content_element):
    return _lib.PdfTools_ToolboxPdfContent_ContentGenerator_AppendContentElement(content_generator, content_element)


_lib.PdfTools_ToolboxPdfContent_ContentGenerator_New.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfContent_ContentGenerator_New.restype = c_void_p

def pdfcontent_contentgenerator_new(content, prepend):
    return _lib.PdfTools_ToolboxPdfContent_ContentGenerator_New(content, prepend)

_lib.PdfTools_ToolboxPdfContent_ContentGenerator_Close.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_ContentGenerator_Close.restype = c_bool

def pdfcontent_contentgenerator_close(object):
    return _lib.PdfTools_ToolboxPdfContent_ContentGenerator_Close(object)


_lib.PdfTools_ToolboxPdfContent_PathGenerator_MoveTo.argtypes = [c_void_p, POINTER(GeomRealPoint)]
_lib.PdfTools_ToolboxPdfContent_PathGenerator_MoveTo.restype = c_bool

def pdfcontent_pathgenerator_moveto(path_generator, target):
    return _lib.PdfTools_ToolboxPdfContent_PathGenerator_MoveTo(path_generator, target)

_lib.PdfTools_ToolboxPdfContent_PathGenerator_LineTo.argtypes = [c_void_p, POINTER(GeomRealPoint)]
_lib.PdfTools_ToolboxPdfContent_PathGenerator_LineTo.restype = c_bool

def pdfcontent_pathgenerator_lineto(path_generator, target):
    return _lib.PdfTools_ToolboxPdfContent_PathGenerator_LineTo(path_generator, target)

_lib.PdfTools_ToolboxPdfContent_PathGenerator_BezierTo.argtypes = [c_void_p, POINTER(GeomRealPoint), POINTER(GeomRealPoint), POINTER(GeomRealPoint)]
_lib.PdfTools_ToolboxPdfContent_PathGenerator_BezierTo.restype = c_bool

def pdfcontent_pathgenerator_bezierto(path_generator, control_point1, control_point2, target):
    return _lib.PdfTools_ToolboxPdfContent_PathGenerator_BezierTo(path_generator, control_point1, control_point2, target)

_lib.PdfTools_ToolboxPdfContent_PathGenerator_CloseSubpath.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_PathGenerator_CloseSubpath.restype = c_bool

def pdfcontent_pathgenerator_closesubpath(path_generator):
    return _lib.PdfTools_ToolboxPdfContent_PathGenerator_CloseSubpath(path_generator)

_lib.PdfTools_ToolboxPdfContent_PathGenerator_AddRectangle.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdfContent_PathGenerator_AddRectangle.restype = c_bool

def pdfcontent_pathgenerator_addrectangle(path_generator, rectangle):
    return _lib.PdfTools_ToolboxPdfContent_PathGenerator_AddRectangle(path_generator, rectangle)

_lib.PdfTools_ToolboxPdfContent_PathGenerator_AddCircle.argtypes = [c_void_p, POINTER(GeomRealPoint), c_double]
_lib.PdfTools_ToolboxPdfContent_PathGenerator_AddCircle.restype = c_bool

def pdfcontent_pathgenerator_addcircle(path_generator, center, radius):
    return _lib.PdfTools_ToolboxPdfContent_PathGenerator_AddCircle(path_generator, center, radius)

_lib.PdfTools_ToolboxPdfContent_PathGenerator_AddEllipse.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdfContent_PathGenerator_AddEllipse.restype = c_bool

def pdfcontent_pathgenerator_addellipse(path_generator, rectangle):
    return _lib.PdfTools_ToolboxPdfContent_PathGenerator_AddEllipse(path_generator, rectangle)

_lib.PdfTools_ToolboxPdfContent_PathGenerator_AddArc.argtypes = [c_void_p, POINTER(GeomRealRectangle), c_double, c_double]
_lib.PdfTools_ToolboxPdfContent_PathGenerator_AddArc.restype = c_bool

def pdfcontent_pathgenerator_addarc(path_generator, rectangle, alpha1, alpha2):
    return _lib.PdfTools_ToolboxPdfContent_PathGenerator_AddArc(path_generator, rectangle, alpha1, alpha2)

_lib.PdfTools_ToolboxPdfContent_PathGenerator_AddPie.argtypes = [c_void_p, POINTER(GeomRealRectangle), c_double, c_double]
_lib.PdfTools_ToolboxPdfContent_PathGenerator_AddPie.restype = c_bool

def pdfcontent_pathgenerator_addpie(path_generator, rectangle, alpha1, alpha2):
    return _lib.PdfTools_ToolboxPdfContent_PathGenerator_AddPie(path_generator, rectangle, alpha1, alpha2)


_lib.PdfTools_ToolboxPdfContent_PathGenerator_New.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_PathGenerator_New.restype = c_void_p

def pdfcontent_pathgenerator_new(path):
    return _lib.PdfTools_ToolboxPdfContent_PathGenerator_New(path)

_lib.PdfTools_ToolboxPdfContent_PathGenerator_Close.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_PathGenerator_Close.restype = c_bool

def pdfcontent_pathgenerator_close(object):
    return _lib.PdfTools_ToolboxPdfContent_PathGenerator_Close(object)


_lib.PdfTools_ToolboxPdfContent_TextGenerator_GetWidthW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfContent_TextGenerator_GetWidthW.restype = c_double

def pdfcontent_textgenerator_getwidth(text_generator, text):
    return _lib.PdfTools_ToolboxPdfContent_TextGenerator_GetWidthW(text_generator, string_to_utf16(text))
_lib.PdfTools_ToolboxPdfContent_TextGenerator_ShowW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfContent_TextGenerator_ShowW.restype = c_bool

def pdfcontent_textgenerator_show(text_generator, text):
    return _lib.PdfTools_ToolboxPdfContent_TextGenerator_ShowW(text_generator, string_to_utf16(text))

_lib.PdfTools_ToolboxPdfContent_TextGenerator_ShowLineW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfContent_TextGenerator_ShowLineW.restype = c_bool

def pdfcontent_textgenerator_showline(text_generator, text):
    return _lib.PdfTools_ToolboxPdfContent_TextGenerator_ShowLineW(text_generator, string_to_utf16(text))

_lib.PdfTools_ToolboxPdfContent_TextGenerator_MoveTo.argtypes = [c_void_p, POINTER(GeomRealPoint)]
_lib.PdfTools_ToolboxPdfContent_TextGenerator_MoveTo.restype = c_bool

def pdfcontent_textgenerator_moveto(text_generator, target):
    return _lib.PdfTools_ToolboxPdfContent_TextGenerator_MoveTo(text_generator, target)


_lib.PdfTools_ToolboxPdfContent_TextGenerator_New.argtypes = [c_void_p, c_void_p, c_double, POINTER(GeomRealPoint)]
_lib.PdfTools_ToolboxPdfContent_TextGenerator_New.restype = c_void_p

def pdfcontent_textgenerator_new(text, font, font_size, location):
    return _lib.PdfTools_ToolboxPdfContent_TextGenerator_New(text, font, font_size, location)

_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetFill.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetFill.restype = c_bool

def pdfcontent_textgenerator_setfill(text_generator, val):
    return _lib.PdfTools_ToolboxPdfContent_TextGenerator_SetFill(text_generator, val)
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetStroke.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetStroke.restype = c_bool

def pdfcontent_textgenerator_setstroke(text_generator, val):
    return _lib.PdfTools_ToolboxPdfContent_TextGenerator_SetStroke(text_generator, val)
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetFont.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetFont.restype = c_bool

def pdfcontent_textgenerator_setfont(text_generator, val):
    return _lib.PdfTools_ToolboxPdfContent_TextGenerator_SetFont(text_generator, val)
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetFontSize.argtypes = [c_void_p, c_double]
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetFontSize.restype = c_bool

def pdfcontent_textgenerator_setfontsize(text_generator, val):
    return _lib.PdfTools_ToolboxPdfContent_TextGenerator_SetFontSize(text_generator, val)
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetCharacterSpacing.argtypes = [c_void_p, c_double]
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetCharacterSpacing.restype = c_bool

def pdfcontent_textgenerator_setcharacterspacing(text_generator, val):
    return _lib.PdfTools_ToolboxPdfContent_TextGenerator_SetCharacterSpacing(text_generator, val)
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetWordSpacing.argtypes = [c_void_p, c_double]
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetWordSpacing.restype = c_bool

def pdfcontent_textgenerator_setwordspacing(text_generator, val):
    return _lib.PdfTools_ToolboxPdfContent_TextGenerator_SetWordSpacing(text_generator, val)
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetHorizontalScaling.argtypes = [c_void_p, c_double]
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetHorizontalScaling.restype = c_bool

def pdfcontent_textgenerator_sethorizontalscaling(text_generator, val):
    return _lib.PdfTools_ToolboxPdfContent_TextGenerator_SetHorizontalScaling(text_generator, val)
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetLeading.argtypes = [c_void_p, c_double]
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetLeading.restype = c_bool

def pdfcontent_textgenerator_setleading(text_generator, val):
    return _lib.PdfTools_ToolboxPdfContent_TextGenerator_SetLeading(text_generator, val)
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetRise.argtypes = [c_void_p, c_double]
_lib.PdfTools_ToolboxPdfContent_TextGenerator_SetRise.restype = c_bool

def pdfcontent_textgenerator_setrise(text_generator, val):
    return _lib.PdfTools_ToolboxPdfContent_TextGenerator_SetRise(text_generator, val)

_lib.PdfTools_ToolboxPdfContent_TextGenerator_Close.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_TextGenerator_Close.restype = c_bool

def pdfcontent_textgenerator_close(object):
    return _lib.PdfTools_ToolboxPdfContent_TextGenerator_Close(object)


_lib.PdfTools_ToolboxPdfContent_Paint_Create.argtypes = [c_void_p, c_void_p, POINTER(c_double), c_size_t, c_void_p]
_lib.PdfTools_ToolboxPdfContent_Paint_Create.restype = c_void_p

def pdfcontent_paint_create(target_document, color_space, color, color_buffer, transparency):
    return _lib.PdfTools_ToolboxPdfContent_Paint_Create(target_document, color_space, color, color_buffer, transparency)

_lib.PdfTools_ToolboxPdfContent_Paint_GetColorSpace.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Paint_GetColorSpace.restype = c_void_p

def pdfcontent_paint_getcolorspace(paint):
    return _lib.PdfTools_ToolboxPdfContent_Paint_GetColorSpace(paint)
_lib.PdfTools_ToolboxPdfContent_Paint_GetColor.argtypes = [c_void_p, POINTER(c_double), c_size_t]
_lib.PdfTools_ToolboxPdfContent_Paint_GetColor.restype = c_size_t

def pdfcontent_paint_getcolor(paint, ret_val, ret_val_buffer):
    return _lib.PdfTools_ToolboxPdfContent_Paint_GetColor(paint, ret_val, ret_val_buffer)
_lib.PdfTools_ToolboxPdfContent_Paint_GetTransparency.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Paint_GetTransparency.restype = c_void_p

def pdfcontent_paint_gettransparency(paint):
    return _lib.PdfTools_ToolboxPdfContent_Paint_GetTransparency(paint)


_lib.PdfTools_ToolboxPdfContent_Glyph_GetTextW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfContent_Glyph_GetTextW.restype = c_size_t

def pdfcontent_glyph_gettext(glyph):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfContent_Glyph_GetTextW(glyph, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfContent_Glyph_GetTextW(glyph, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfContent_Glyph_GetPosition.argtypes = [c_void_p, POINTER(GeomRealPoint)]
_lib.PdfTools_ToolboxPdfContent_Glyph_GetPosition.restype = c_bool

def pdfcontent_glyph_getposition(glyph, ret_val):
    return _lib.PdfTools_ToolboxPdfContent_Glyph_GetPosition(glyph, byref(ret_val))
_lib.PdfTools_ToolboxPdfContent_Glyph_GetWidth.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Glyph_GetWidth.restype = c_double

def pdfcontent_glyph_getwidth(glyph):
    return _lib.PdfTools_ToolboxPdfContent_Glyph_GetWidth(glyph)


_lib.PdfTools_ToolboxPdfContent_TextFragment_GetCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetCount.restype = c_int

def pdfcontent_textfragment_getcount(text_fragment):
    return _lib.PdfTools_ToolboxPdfContent_TextFragment_GetCount(text_fragment)
_lib.PdfTools_ToolboxPdfContent_TextFragment_Get.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfContent_TextFragment_Get.restype = c_void_p

def pdfcontent_textfragment_get(text_fragment, i_index):
    return _lib.PdfTools_ToolboxPdfContent_TextFragment_Get(text_fragment, i_index)
_lib.PdfTools_ToolboxPdfContent_TextFragment_Remove.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfContent_TextFragment_Remove.restype = c_bool

def pdfcontent_textfragment_remove(text_fragment, index):
    return _lib.PdfTools_ToolboxPdfContent_TextFragment_Remove(text_fragment, index)


_lib.PdfTools_ToolboxPdfContent_TextFragment_GetBoundingBox.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetBoundingBox.restype = c_bool

def pdfcontent_textfragment_getboundingbox(text_fragment, ret_val):
    return _lib.PdfTools_ToolboxPdfContent_TextFragment_GetBoundingBox(text_fragment, byref(ret_val))
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetTransform.argtypes = [c_void_p, POINTER(GeomRealAffineTransform)]
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetTransform.restype = c_bool

def pdfcontent_textfragment_gettransform(text_fragment, ret_val):
    return _lib.PdfTools_ToolboxPdfContent_TextFragment_GetTransform(text_fragment, byref(ret_val))
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetTextW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetTextW.restype = c_size_t

def pdfcontent_textfragment_gettext(text_fragment):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfContent_TextFragment_GetTextW(text_fragment, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfContent_TextFragment_GetTextW(text_fragment, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetStroke.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetStroke.restype = c_void_p

def pdfcontent_textfragment_getstroke(text_fragment):
    return _lib.PdfTools_ToolboxPdfContent_TextFragment_GetStroke(text_fragment)
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetFill.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetFill.restype = c_void_p

def pdfcontent_textfragment_getfill(text_fragment):
    return _lib.PdfTools_ToolboxPdfContent_TextFragment_GetFill(text_fragment)
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetFontSize.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetFontSize.restype = c_double

def pdfcontent_textfragment_getfontsize(text_fragment):
    return _lib.PdfTools_ToolboxPdfContent_TextFragment_GetFontSize(text_fragment)
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetCharacterSpacing.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetCharacterSpacing.restype = c_double

def pdfcontent_textfragment_getcharacterspacing(text_fragment):
    return _lib.PdfTools_ToolboxPdfContent_TextFragment_GetCharacterSpacing(text_fragment)
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetWordSpacing.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetWordSpacing.restype = c_double

def pdfcontent_textfragment_getwordspacing(text_fragment):
    return _lib.PdfTools_ToolboxPdfContent_TextFragment_GetWordSpacing(text_fragment)
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetHorizontalScaling.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetHorizontalScaling.restype = c_double

def pdfcontent_textfragment_gethorizontalscaling(text_fragment):
    return _lib.PdfTools_ToolboxPdfContent_TextFragment_GetHorizontalScaling(text_fragment)
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetRise.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetRise.restype = c_double

def pdfcontent_textfragment_getrise(text_fragment):
    return _lib.PdfTools_ToolboxPdfContent_TextFragment_GetRise(text_fragment)
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetWritingMode.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetWritingMode.restype = c_int

def pdfcontent_textfragment_getwritingmode(text_fragment):
    return _lib.PdfTools_ToolboxPdfContent_TextFragment_GetWritingMode(text_fragment)
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetFont.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_TextFragment_GetFont.restype = c_void_p

def pdfcontent_textfragment_getfont(text_fragment):
    return _lib.PdfTools_ToolboxPdfContent_TextFragment_GetFont(text_fragment)


_lib.PdfTools_ToolboxPdfContent_Text_Create.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Text_Create.restype = c_void_p

def pdfcontent_text_create(target_document):
    return _lib.PdfTools_ToolboxPdfContent_Text_Create(target_document)
_lib.PdfTools_ToolboxPdfContent_Text_GetCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Text_GetCount.restype = c_int

def pdfcontent_text_getcount(text):
    return _lib.PdfTools_ToolboxPdfContent_Text_GetCount(text)
_lib.PdfTools_ToolboxPdfContent_Text_Get.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfContent_Text_Get.restype = c_void_p

def pdfcontent_text_get(text, i_index):
    return _lib.PdfTools_ToolboxPdfContent_Text_Get(text, i_index)
_lib.PdfTools_ToolboxPdfContent_Text_Clear.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_Text_Clear.restype = c_bool

def pdfcontent_text_clear(text):
    return _lib.PdfTools_ToolboxPdfContent_Text_Clear(text)

_lib.PdfTools_ToolboxPdfContent_Text_Remove.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfContent_Text_Remove.restype = c_bool

def pdfcontent_text_remove(text, index):
    return _lib.PdfTools_ToolboxPdfContent_Text_Remove(text, index)



_lib.PdfTools_ToolboxPdfContent_ContentElement_Copy.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfContent_ContentElement_Copy.restype = c_void_p

def pdfcontent_contentelement_copy(target_document, content_element):
    return _lib.PdfTools_ToolboxPdfContent_ContentElement_Copy(target_document, content_element)

_lib.PdfTools_ToolboxPdfContent_ContentElement_GetBoundingBox.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdfContent_ContentElement_GetBoundingBox.restype = c_bool

def pdfcontent_contentelement_getboundingbox(content_element, ret_val):
    return _lib.PdfTools_ToolboxPdfContent_ContentElement_GetBoundingBox(content_element, byref(ret_val))
_lib.PdfTools_ToolboxPdfContent_ContentElement_GetTransform.argtypes = [c_void_p, POINTER(GeomRealAffineTransform)]
_lib.PdfTools_ToolboxPdfContent_ContentElement_GetTransform.restype = c_bool

def pdfcontent_contentelement_gettransform(content_element, ret_val):
    return _lib.PdfTools_ToolboxPdfContent_ContentElement_GetTransform(content_element, byref(ret_val))
_lib.PdfTools_ToolboxPdfContent_ContentElement_SetTransform.argtypes = [c_void_p, POINTER(GeomRealAffineTransform)]
_lib.PdfTools_ToolboxPdfContent_ContentElement_SetTransform.restype = c_bool

def pdfcontent_contentelement_settransform(content_element, val):
    return _lib.PdfTools_ToolboxPdfContent_ContentElement_SetTransform(content_element, val)

_lib.PdfTools_ToolboxPdfContent_ContentElement_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_ContentElement_GetType.restype = c_int

def pdfcontent_contentelement_gettype(object):
    return _lib.PdfTools_ToolboxPdfContent_ContentElement_GetType(object)

_lib.PdfTools_ToolboxPdfContent_TextElement_GetText.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_TextElement_GetText.restype = c_void_p

def pdfcontent_textelement_gettext(text_element):
    return _lib.PdfTools_ToolboxPdfContent_TextElement_GetText(text_element)


_lib.PdfTools_ToolboxPdfContent_GroupElement_CopyWithoutContent.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfContent_GroupElement_CopyWithoutContent.restype = c_void_p

def pdfcontent_groupelement_copywithoutcontent(target_document, group_element):
    return _lib.PdfTools_ToolboxPdfContent_GroupElement_CopyWithoutContent(target_document, group_element)

_lib.PdfTools_ToolboxPdfContent_GroupElement_GetGroup.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_GroupElement_GetGroup.restype = c_void_p

def pdfcontent_groupelement_getgroup(group_element):
    return _lib.PdfTools_ToolboxPdfContent_GroupElement_GetGroup(group_element)


_lib.PdfTools_ToolboxPdfContent_PathElement_GetAlignmentBox.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdfContent_PathElement_GetAlignmentBox.restype = c_bool

def pdfcontent_pathelement_getalignmentbox(path_element, ret_val):
    return _lib.PdfTools_ToolboxPdfContent_PathElement_GetAlignmentBox(path_element, byref(ret_val))
_lib.PdfTools_ToolboxPdfContent_PathElement_GetPath.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_PathElement_GetPath.restype = c_void_p

def pdfcontent_pathelement_getpath(path_element):
    return _lib.PdfTools_ToolboxPdfContent_PathElement_GetPath(path_element)
_lib.PdfTools_ToolboxPdfContent_PathElement_GetStroke.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_PathElement_GetStroke.restype = c_void_p

def pdfcontent_pathelement_getstroke(path_element):
    return _lib.PdfTools_ToolboxPdfContent_PathElement_GetStroke(path_element)
_lib.PdfTools_ToolboxPdfContent_PathElement_GetFill.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_PathElement_GetFill.restype = c_void_p

def pdfcontent_pathelement_getfill(path_element):
    return _lib.PdfTools_ToolboxPdfContent_PathElement_GetFill(path_element)


_lib.PdfTools_ToolboxPdfContent_ImageElement_GetImage.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_ImageElement_GetImage.restype = c_void_p

def pdfcontent_imageelement_getimage(image_element):
    return _lib.PdfTools_ToolboxPdfContent_ImageElement_GetImage(image_element)


_lib.PdfTools_ToolboxPdfContent_ImageMaskElement_GetImageMask.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_ImageMaskElement_GetImageMask.restype = c_void_p

def pdfcontent_imagemaskelement_getimagemask(image_mask_element):
    return _lib.PdfTools_ToolboxPdfContent_ImageMaskElement_GetImageMask(image_mask_element)
_lib.PdfTools_ToolboxPdfContent_ImageMaskElement_GetPaint.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_ImageMaskElement_GetPaint.restype = c_void_p

def pdfcontent_imagemaskelement_getpaint(image_mask_element):
    return _lib.PdfTools_ToolboxPdfContent_ImageMaskElement_GetPaint(image_mask_element)


_lib.PdfTools_ToolboxPdfContent_ContentExtractor_GetIterator.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_ContentExtractor_GetIterator.restype = c_void_p

def pdfcontent_contentextractor_getiterator(content_extractor):
    return _lib.PdfTools_ToolboxPdfContent_ContentExtractor_GetIterator(content_extractor)

_lib.PdfTools_ToolboxPdfContent_ContentExtractor_New.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_ContentExtractor_New.restype = c_void_p

def pdfcontent_contentextractor_new(content):
    return _lib.PdfTools_ToolboxPdfContent_ContentExtractor_New(content)

_lib.PdfTools_ToolboxPdfContent_ContentExtractor_GetUngrouping.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfContent_ContentExtractor_GetUngrouping.restype = c_int

def pdfcontent_contentextractor_getungrouping(content_extractor):
    return _lib.PdfTools_ToolboxPdfContent_ContentExtractor_GetUngrouping(content_extractor)
_lib.PdfTools_ToolboxPdfContent_ContentExtractor_SetUngrouping.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfContent_ContentExtractor_SetUngrouping.restype = c_bool

def pdfcontent_contentextractor_setungrouping(content_extractor, val):
    return _lib.PdfTools_ToolboxPdfContent_ContentExtractor_SetUngrouping(content_extractor, val)


_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_LookupW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_LookupW.restype = c_void_p

def pdfforms_fieldnodemap_lookup(field_node_map, identifier_path):
    return _lib.PdfTools_ToolboxPdfForms_FieldNodeMap_LookupW(field_node_map, string_to_utf16(identifier_path))
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetCount.restype = c_int

def pdfforms_fieldnodemap_getcount(field_node_map):
    return _lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetCount(field_node_map)
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetSize.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetSize.restype = c_int

def pdfforms_fieldnodemap_getsize(field_node_map):
    return _lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetSize(field_node_map)
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetBegin.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetBegin.restype = c_int

def pdfforms_fieldnodemap_getbegin(field_node_map):
    return _lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetBegin(field_node_map)
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetEnd.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetEnd.restype = c_int

def pdfforms_fieldnodemap_getend(field_node_map):
    return _lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetEnd(field_node_map)
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetNext.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetNext.restype = c_int

def pdfforms_fieldnodemap_getnext(field_node_map, it):
    return _lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetNext(field_node_map, it)
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetW.restype = c_int

def pdfforms_fieldnodemap_get(field_node_map, key):
    return _lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetW(field_node_map, string_to_utf16(key))
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetKeyW.argtypes = [c_void_p, c_int, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetKeyW.restype = c_size_t

def pdfforms_fieldnodemap_getkey(field_node_map, it):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetKeyW(field_node_map, it, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetKeyW(field_node_map, it, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetValue.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetValue.restype = c_void_p

def pdfforms_fieldnodemap_getvalue(field_node_map, it):
    return _lib.PdfTools_ToolboxPdfForms_FieldNodeMap_GetValue(field_node_map, it)
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_SetW.argtypes = [c_void_p, c_wchar_p, c_void_p]
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_SetW.restype = c_bool

def pdfforms_fieldnodemap_set(field_node_map, key, value):
    return _lib.PdfTools_ToolboxPdfForms_FieldNodeMap_SetW(field_node_map, string_to_utf16(key), value)

_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_SetValue.argtypes = [c_void_p, c_int, c_void_p]
_lib.PdfTools_ToolboxPdfForms_FieldNodeMap_SetValue.restype = c_bool

def pdfforms_fieldnodemap_setvalue(field_node_map, it, value):
    return _lib.PdfTools_ToolboxPdfForms_FieldNodeMap_SetValue(field_node_map, it, value)



_lib.PdfTools_ToolboxPdfForms_WidgetList_GetCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_WidgetList_GetCount.restype = c_int

def pdfforms_widgetlist_getcount(widget_list):
    return _lib.PdfTools_ToolboxPdfForms_WidgetList_GetCount(widget_list)
_lib.PdfTools_ToolboxPdfForms_WidgetList_Get.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfForms_WidgetList_Get.restype = c_void_p

def pdfforms_widgetlist_get(widget_list, i_index):
    return _lib.PdfTools_ToolboxPdfForms_WidgetList_Get(widget_list, i_index)
_lib.PdfTools_ToolboxPdfForms_WidgetList_Add.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfForms_WidgetList_Add.restype = c_bool

def pdfforms_widgetlist_add(widget_list, widget):
    return _lib.PdfTools_ToolboxPdfForms_WidgetList_Add(widget_list, widget)


_lib.PdfTools_ToolboxPdfForms_SignatureFieldList_GetCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_SignatureFieldList_GetCount.restype = c_int

def pdfforms_signaturefieldlist_getcount(signature_field_list):
    return _lib.PdfTools_ToolboxPdfForms_SignatureFieldList_GetCount(signature_field_list)
_lib.PdfTools_ToolboxPdfForms_SignatureFieldList_Get.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfForms_SignatureFieldList_Get.restype = c_void_p

def pdfforms_signaturefieldlist_get(signature_field_list, i_index):
    return _lib.PdfTools_ToolboxPdfForms_SignatureFieldList_Get(signature_field_list, i_index)


_lib.PdfTools_ToolboxPdfForms_Widget_GetBoundingBox.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdfForms_Widget_GetBoundingBox.restype = c_bool

def pdfforms_widget_getboundingbox(widget, ret_val):
    return _lib.PdfTools_ToolboxPdfForms_Widget_GetBoundingBox(widget, byref(ret_val))
_lib.PdfTools_ToolboxPdfForms_Widget_GetHidden.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_Widget_GetHidden.restype = c_bool

def pdfforms_widget_gethidden(widget):
    return _lib.PdfTools_ToolboxPdfForms_Widget_GetHidden(widget)
_lib.PdfTools_ToolboxPdfForms_Widget_GetNoPrint.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_Widget_GetNoPrint.restype = c_bool

def pdfforms_widget_getnoprint(widget):
    return _lib.PdfTools_ToolboxPdfForms_Widget_GetNoPrint(widget)


_lib.PdfTools_ToolboxPdfForms_FieldNode_Copy.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfForms_FieldNode_Copy.restype = c_void_p

def pdfforms_fieldnode_copy(target_document, field_node):
    return _lib.PdfTools_ToolboxPdfForms_FieldNode_Copy(target_document, field_node)

_lib.PdfTools_ToolboxPdfForms_FieldNode_GetDisplayNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfForms_FieldNode_GetDisplayNameW.restype = c_size_t

def pdfforms_fieldnode_getdisplayname(field_node):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfForms_FieldNode_GetDisplayNameW(field_node, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfForms_FieldNode_GetDisplayNameW(field_node, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfForms_FieldNode_SetDisplayNameW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfForms_FieldNode_SetDisplayNameW.restype = c_bool

def pdfforms_fieldnode_setdisplayname(field_node, val):
    return _lib.PdfTools_ToolboxPdfForms_FieldNode_SetDisplayNameW(field_node, string_to_utf16(val))
_lib.PdfTools_ToolboxPdfForms_FieldNode_GetExportNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfForms_FieldNode_GetExportNameW.restype = c_size_t

def pdfforms_fieldnode_getexportname(field_node):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfForms_FieldNode_GetExportNameW(field_node, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfForms_FieldNode_GetExportNameW(field_node, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfForms_FieldNode_SetExportNameW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfForms_FieldNode_SetExportNameW.restype = c_bool

def pdfforms_fieldnode_setexportname(field_node, val):
    return _lib.PdfTools_ToolboxPdfForms_FieldNode_SetExportNameW(field_node, string_to_utf16(val))

_lib.PdfTools_ToolboxPdfForms_FieldNode_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_FieldNode_GetType.restype = c_int

def pdfforms_fieldnode_gettype(object):
    return _lib.PdfTools_ToolboxPdfForms_FieldNode_GetType(object)

_lib.PdfTools_ToolboxPdfForms_SubForm_Create.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_SubForm_Create.restype = c_void_p

def pdfforms_subform_create(target_document):
    return _lib.PdfTools_ToolboxPdfForms_SubForm_Create(target_document)

_lib.PdfTools_ToolboxPdfForms_SubForm_GetChildren.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_SubForm_GetChildren.restype = c_void_p

def pdfforms_subform_getchildren(sub_form):
    return _lib.PdfTools_ToolboxPdfForms_SubForm_GetChildren(sub_form)


_lib.PdfTools_ToolboxPdfForms_Field_AddNewWidget.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdfForms_Field_AddNewWidget.restype = c_void_p

def pdfforms_field_addnewwidget(field, bounding_box):
    return _lib.PdfTools_ToolboxPdfForms_Field_AddNewWidget(field, bounding_box)

_lib.PdfTools_ToolboxPdfForms_Field_GetWidgets.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_Field_GetWidgets.restype = c_void_p

def pdfforms_field_getwidgets(field):
    return _lib.PdfTools_ToolboxPdfForms_Field_GetWidgets(field)
_lib.PdfTools_ToolboxPdfForms_Field_GetReadOnly.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_Field_GetReadOnly.restype = c_bool

def pdfforms_field_getreadonly(field):
    return _lib.PdfTools_ToolboxPdfForms_Field_GetReadOnly(field)
_lib.PdfTools_ToolboxPdfForms_Field_SetReadOnly.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfForms_Field_SetReadOnly.restype = c_bool

def pdfforms_field_setreadonly(field, val):
    return _lib.PdfTools_ToolboxPdfForms_Field_SetReadOnly(field, val)
_lib.PdfTools_ToolboxPdfForms_Field_GetRequired.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_Field_GetRequired.restype = c_bool

def pdfforms_field_getrequired(field):
    return _lib.PdfTools_ToolboxPdfForms_Field_GetRequired(field)
_lib.PdfTools_ToolboxPdfForms_Field_SetRequired.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfForms_Field_SetRequired.restype = c_bool

def pdfforms_field_setrequired(field, val):
    return _lib.PdfTools_ToolboxPdfForms_Field_SetRequired(field, val)
_lib.PdfTools_ToolboxPdfForms_Field_GetDoNotExport.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_Field_GetDoNotExport.restype = c_bool

def pdfforms_field_getdonotexport(field):
    return _lib.PdfTools_ToolboxPdfForms_Field_GetDoNotExport(field)
_lib.PdfTools_ToolboxPdfForms_Field_SetDoNotExport.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfForms_Field_SetDoNotExport.restype = c_bool

def pdfforms_field_setdonotexport(field, val):
    return _lib.PdfTools_ToolboxPdfForms_Field_SetDoNotExport(field, val)

_lib.PdfTools_ToolboxPdfForms_Field_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_Field_GetType.restype = c_int

def pdfforms_field_gettype(object):
    return _lib.PdfTools_ToolboxPdfForms_Field_GetType(object)

_lib.PdfTools_ToolboxPdfForms_TextField_GetTextW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfForms_TextField_GetTextW.restype = c_size_t

def pdfforms_textfield_gettext(text_field):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfForms_TextField_GetTextW(text_field, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfForms_TextField_GetTextW(text_field, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfForms_TextField_SetTextW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfForms_TextField_SetTextW.restype = c_bool

def pdfforms_textfield_settext(text_field, val):
    return _lib.PdfTools_ToolboxPdfForms_TextField_SetTextW(text_field, string_to_utf16(val))
_lib.PdfTools_ToolboxPdfForms_TextField_GetAlignment.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_TextField_GetAlignment.restype = c_int

def pdfforms_textfield_getalignment(text_field):
    return _lib.PdfTools_ToolboxPdfForms_TextField_GetAlignment(text_field)
_lib.PdfTools_ToolboxPdfForms_TextField_SetAlignment.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfForms_TextField_SetAlignment.restype = c_bool

def pdfforms_textfield_setalignment(text_field, val):
    return _lib.PdfTools_ToolboxPdfForms_TextField_SetAlignment(text_field, val)
_lib.PdfTools_ToolboxPdfForms_TextField_GetFontSize.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfTools_ToolboxPdfForms_TextField_GetFontSize.restype = c_bool

def pdfforms_textfield_getfontsize(text_field, ret_val):
    return _lib.PdfTools_ToolboxPdfForms_TextField_GetFontSize(text_field, byref(ret_val))
_lib.PdfTools_ToolboxPdfForms_TextField_SetFontSize.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfTools_ToolboxPdfForms_TextField_SetFontSize.restype = c_bool

def pdfforms_textfield_setfontsize(text_field, val):
    return _lib.PdfTools_ToolboxPdfForms_TextField_SetFontSize(text_field, byref(c_double(val)) if val is not None else None)

_lib.PdfTools_ToolboxPdfForms_TextField_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_TextField_GetType.restype = c_int

def pdfforms_textfield_gettype(object):
    return _lib.PdfTools_ToolboxPdfForms_TextField_GetType(object)

_lib.PdfTools_ToolboxPdfForms_GeneralTextField_Create.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_Create.restype = c_void_p

def pdfforms_generaltextfield_create(target_document):
    return _lib.PdfTools_ToolboxPdfForms_GeneralTextField_Create(target_document)

_lib.PdfTools_ToolboxPdfForms_GeneralTextField_GetMaxLength.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_GetMaxLength.restype = c_bool

def pdfforms_generaltextfield_getmaxlength(general_text_field, ret_val):
    return _lib.PdfTools_ToolboxPdfForms_GeneralTextField_GetMaxLength(general_text_field, byref(ret_val))
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_SetMaxLength.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_SetMaxLength.restype = c_bool

def pdfforms_generaltextfield_setmaxlength(general_text_field, val):
    return _lib.PdfTools_ToolboxPdfForms_GeneralTextField_SetMaxLength(general_text_field, byref(c_int(val)) if val is not None else None)
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_GetMultiline.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_GetMultiline.restype = c_bool

def pdfforms_generaltextfield_getmultiline(general_text_field):
    return _lib.PdfTools_ToolboxPdfForms_GeneralTextField_GetMultiline(general_text_field)
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_SetMultiline.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_SetMultiline.restype = c_bool

def pdfforms_generaltextfield_setmultiline(general_text_field, val):
    return _lib.PdfTools_ToolboxPdfForms_GeneralTextField_SetMultiline(general_text_field, val)
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_GetPassword.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_GetPassword.restype = c_bool

def pdfforms_generaltextfield_getpassword(general_text_field):
    return _lib.PdfTools_ToolboxPdfForms_GeneralTextField_GetPassword(general_text_field)
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_SetPassword.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_SetPassword.restype = c_bool

def pdfforms_generaltextfield_setpassword(general_text_field, val):
    return _lib.PdfTools_ToolboxPdfForms_GeneralTextField_SetPassword(general_text_field, val)
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_GetDoNotSpellCheck.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_GetDoNotSpellCheck.restype = c_bool

def pdfforms_generaltextfield_getdonotspellcheck(general_text_field):
    return _lib.PdfTools_ToolboxPdfForms_GeneralTextField_GetDoNotSpellCheck(general_text_field)
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_SetDoNotSpellCheck.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_SetDoNotSpellCheck.restype = c_bool

def pdfforms_generaltextfield_setdonotspellcheck(general_text_field, val):
    return _lib.PdfTools_ToolboxPdfForms_GeneralTextField_SetDoNotSpellCheck(general_text_field, val)
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_GetDoNotScroll.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_GetDoNotScroll.restype = c_bool

def pdfforms_generaltextfield_getdonotscroll(general_text_field):
    return _lib.PdfTools_ToolboxPdfForms_GeneralTextField_GetDoNotScroll(general_text_field)
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_SetDoNotScroll.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfForms_GeneralTextField_SetDoNotScroll.restype = c_bool

def pdfforms_generaltextfield_setdonotscroll(general_text_field, val):
    return _lib.PdfTools_ToolboxPdfForms_GeneralTextField_SetDoNotScroll(general_text_field, val)


_lib.PdfTools_ToolboxPdfForms_CombTextField_Create.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfForms_CombTextField_Create.restype = c_void_p

def pdfforms_combtextfield_create(target_document, max_length):
    return _lib.PdfTools_ToolboxPdfForms_CombTextField_Create(target_document, max_length)

_lib.PdfTools_ToolboxPdfForms_CombTextField_GetMaxLength.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_CombTextField_GetMaxLength.restype = c_int

def pdfforms_combtextfield_getmaxlength(comb_text_field):
    return _lib.PdfTools_ToolboxPdfForms_CombTextField_GetMaxLength(comb_text_field)
_lib.PdfTools_ToolboxPdfForms_CombTextField_SetMaxLength.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfForms_CombTextField_SetMaxLength.restype = c_bool

def pdfforms_combtextfield_setmaxlength(comb_text_field, val):
    return _lib.PdfTools_ToolboxPdfForms_CombTextField_SetMaxLength(comb_text_field, val)


_lib.PdfTools_ToolboxPdfForms_CheckBox_Create.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_CheckBox_Create.restype = c_void_p

def pdfforms_checkbox_create(target_document):
    return _lib.PdfTools_ToolboxPdfForms_CheckBox_Create(target_document)

_lib.PdfTools_ToolboxPdfForms_CheckBox_GetCheckedExportNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfForms_CheckBox_GetCheckedExportNameW.restype = c_size_t

def pdfforms_checkbox_getcheckedexportname(check_box):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfForms_CheckBox_GetCheckedExportNameW(check_box, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfForms_CheckBox_GetCheckedExportNameW(check_box, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfForms_CheckBox_GetChecked.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_CheckBox_GetChecked.restype = c_bool

def pdfforms_checkbox_getchecked(check_box):
    return _lib.PdfTools_ToolboxPdfForms_CheckBox_GetChecked(check_box)
_lib.PdfTools_ToolboxPdfForms_CheckBox_SetChecked.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfForms_CheckBox_SetChecked.restype = c_bool

def pdfforms_checkbox_setchecked(check_box, val):
    return _lib.PdfTools_ToolboxPdfForms_CheckBox_SetChecked(check_box, val)


_lib.PdfTools_ToolboxPdfForms_RadioButton_AddNewWidget.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdfForms_RadioButton_AddNewWidget.restype = c_void_p

def pdfforms_radiobutton_addnewwidget(radio_button, bounding_box):
    return _lib.PdfTools_ToolboxPdfForms_RadioButton_AddNewWidget(radio_button, bounding_box)

_lib.PdfTools_ToolboxPdfForms_RadioButton_GetExportNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfForms_RadioButton_GetExportNameW.restype = c_size_t

def pdfforms_radiobutton_getexportname(radio_button):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfForms_RadioButton_GetExportNameW(radio_button, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfForms_RadioButton_GetExportNameW(radio_button, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfForms_RadioButton_GetWidgets.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_RadioButton_GetWidgets.restype = c_void_p

def pdfforms_radiobutton_getwidgets(radio_button):
    return _lib.PdfTools_ToolboxPdfForms_RadioButton_GetWidgets(radio_button)


_lib.PdfTools_ToolboxPdfForms_RadioButtonList_GetCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_RadioButtonList_GetCount.restype = c_int

def pdfforms_radiobuttonlist_getcount(radio_button_list):
    return _lib.PdfTools_ToolboxPdfForms_RadioButtonList_GetCount(radio_button_list)
_lib.PdfTools_ToolboxPdfForms_RadioButtonList_Get.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfForms_RadioButtonList_Get.restype = c_void_p

def pdfforms_radiobuttonlist_get(radio_button_list, i_index):
    return _lib.PdfTools_ToolboxPdfForms_RadioButtonList_Get(radio_button_list, i_index)


_lib.PdfTools_ToolboxPdfForms_RadioButtonGroup_Create.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_RadioButtonGroup_Create.restype = c_void_p

def pdfforms_radiobuttongroup_create(target_document):
    return _lib.PdfTools_ToolboxPdfForms_RadioButtonGroup_Create(target_document)
_lib.PdfTools_ToolboxPdfForms_RadioButtonGroup_AddNewButtonW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfForms_RadioButtonGroup_AddNewButtonW.restype = c_void_p

def pdfforms_radiobuttongroup_addnewbutton(radio_button_group, export_name):
    return _lib.PdfTools_ToolboxPdfForms_RadioButtonGroup_AddNewButtonW(radio_button_group, string_to_utf16(export_name))

_lib.PdfTools_ToolboxPdfForms_RadioButtonGroup_GetButtons.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_RadioButtonGroup_GetButtons.restype = c_void_p

def pdfforms_radiobuttongroup_getbuttons(radio_button_group):
    return _lib.PdfTools_ToolboxPdfForms_RadioButtonGroup_GetButtons(radio_button_group)
_lib.PdfTools_ToolboxPdfForms_RadioButtonGroup_GetChosenButton.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_RadioButtonGroup_GetChosenButton.restype = c_void_p

def pdfforms_radiobuttongroup_getchosenbutton(radio_button_group):
    return _lib.PdfTools_ToolboxPdfForms_RadioButtonGroup_GetChosenButton(radio_button_group)
_lib.PdfTools_ToolboxPdfForms_RadioButtonGroup_SetChosenButton.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfForms_RadioButtonGroup_SetChosenButton.restype = c_bool

def pdfforms_radiobuttongroup_setchosenbutton(radio_button_group, val):
    return _lib.PdfTools_ToolboxPdfForms_RadioButtonGroup_SetChosenButton(radio_button_group, val)


_lib.PdfTools_ToolboxPdfForms_ChoiceItem_GetDisplayNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfForms_ChoiceItem_GetDisplayNameW.restype = c_size_t

def pdfforms_choiceitem_getdisplayname(choice_item):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfForms_ChoiceItem_GetDisplayNameW(choice_item, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfForms_ChoiceItem_GetDisplayNameW(choice_item, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfForms_ChoiceItem_SetDisplayNameW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfForms_ChoiceItem_SetDisplayNameW.restype = c_bool

def pdfforms_choiceitem_setdisplayname(choice_item, val):
    return _lib.PdfTools_ToolboxPdfForms_ChoiceItem_SetDisplayNameW(choice_item, string_to_utf16(val))
_lib.PdfTools_ToolboxPdfForms_ChoiceItem_GetExportNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfForms_ChoiceItem_GetExportNameW.restype = c_size_t

def pdfforms_choiceitem_getexportname(choice_item):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfForms_ChoiceItem_GetExportNameW(choice_item, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfForms_ChoiceItem_GetExportNameW(choice_item, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfForms_ChoiceItem_SetExportNameW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfForms_ChoiceItem_SetExportNameW.restype = c_bool

def pdfforms_choiceitem_setexportname(choice_item, val):
    return _lib.PdfTools_ToolboxPdfForms_ChoiceItem_SetExportNameW(choice_item, string_to_utf16(val))


_lib.PdfTools_ToolboxPdfForms_ChoiceItemList_GetCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_ChoiceItemList_GetCount.restype = c_int

def pdfforms_choiceitemlist_getcount(choice_item_list):
    return _lib.PdfTools_ToolboxPdfForms_ChoiceItemList_GetCount(choice_item_list)
_lib.PdfTools_ToolboxPdfForms_ChoiceItemList_Get.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfForms_ChoiceItemList_Get.restype = c_void_p

def pdfforms_choiceitemlist_get(choice_item_list, i_index):
    return _lib.PdfTools_ToolboxPdfForms_ChoiceItemList_Get(choice_item_list, i_index)
_lib.PdfTools_ToolboxPdfForms_ChoiceItemList_Add.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfForms_ChoiceItemList_Add.restype = c_bool

def pdfforms_choiceitemlist_add(choice_item_list, choice_item):
    return _lib.PdfTools_ToolboxPdfForms_ChoiceItemList_Add(choice_item_list, choice_item)
_lib.PdfTools_ToolboxPdfForms_ChoiceItemList_Clear.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_ChoiceItemList_Clear.restype = c_bool

def pdfforms_choiceitemlist_clear(choice_item_list):
    return _lib.PdfTools_ToolboxPdfForms_ChoiceItemList_Clear(choice_item_list)

_lib.PdfTools_ToolboxPdfForms_ChoiceItemList_Remove.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfForms_ChoiceItemList_Remove.restype = c_bool

def pdfforms_choiceitemlist_remove(choice_item_list, index):
    return _lib.PdfTools_ToolboxPdfForms_ChoiceItemList_Remove(choice_item_list, index)



_lib.PdfTools_ToolboxPdfForms_ChoiceField_AddNewItemW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfForms_ChoiceField_AddNewItemW.restype = c_void_p

def pdfforms_choicefield_addnewitem(choice_field, display_name):
    return _lib.PdfTools_ToolboxPdfForms_ChoiceField_AddNewItemW(choice_field, string_to_utf16(display_name))

_lib.PdfTools_ToolboxPdfForms_ChoiceField_GetItems.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_ChoiceField_GetItems.restype = c_void_p

def pdfforms_choicefield_getitems(choice_field):
    return _lib.PdfTools_ToolboxPdfForms_ChoiceField_GetItems(choice_field)

_lib.PdfTools_ToolboxPdfForms_ChoiceField_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_ChoiceField_GetType.restype = c_int

def pdfforms_choicefield_gettype(object):
    return _lib.PdfTools_ToolboxPdfForms_ChoiceField_GetType(object)

_lib.PdfTools_ToolboxPdfForms_ListBox_Create.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_ListBox_Create.restype = c_void_p

def pdfforms_listbox_create(target_document):
    return _lib.PdfTools_ToolboxPdfForms_ListBox_Create(target_document)

_lib.PdfTools_ToolboxPdfForms_ListBox_GetAllowMultiSelect.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_ListBox_GetAllowMultiSelect.restype = c_bool

def pdfforms_listbox_getallowmultiselect(list_box):
    return _lib.PdfTools_ToolboxPdfForms_ListBox_GetAllowMultiSelect(list_box)
_lib.PdfTools_ToolboxPdfForms_ListBox_SetAllowMultiSelect.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfForms_ListBox_SetAllowMultiSelect.restype = c_bool

def pdfforms_listbox_setallowmultiselect(list_box, val):
    return _lib.PdfTools_ToolboxPdfForms_ListBox_SetAllowMultiSelect(list_box, val)
_lib.PdfTools_ToolboxPdfForms_ListBox_GetChosenItems.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_ListBox_GetChosenItems.restype = c_void_p

def pdfforms_listbox_getchosenitems(list_box):
    return _lib.PdfTools_ToolboxPdfForms_ListBox_GetChosenItems(list_box)


_lib.PdfTools_ToolboxPdfForms_ComboBox_Create.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_ComboBox_Create.restype = c_void_p

def pdfforms_combobox_create(target_document):
    return _lib.PdfTools_ToolboxPdfForms_ComboBox_Create(target_document)

_lib.PdfTools_ToolboxPdfForms_ComboBox_GetCanEdit.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_ComboBox_GetCanEdit.restype = c_bool

def pdfforms_combobox_getcanedit(combo_box):
    return _lib.PdfTools_ToolboxPdfForms_ComboBox_GetCanEdit(combo_box)
_lib.PdfTools_ToolboxPdfForms_ComboBox_SetCanEdit.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfForms_ComboBox_SetCanEdit.restype = c_bool

def pdfforms_combobox_setcanedit(combo_box, val):
    return _lib.PdfTools_ToolboxPdfForms_ComboBox_SetCanEdit(combo_box, val)
_lib.PdfTools_ToolboxPdfForms_ComboBox_GetChosenItem.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_ComboBox_GetChosenItem.restype = c_void_p

def pdfforms_combobox_getchosenitem(combo_box):
    return _lib.PdfTools_ToolboxPdfForms_ComboBox_GetChosenItem(combo_box)
_lib.PdfTools_ToolboxPdfForms_ComboBox_SetChosenItem.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfForms_ComboBox_SetChosenItem.restype = c_bool

def pdfforms_combobox_setchosenitem(combo_box, val):
    return _lib.PdfTools_ToolboxPdfForms_ComboBox_SetChosenItem(combo_box, val)
_lib.PdfTools_ToolboxPdfForms_ComboBox_GetEditableItemNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfForms_ComboBox_GetEditableItemNameW.restype = c_size_t

def pdfforms_combobox_geteditableitemname(combo_box):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfForms_ComboBox_GetEditableItemNameW(combo_box, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfForms_ComboBox_GetEditableItemNameW(combo_box, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfForms_ComboBox_SetEditableItemNameW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfForms_ComboBox_SetEditableItemNameW.restype = c_bool

def pdfforms_combobox_seteditableitemname(combo_box, val):
    return _lib.PdfTools_ToolboxPdfForms_ComboBox_SetEditableItemNameW(combo_box, string_to_utf16(val))


_lib.PdfTools_ToolboxPdfForms_SignatureField_IsVisible.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_SignatureField_IsVisible.restype = c_bool

def pdfforms_signaturefield_isvisible(signature_field):
    return _lib.PdfTools_ToolboxPdfForms_SignatureField_IsVisible(signature_field)

_lib.PdfTools_ToolboxPdfForms_SignatureField_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_SignatureField_GetType.restype = c_int

def pdfforms_signaturefield_gettype(object):
    return _lib.PdfTools_ToolboxPdfForms_SignatureField_GetType(object)

_lib.PdfTools_ToolboxPdfForms_SignedSignatureField_GetNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfForms_SignedSignatureField_GetNameW.restype = c_size_t

def pdfforms_signedsignaturefield_getname(signed_signature_field):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfForms_SignedSignatureField_GetNameW(signed_signature_field, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfForms_SignedSignatureField_GetNameW(signed_signature_field, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfForms_SignedSignatureField_GetDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfTools_ToolboxPdfForms_SignedSignatureField_GetDate.restype = c_bool

def pdfforms_signedsignaturefield_getdate(signed_signature_field, ret_val):
    return _lib.PdfTools_ToolboxPdfForms_SignedSignatureField_GetDate(signed_signature_field, byref(ret_val))

_lib.PdfTools_ToolboxPdfForms_SignedSignatureField_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_SignedSignatureField_GetType.restype = c_int

def pdfforms_signedsignaturefield_gettype(object):
    return _lib.PdfTools_ToolboxPdfForms_SignedSignatureField_GetType(object)

_lib.PdfTools_ToolboxPdfForms_Signature_GetLocationW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfForms_Signature_GetLocationW.restype = c_size_t

def pdfforms_signature_getlocation(signature):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfForms_Signature_GetLocationW(signature, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfForms_Signature_GetLocationW(signature, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfForms_Signature_GetReasonW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfForms_Signature_GetReasonW.restype = c_size_t

def pdfforms_signature_getreason(signature):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfForms_Signature_GetReasonW(signature, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfForms_Signature_GetReasonW(signature, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfForms_Signature_GetContactInfoW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfForms_Signature_GetContactInfoW.restype = c_size_t

def pdfforms_signature_getcontactinfo(signature):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfForms_Signature_GetContactInfoW(signature, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfForms_Signature_GetContactInfoW(signature, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)

_lib.PdfTools_ToolboxPdfForms_Signature_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_Signature_GetType.restype = c_int

def pdfforms_signature_gettype(object):
    return _lib.PdfTools_ToolboxPdfForms_Signature_GetType(object)

_lib.PdfTools_ToolboxPdfForms_DocMdpSignature_GetPermissions.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfForms_DocMdpSignature_GetPermissions.restype = c_int

def pdfforms_docmdpsignature_getpermissions(doc_mdp_signature):
    return _lib.PdfTools_ToolboxPdfForms_DocMdpSignature_GetPermissions(doc_mdp_signature)


_lib.PdfTools_ToolboxPdfNav_ViewerSettings_Copy.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_Copy.restype = c_void_p

def pdfnav_viewersettings_copy(target_document, viewer_settings):
    return _lib.PdfTools_ToolboxPdfNav_ViewerSettings_Copy(target_document, viewer_settings)

_lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetPageDisplay.argtypes = [c_void_p, POINTER(PdfNavPageDisplay)]
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetPageDisplay.restype = c_bool

def pdfnav_viewersettings_getpagedisplay(viewer_settings, ret_val):
    return _lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetPageDisplay(viewer_settings, byref(ret_val))
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetPageDisplay.argtypes = [c_void_p, POINTER(PdfNavPageDisplay)]
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetPageDisplay.restype = c_bool

def pdfnav_viewersettings_setpagedisplay(viewer_settings, val):
    return _lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetPageDisplay(viewer_settings, val)
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetActivePane.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetActivePane.restype = c_bool

def pdfnav_viewersettings_getactivepane(viewer_settings, ret_val):
    return _lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetActivePane(viewer_settings, byref(ret_val))
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetActivePane.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetActivePane.restype = c_bool

def pdfnav_viewersettings_setactivepane(viewer_settings, val):
    return _lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetActivePane(viewer_settings, byref(c_int(val)) if val is not None else None)
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetFullScreen.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetFullScreen.restype = c_bool

def pdfnav_viewersettings_getfullscreen(viewer_settings):
    return _lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetFullScreen(viewer_settings)
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetFullScreen.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetFullScreen.restype = c_bool

def pdfnav_viewersettings_setfullscreen(viewer_settings, val):
    return _lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetFullScreen(viewer_settings, val)
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetHideToolbar.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetHideToolbar.restype = c_bool

def pdfnav_viewersettings_gethidetoolbar(viewer_settings):
    return _lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetHideToolbar(viewer_settings)
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetHideToolbar.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetHideToolbar.restype = c_bool

def pdfnav_viewersettings_sethidetoolbar(viewer_settings, val):
    return _lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetHideToolbar(viewer_settings, val)
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetHideMenubar.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetHideMenubar.restype = c_bool

def pdfnav_viewersettings_gethidemenubar(viewer_settings):
    return _lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetHideMenubar(viewer_settings)
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetHideMenubar.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetHideMenubar.restype = c_bool

def pdfnav_viewersettings_sethidemenubar(viewer_settings, val):
    return _lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetHideMenubar(viewer_settings, val)
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetDisplayDocumentTitle.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetDisplayDocumentTitle.restype = c_bool

def pdfnav_viewersettings_getdisplaydocumenttitle(viewer_settings):
    return _lib.PdfTools_ToolboxPdfNav_ViewerSettings_GetDisplayDocumentTitle(viewer_settings)
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetDisplayDocumentTitle.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetDisplayDocumentTitle.restype = c_bool

def pdfnav_viewersettings_setdisplaydocumenttitle(viewer_settings, val):
    return _lib.PdfTools_ToolboxPdfNav_ViewerSettings_SetDisplayDocumentTitle(viewer_settings, val)


_lib.PdfTools_ToolboxPdfNav_OutlineItem_CreateW.argtypes = [c_void_p, c_wchar_p, c_void_p]
_lib.PdfTools_ToolboxPdfNav_OutlineItem_CreateW.restype = c_void_p

def pdfnav_outlineitem_create(target_document, title, destination):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItem_CreateW(target_document, string_to_utf16(title), destination)
_lib.PdfTools_ToolboxPdfNav_OutlineItem_Copy.argtypes = [c_void_p, c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfNav_OutlineItem_Copy.restype = c_void_p

def pdfnav_outlineitem_copy(target_document, outline_item, options):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItem_Copy(target_document, outline_item, options)

_lib.PdfTools_ToolboxPdfNav_OutlineItem_GetTitleW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfNav_OutlineItem_GetTitleW.restype = c_size_t

def pdfnav_outlineitem_gettitle(outline_item):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfNav_OutlineItem_GetTitleW(outline_item, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfNav_OutlineItem_GetTitleW(outline_item, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfNav_OutlineItem_SetTitleW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfNav_OutlineItem_SetTitleW.restype = c_bool

def pdfnav_outlineitem_settitle(outline_item, val):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItem_SetTitleW(outline_item, string_to_utf16(val))
_lib.PdfTools_ToolboxPdfNav_OutlineItem_GetBold.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_OutlineItem_GetBold.restype = c_bool

def pdfnav_outlineitem_getbold(outline_item):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItem_GetBold(outline_item)
_lib.PdfTools_ToolboxPdfNav_OutlineItem_SetBold.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfNav_OutlineItem_SetBold.restype = c_bool

def pdfnav_outlineitem_setbold(outline_item, val):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItem_SetBold(outline_item, val)
_lib.PdfTools_ToolboxPdfNav_OutlineItem_GetItalic.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_OutlineItem_GetItalic.restype = c_bool

def pdfnav_outlineitem_getitalic(outline_item):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItem_GetItalic(outline_item)
_lib.PdfTools_ToolboxPdfNav_OutlineItem_SetItalic.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfNav_OutlineItem_SetItalic.restype = c_bool

def pdfnav_outlineitem_setitalic(outline_item, val):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItem_SetItalic(outline_item, val)
_lib.PdfTools_ToolboxPdfNav_OutlineItem_GetDestination.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_OutlineItem_GetDestination.restype = c_void_p

def pdfnav_outlineitem_getdestination(outline_item):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItem_GetDestination(outline_item)
_lib.PdfTools_ToolboxPdfNav_OutlineItem_SetDestination.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfNav_OutlineItem_SetDestination.restype = c_bool

def pdfnav_outlineitem_setdestination(outline_item, val):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItem_SetDestination(outline_item, val)
_lib.PdfTools_ToolboxPdfNav_OutlineItem_IsOpen.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_OutlineItem_IsOpen.restype = c_bool

def pdfnav_outlineitem_isopen(outline_item):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItem_IsOpen(outline_item)
_lib.PdfTools_ToolboxPdfNav_OutlineItem_IsOpen.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfNav_OutlineItem_IsOpen.restype = c_bool

def pdfnav_outlineitem_isopen(outline_item, val):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItem_IsOpen(outline_item, val)
_lib.PdfTools_ToolboxPdfNav_OutlineItem_GetChildren.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_OutlineItem_GetChildren.restype = c_void_p

def pdfnav_outlineitem_getchildren(outline_item):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItem_GetChildren(outline_item)


_lib.PdfTools_ToolboxPdfNav_OutlineItemList_GetCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_OutlineItemList_GetCount.restype = c_int

def pdfnav_outlineitemlist_getcount(outline_item_list):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItemList_GetCount(outline_item_list)
_lib.PdfTools_ToolboxPdfNav_OutlineItemList_Get.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfNav_OutlineItemList_Get.restype = c_void_p

def pdfnav_outlineitemlist_get(outline_item_list, i_index):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItemList_Get(outline_item_list, i_index)
_lib.PdfTools_ToolboxPdfNav_OutlineItemList_Add.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfNav_OutlineItemList_Add.restype = c_bool

def pdfnav_outlineitemlist_add(outline_item_list, outline_item):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItemList_Add(outline_item_list, outline_item)
_lib.PdfTools_ToolboxPdfNav_OutlineItemList_Clear.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_OutlineItemList_Clear.restype = c_bool

def pdfnav_outlineitemlist_clear(outline_item_list):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItemList_Clear(outline_item_list)

_lib.PdfTools_ToolboxPdfNav_OutlineItemList_Remove.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfNav_OutlineItemList_Remove.restype = c_bool

def pdfnav_outlineitemlist_remove(outline_item_list, index):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItemList_Remove(outline_item_list, index)

_lib.PdfTools_ToolboxPdfNav_OutlineItemList_Set.argtypes = [c_void_p, c_int, c_void_p]
_lib.PdfTools_ToolboxPdfNav_OutlineItemList_Set.restype = c_bool

def pdfnav_outlineitemlist_set(outline_item_list, index, value):
    return _lib.PdfTools_ToolboxPdfNav_OutlineItemList_Set(outline_item_list, index, value)



_lib.PdfTools_ToolboxPdfNav_Destination_GetTarget.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_Destination_GetTarget.restype = c_void_p

def pdfnav_destination_gettarget(destination):
    return _lib.PdfTools_ToolboxPdfNav_Destination_GetTarget(destination)

_lib.PdfTools_ToolboxPdfNav_Destination_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_Destination_GetType.restype = c_int

def pdfnav_destination_gettype(object):
    return _lib.PdfTools_ToolboxPdfNav_Destination_GetType(object)

_lib.PdfTools_ToolboxPdfNav_NamedDestination_CreateW.argtypes = [c_void_p, c_wchar_p, c_void_p]
_lib.PdfTools_ToolboxPdfNav_NamedDestination_CreateW.restype = c_void_p

def pdfnav_nameddestination_create(target_document, name, target):
    return _lib.PdfTools_ToolboxPdfNav_NamedDestination_CreateW(target_document, string_to_utf16(name), target)

_lib.PdfTools_ToolboxPdfNav_NamedDestination_GetNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfNav_NamedDestination_GetNameW.restype = c_size_t

def pdfnav_nameddestination_getname(named_destination):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfNav_NamedDestination_GetNameW(named_destination, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfNav_NamedDestination_GetNameW(named_destination, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)


_lib.PdfTools_ToolboxPdfNav_DirectDestination_GetPage.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_DirectDestination_GetPage.restype = c_void_p

def pdfnav_directdestination_getpage(direct_destination):
    return _lib.PdfTools_ToolboxPdfNav_DirectDestination_GetPage(direct_destination)

_lib.PdfTools_ToolboxPdfNav_DirectDestination_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_DirectDestination_GetType.restype = c_int

def pdfnav_directdestination_gettype(object):
    return _lib.PdfTools_ToolboxPdfNav_DirectDestination_GetType(object)

_lib.PdfTools_ToolboxPdfNav_LocationZoomDestination_Create.argtypes = [c_void_p, c_void_p, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
_lib.PdfTools_ToolboxPdfNav_LocationZoomDestination_Create.restype = c_void_p

def pdfnav_locationzoomdestination_create(target_document, page, left, top, zoom):
    return _lib.PdfTools_ToolboxPdfNav_LocationZoomDestination_Create(target_document, page, byref(c_double(left)) if left is not None else None, byref(c_double(top)) if top is not None else None, byref(c_double(zoom)) if zoom is not None else None)

_lib.PdfTools_ToolboxPdfNav_LocationZoomDestination_GetLeft.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfTools_ToolboxPdfNav_LocationZoomDestination_GetLeft.restype = c_bool

def pdfnav_locationzoomdestination_getleft(location_zoom_destination, ret_val):
    return _lib.PdfTools_ToolboxPdfNav_LocationZoomDestination_GetLeft(location_zoom_destination, byref(ret_val))
_lib.PdfTools_ToolboxPdfNav_LocationZoomDestination_GetTop.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfTools_ToolboxPdfNav_LocationZoomDestination_GetTop.restype = c_bool

def pdfnav_locationzoomdestination_gettop(location_zoom_destination, ret_val):
    return _lib.PdfTools_ToolboxPdfNav_LocationZoomDestination_GetTop(location_zoom_destination, byref(ret_val))
_lib.PdfTools_ToolboxPdfNav_LocationZoomDestination_GetZoom.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfTools_ToolboxPdfNav_LocationZoomDestination_GetZoom.restype = c_bool

def pdfnav_locationzoomdestination_getzoom(location_zoom_destination, ret_val):
    return _lib.PdfTools_ToolboxPdfNav_LocationZoomDestination_GetZoom(location_zoom_destination, byref(ret_val))


_lib.PdfTools_ToolboxPdfNav_FitPageDestination_Create.argtypes = [c_void_p, c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfNav_FitPageDestination_Create.restype = c_void_p

def pdfnav_fitpagedestination_create(target_document, page, fit_actual_content):
    return _lib.PdfTools_ToolboxPdfNav_FitPageDestination_Create(target_document, page, fit_actual_content)

_lib.PdfTools_ToolboxPdfNav_FitPageDestination_GetFitActualContent.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_FitPageDestination_GetFitActualContent.restype = c_bool

def pdfnav_fitpagedestination_getfitactualcontent(fit_page_destination):
    return _lib.PdfTools_ToolboxPdfNav_FitPageDestination_GetFitActualContent(fit_page_destination)


_lib.PdfTools_ToolboxPdfNav_FitWidthDestination_Create.argtypes = [c_void_p, c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfNav_FitWidthDestination_Create.restype = c_void_p

def pdfnav_fitwidthdestination_create(target_document, page, fit_actual_content):
    return _lib.PdfTools_ToolboxPdfNav_FitWidthDestination_Create(target_document, page, fit_actual_content)

_lib.PdfTools_ToolboxPdfNav_FitWidthDestination_GetFitActualContent.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_FitWidthDestination_GetFitActualContent.restype = c_bool

def pdfnav_fitwidthdestination_getfitactualcontent(fit_width_destination):
    return _lib.PdfTools_ToolboxPdfNav_FitWidthDestination_GetFitActualContent(fit_width_destination)


_lib.PdfTools_ToolboxPdfNav_FitHeightDestination_Create.argtypes = [c_void_p, c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfNav_FitHeightDestination_Create.restype = c_void_p

def pdfnav_fitheightdestination_create(target_document, page, fit_actual_content):
    return _lib.PdfTools_ToolboxPdfNav_FitHeightDestination_Create(target_document, page, fit_actual_content)

_lib.PdfTools_ToolboxPdfNav_FitHeightDestination_GetFitActualContent.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_FitHeightDestination_GetFitActualContent.restype = c_bool

def pdfnav_fitheightdestination_getfitactualcontent(fit_height_destination):
    return _lib.PdfTools_ToolboxPdfNav_FitHeightDestination_GetFitActualContent(fit_height_destination)


_lib.PdfTools_ToolboxPdfNav_FitRectangleDestination_Create.argtypes = [c_void_p, c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdfNav_FitRectangleDestination_Create.restype = c_void_p

def pdfnav_fitrectangledestination_create(target_document, page, rectangle):
    return _lib.PdfTools_ToolboxPdfNav_FitRectangleDestination_Create(target_document, page, rectangle)

_lib.PdfTools_ToolboxPdfNav_FitRectangleDestination_GetRectangle.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdfNav_FitRectangleDestination_GetRectangle.restype = c_bool

def pdfnav_fitrectangledestination_getrectangle(fit_rectangle_destination, ret_val):
    return _lib.PdfTools_ToolboxPdfNav_FitRectangleDestination_GetRectangle(fit_rectangle_destination, byref(ret_val))


_lib.PdfTools_ToolboxPdfNav_Link_Copy.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfNav_Link_Copy.restype = c_void_p

def pdfnav_link_copy(target_document, link):
    return _lib.PdfTools_ToolboxPdfNav_Link_Copy(target_document, link)

_lib.PdfTools_ToolboxPdfNav_Link_GetActiveArea.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_Link_GetActiveArea.restype = c_void_p

def pdfnav_link_getactivearea(link):
    return _lib.PdfTools_ToolboxPdfNav_Link_GetActiveArea(link)
_lib.PdfTools_ToolboxPdfNav_Link_GetBoundingBox.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdfNav_Link_GetBoundingBox.restype = c_bool

def pdfnav_link_getboundingbox(link, ret_val):
    return _lib.PdfTools_ToolboxPdfNav_Link_GetBoundingBox(link, byref(ret_val))
_lib.PdfTools_ToolboxPdfNav_Link_GetHidden.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_Link_GetHidden.restype = c_bool

def pdfnav_link_gethidden(link):
    return _lib.PdfTools_ToolboxPdfNav_Link_GetHidden(link)
_lib.PdfTools_ToolboxPdfNav_Link_GetNoPrint.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_Link_GetNoPrint.restype = c_bool

def pdfnav_link_getnoprint(link):
    return _lib.PdfTools_ToolboxPdfNav_Link_GetNoPrint(link)
_lib.PdfTools_ToolboxPdfNav_Link_SetBorderStyle.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfNav_Link_SetBorderStyle.restype = c_bool

def pdfnav_link_setborderstyle(link, val):
    return _lib.PdfTools_ToolboxPdfNav_Link_SetBorderStyle(link, val)

_lib.PdfTools_ToolboxPdfNav_Link_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_Link_GetType.restype = c_int

def pdfnav_link_gettype(object):
    return _lib.PdfTools_ToolboxPdfNav_Link_GetType(object)

_lib.PdfTools_ToolboxPdfNav_LinkList_GetCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_LinkList_GetCount.restype = c_int

def pdfnav_linklist_getcount(link_list):
    return _lib.PdfTools_ToolboxPdfNav_LinkList_GetCount(link_list)
_lib.PdfTools_ToolboxPdfNav_LinkList_Get.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfNav_LinkList_Get.restype = c_void_p

def pdfnav_linklist_get(link_list, i_index):
    return _lib.PdfTools_ToolboxPdfNav_LinkList_Get(link_list, i_index)
_lib.PdfTools_ToolboxPdfNav_LinkList_Add.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfNav_LinkList_Add.restype = c_bool

def pdfnav_linklist_add(link_list, link):
    return _lib.PdfTools_ToolboxPdfNav_LinkList_Add(link_list, link)


_lib.PdfTools_ToolboxPdfNav_InternalLink_Create.argtypes = [c_void_p, POINTER(GeomRealRectangle), c_void_p]
_lib.PdfTools_ToolboxPdfNav_InternalLink_Create.restype = c_void_p

def pdfnav_internallink_create(target_document, bounding_box, target):
    return _lib.PdfTools_ToolboxPdfNav_InternalLink_Create(target_document, bounding_box, target)
_lib.PdfTools_ToolboxPdfNav_InternalLink_CreateFromQuadrilaterals.argtypes = [c_void_p, c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfNav_InternalLink_CreateFromQuadrilaterals.restype = c_void_p

def pdfnav_internallink_createfromquadrilaterals(target_document, active_area, target):
    return _lib.PdfTools_ToolboxPdfNav_InternalLink_CreateFromQuadrilaterals(target_document, active_area, target)

_lib.PdfTools_ToolboxPdfNav_InternalLink_GetDestination.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_InternalLink_GetDestination.restype = c_void_p

def pdfnav_internallink_getdestination(internal_link):
    return _lib.PdfTools_ToolboxPdfNav_InternalLink_GetDestination(internal_link)


_lib.PdfTools_ToolboxPdfNav_WebLink_CreateW.argtypes = [c_void_p, POINTER(GeomRealRectangle), c_wchar_p]
_lib.PdfTools_ToolboxPdfNav_WebLink_CreateW.restype = c_void_p

def pdfnav_weblink_create(target_document, bounding_box, uri):
    return _lib.PdfTools_ToolboxPdfNav_WebLink_CreateW(target_document, bounding_box, string_to_utf16(uri))
_lib.PdfTools_ToolboxPdfNav_WebLink_CreateFromQuadrilateralsW.argtypes = [c_void_p, c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfNav_WebLink_CreateFromQuadrilateralsW.restype = c_void_p

def pdfnav_weblink_createfromquadrilaterals(target_document, active_area, uri):
    return _lib.PdfTools_ToolboxPdfNav_WebLink_CreateFromQuadrilateralsW(target_document, active_area, string_to_utf16(uri))

_lib.PdfTools_ToolboxPdfNav_WebLink_GetUriW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfNav_WebLink_GetUriW.restype = c_size_t

def pdfnav_weblink_geturi(web_link):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfNav_WebLink_GetUriW(web_link, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfNav_WebLink_GetUriW(web_link, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfNav_WebLink_SetUriW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfNav_WebLink_SetUriW.restype = c_bool

def pdfnav_weblink_seturi(web_link, val):
    return _lib.PdfTools_ToolboxPdfNav_WebLink_SetUriW(web_link, string_to_utf16(val))


_lib.PdfTools_ToolboxPdfNav_EmbeddedPdfLink_Create.argtypes = [c_void_p, POINTER(GeomRealRectangle), c_void_p]
_lib.PdfTools_ToolboxPdfNav_EmbeddedPdfLink_Create.restype = c_void_p

def pdfnav_embeddedpdflink_create(target_document, bounding_box, file_reference):
    return _lib.PdfTools_ToolboxPdfNav_EmbeddedPdfLink_Create(target_document, bounding_box, file_reference)
_lib.PdfTools_ToolboxPdfNav_EmbeddedPdfLink_CreateFromQuadrilaterals.argtypes = [c_void_p, c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfNav_EmbeddedPdfLink_CreateFromQuadrilaterals.restype = c_void_p

def pdfnav_embeddedpdflink_createfromquadrilaterals(target_document, active_area, file_reference):
    return _lib.PdfTools_ToolboxPdfNav_EmbeddedPdfLink_CreateFromQuadrilaterals(target_document, active_area, file_reference)

_lib.PdfTools_ToolboxPdfNav_EmbeddedPdfLink_GetNewWindow.argtypes = [c_void_p, POINTER(c_bool)]
_lib.PdfTools_ToolboxPdfNav_EmbeddedPdfLink_GetNewWindow.restype = c_bool

def pdfnav_embeddedpdflink_getnewwindow(embedded_pdf_link, ret_val):
    return _lib.PdfTools_ToolboxPdfNav_EmbeddedPdfLink_GetNewWindow(embedded_pdf_link, byref(ret_val))
_lib.PdfTools_ToolboxPdfNav_EmbeddedPdfLink_SetNewWindow.argtypes = [c_void_p, POINTER(c_bool)]
_lib.PdfTools_ToolboxPdfNav_EmbeddedPdfLink_SetNewWindow.restype = c_bool

def pdfnav_embeddedpdflink_setnewwindow(embedded_pdf_link, val):
    return _lib.PdfTools_ToolboxPdfNav_EmbeddedPdfLink_SetNewWindow(embedded_pdf_link, byref(c_bool(val)) if val is not None else None)


_lib.PdfTools_ToolboxPdfNav_OutlineCopyOptions_New.argtypes = []
_lib.PdfTools_ToolboxPdfNav_OutlineCopyOptions_New.restype = c_void_p

def pdfnav_outlinecopyoptions_new():
    return _lib.PdfTools_ToolboxPdfNav_OutlineCopyOptions_New()

_lib.PdfTools_ToolboxPdfNav_OutlineCopyOptions_GetCopyLogicalStructure.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_OutlineCopyOptions_GetCopyLogicalStructure.restype = c_bool

def pdfnav_outlinecopyoptions_getcopylogicalstructure(outline_copy_options):
    return _lib.PdfTools_ToolboxPdfNav_OutlineCopyOptions_GetCopyLogicalStructure(outline_copy_options)
_lib.PdfTools_ToolboxPdfNav_OutlineCopyOptions_SetCopyLogicalStructure.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfNav_OutlineCopyOptions_SetCopyLogicalStructure.restype = c_bool

def pdfnav_outlinecopyoptions_setcopylogicalstructure(outline_copy_options, val):
    return _lib.PdfTools_ToolboxPdfNav_OutlineCopyOptions_SetCopyLogicalStructure(outline_copy_options, val)
_lib.PdfTools_ToolboxPdfNav_OutlineCopyOptions_GetNamedDestinations.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfNav_OutlineCopyOptions_GetNamedDestinations.restype = c_int

def pdfnav_outlinecopyoptions_getnameddestinations(outline_copy_options):
    return _lib.PdfTools_ToolboxPdfNav_OutlineCopyOptions_GetNamedDestinations(outline_copy_options)
_lib.PdfTools_ToolboxPdfNav_OutlineCopyOptions_SetNamedDestinations.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfNav_OutlineCopyOptions_SetNamedDestinations.restype = c_bool

def pdfnav_outlinecopyoptions_setnameddestinations(outline_copy_options, val):
    return _lib.PdfTools_ToolboxPdfNav_OutlineCopyOptions_SetNamedDestinations(outline_copy_options, val)


_lib.PdfTools_ToolboxPdfAnnots_Annotation_Copy.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_Annotation_Copy.restype = c_void_p

def pdfannots_annotation_copy(target_document, annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_Annotation_Copy(target_document, annotation)

_lib.PdfTools_ToolboxPdfAnnots_Annotation_GetBoundingBox.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdfAnnots_Annotation_GetBoundingBox.restype = c_bool

def pdfannots_annotation_getboundingbox(annotation, ret_val):
    return _lib.PdfTools_ToolboxPdfAnnots_Annotation_GetBoundingBox(annotation, byref(ret_val))
_lib.PdfTools_ToolboxPdfAnnots_Annotation_GetHidden.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_Annotation_GetHidden.restype = c_bool

def pdfannots_annotation_gethidden(annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_Annotation_GetHidden(annotation)
_lib.PdfTools_ToolboxPdfAnnots_Annotation_GetNoPrint.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_Annotation_GetNoPrint.restype = c_bool

def pdfannots_annotation_getnoprint(annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_Annotation_GetNoPrint(annotation)
_lib.PdfTools_ToolboxPdfAnnots_Annotation_GetNoZoom.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_Annotation_GetNoZoom.restype = c_bool

def pdfannots_annotation_getnozoom(annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_Annotation_GetNoZoom(annotation)
_lib.PdfTools_ToolboxPdfAnnots_Annotation_GetNoRotate.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_Annotation_GetNoRotate.restype = c_bool

def pdfannots_annotation_getnorotate(annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_Annotation_GetNoRotate(annotation)
_lib.PdfTools_ToolboxPdfAnnots_Annotation_GetIdW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfAnnots_Annotation_GetIdW.restype = c_size_t

def pdfannots_annotation_getid(annotation):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfAnnots_Annotation_GetIdW(annotation, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfAnnots_Annotation_GetIdW(annotation, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)

_lib.PdfTools_ToolboxPdfAnnots_Annotation_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_Annotation_GetType.restype = c_int

def pdfannots_annotation_gettype(object):
    return _lib.PdfTools_ToolboxPdfAnnots_Annotation_GetType(object)

_lib.PdfTools_ToolboxPdfAnnots_AnnotationList_GetCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_AnnotationList_GetCount.restype = c_int

def pdfannots_annotationlist_getcount(annotation_list):
    return _lib.PdfTools_ToolboxPdfAnnots_AnnotationList_GetCount(annotation_list)
_lib.PdfTools_ToolboxPdfAnnots_AnnotationList_Get.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfAnnots_AnnotationList_Get.restype = c_void_p

def pdfannots_annotationlist_get(annotation_list, i_index):
    return _lib.PdfTools_ToolboxPdfAnnots_AnnotationList_Get(annotation_list, i_index)
_lib.PdfTools_ToolboxPdfAnnots_AnnotationList_Add.argtypes = [c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_AnnotationList_Add.restype = c_bool

def pdfannots_annotationlist_add(annotation_list, annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_AnnotationList_Add(annotation_list, annotation)


_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetCreationDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetCreationDate.restype = c_bool

def pdfannots_markupinfo_getcreationdate(markup_info, ret_val):
    return _lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetCreationDate(markup_info, byref(ret_val))
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetCreationDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetCreationDate.restype = c_bool

def pdfannots_markupinfo_setcreationdate(markup_info, val):
    return _lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetCreationDate(markup_info, val)
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetModificationDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetModificationDate.restype = c_bool

def pdfannots_markupinfo_getmodificationdate(markup_info, ret_val):
    return _lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetModificationDate(markup_info, byref(ret_val))
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetModificationDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetModificationDate.restype = c_bool

def pdfannots_markupinfo_setmodificationdate(markup_info, val):
    return _lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetModificationDate(markup_info, val)
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetLocked.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetLocked.restype = c_bool

def pdfannots_markupinfo_getlocked(markup_info):
    return _lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetLocked(markup_info)
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetLocked.argtypes = [c_void_p, c_bool]
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetLocked.restype = c_bool

def pdfannots_markupinfo_setlocked(markup_info, val):
    return _lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetLocked(markup_info, val)
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetAuthorW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetAuthorW.restype = c_size_t

def pdfannots_markupinfo_getauthor(markup_info):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetAuthorW(markup_info, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetAuthorW(markup_info, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetAuthorW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetAuthorW.restype = c_bool

def pdfannots_markupinfo_setauthor(markup_info, val):
    return _lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetAuthorW(markup_info, string_to_utf16(val))
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetSubjectW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetSubjectW.restype = c_size_t

def pdfannots_markupinfo_getsubject(markup_info):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetSubjectW(markup_info, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetSubjectW(markup_info, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetSubjectW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetSubjectW.restype = c_bool

def pdfannots_markupinfo_setsubject(markup_info, val):
    return _lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetSubjectW(markup_info, string_to_utf16(val))
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetContentW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetContentW.restype = c_size_t

def pdfannots_markupinfo_getcontent(markup_info):
    ret_buffer_size = _lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetContentW(markup_info, None, 0)
    if ret_buffer_size == 0 and get_last_error() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_GetContentW(markup_info, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetContentW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetContentW.restype = c_bool

def pdfannots_markupinfo_setcontent(markup_info, val):
    return _lib.PdfTools_ToolboxPdfAnnots_MarkupInfo_SetContentW(markup_info, string_to_utf16(val))


_lib.PdfTools_ToolboxPdfAnnots_MarkupInfoList_GetCount.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfoList_GetCount.restype = c_int

def pdfannots_markupinfolist_getcount(markup_info_list):
    return _lib.PdfTools_ToolboxPdfAnnots_MarkupInfoList_GetCount(markup_info_list)
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfoList_Get.argtypes = [c_void_p, c_int]
_lib.PdfTools_ToolboxPdfAnnots_MarkupInfoList_Get.restype = c_void_p

def pdfannots_markupinfolist_get(markup_info_list, i_index):
    return _lib.PdfTools_ToolboxPdfAnnots_MarkupInfoList_Get(markup_info_list, i_index)


_lib.PdfTools_ToolboxPdfAnnots_Popup_IsOpen.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_Popup_IsOpen.restype = c_bool

def pdfannots_popup_isopen(popup):
    return _lib.PdfTools_ToolboxPdfAnnots_Popup_IsOpen(popup)
_lib.PdfTools_ToolboxPdfAnnots_Popup_GetBoundingBox.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdfAnnots_Popup_GetBoundingBox.restype = c_bool

def pdfannots_popup_getboundingbox(popup, ret_val):
    return _lib.PdfTools_ToolboxPdfAnnots_Popup_GetBoundingBox(popup, byref(ret_val))


_lib.PdfTools_ToolboxPdfAnnots_MarkupAnnotation_GetLocked.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_MarkupAnnotation_GetLocked.restype = c_bool

def pdfannots_markupannotation_getlocked(markup_annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_MarkupAnnotation_GetLocked(markup_annotation)
_lib.PdfTools_ToolboxPdfAnnots_MarkupAnnotation_GetInfo.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_MarkupAnnotation_GetInfo.restype = c_void_p

def pdfannots_markupannotation_getinfo(markup_annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_MarkupAnnotation_GetInfo(markup_annotation)
_lib.PdfTools_ToolboxPdfAnnots_MarkupAnnotation_GetReplies.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_MarkupAnnotation_GetReplies.restype = c_void_p

def pdfannots_markupannotation_getreplies(markup_annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_MarkupAnnotation_GetReplies(markup_annotation)

_lib.PdfTools_ToolboxPdfAnnots_MarkupAnnotation_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_MarkupAnnotation_GetType.restype = c_int

def pdfannots_markupannotation_gettype(object):
    return _lib.PdfTools_ToolboxPdfAnnots_MarkupAnnotation_GetType(object)

_lib.PdfTools_ToolboxPdfAnnots_StickyNote_CreateW.argtypes = [c_void_p, POINTER(GeomRealPoint), c_wchar_p, c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_StickyNote_CreateW.restype = c_void_p

def pdfannots_stickynote_create(target_document, top_left, content, paint):
    return _lib.PdfTools_ToolboxPdfAnnots_StickyNote_CreateW(target_document, top_left, string_to_utf16(content), paint)

_lib.PdfTools_ToolboxPdfAnnots_StickyNote_GetPaint.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_StickyNote_GetPaint.restype = c_void_p

def pdfannots_stickynote_getpaint(sticky_note):
    return _lib.PdfTools_ToolboxPdfAnnots_StickyNote_GetPaint(sticky_note)
_lib.PdfTools_ToolboxPdfAnnots_StickyNote_GetPopup.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_StickyNote_GetPopup.restype = c_void_p

def pdfannots_stickynote_getpopup(sticky_note):
    return _lib.PdfTools_ToolboxPdfAnnots_StickyNote_GetPopup(sticky_note)


_lib.PdfTools_ToolboxPdfAnnots_FileAttachment_Create.argtypes = [c_void_p, POINTER(GeomRealPoint), c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_FileAttachment_Create.restype = c_void_p

def pdfannots_fileattachment_create(target_document, top_left, attached_file, paint):
    return _lib.PdfTools_ToolboxPdfAnnots_FileAttachment_Create(target_document, top_left, attached_file, paint)

_lib.PdfTools_ToolboxPdfAnnots_FileAttachment_GetIcon.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_FileAttachment_GetIcon.restype = c_int

def pdfannots_fileattachment_geticon(file_attachment):
    return _lib.PdfTools_ToolboxPdfAnnots_FileAttachment_GetIcon(file_attachment)
_lib.PdfTools_ToolboxPdfAnnots_FileAttachment_GetPaint.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_FileAttachment_GetPaint.restype = c_void_p

def pdfannots_fileattachment_getpaint(file_attachment):
    return _lib.PdfTools_ToolboxPdfAnnots_FileAttachment_GetPaint(file_attachment)
_lib.PdfTools_ToolboxPdfAnnots_FileAttachment_GetAttachedFile.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_FileAttachment_GetAttachedFile.restype = c_void_p

def pdfannots_fileattachment_getattachedfile(file_attachment):
    return _lib.PdfTools_ToolboxPdfAnnots_FileAttachment_GetAttachedFile(file_attachment)
_lib.PdfTools_ToolboxPdfAnnots_FileAttachment_GetPopup.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_FileAttachment_GetPopup.restype = c_void_p

def pdfannots_fileattachment_getpopup(file_attachment):
    return _lib.PdfTools_ToolboxPdfAnnots_FileAttachment_GetPopup(file_attachment)


_lib.PdfTools_ToolboxPdfAnnots_Stamp_GetPopup.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_Stamp_GetPopup.restype = c_void_p

def pdfannots_stamp_getpopup(stamp):
    return _lib.PdfTools_ToolboxPdfAnnots_Stamp_GetPopup(stamp)
_lib.PdfTools_ToolboxPdfAnnots_Stamp_GetPopupPaint.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_Stamp_GetPopupPaint.restype = c_void_p

def pdfannots_stamp_getpopuppaint(stamp):
    return _lib.PdfTools_ToolboxPdfAnnots_Stamp_GetPopupPaint(stamp)

_lib.PdfTools_ToolboxPdfAnnots_Stamp_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_Stamp_GetType.restype = c_int

def pdfannots_stamp_gettype(object):
    return _lib.PdfTools_ToolboxPdfAnnots_Stamp_GetType(object)

_lib.PdfTools_ToolboxPdfAnnots_TextStamp_CreateRawW.argtypes = [c_void_p, POINTER(GeomRealPoint), POINTER(c_double), c_int, c_wchar_p]
_lib.PdfTools_ToolboxPdfAnnots_TextStamp_CreateRawW.restype = c_void_p

def pdfannots_textstamp_createraw(target_document, top_left, height, text_type, text):
    return _lib.PdfTools_ToolboxPdfAnnots_TextStamp_CreateRawW(target_document, top_left, byref(c_double(height)) if height is not None else None, text_type, string_to_utf16(text))
_lib.PdfTools_ToolboxPdfAnnots_TextStamp_Create.argtypes = [c_void_p, POINTER(GeomRealPoint), POINTER(c_double), c_int]
_lib.PdfTools_ToolboxPdfAnnots_TextStamp_Create.restype = c_void_p

def pdfannots_textstamp_create(target_document, top_left, height, text_type):
    return _lib.PdfTools_ToolboxPdfAnnots_TextStamp_Create(target_document, top_left, byref(c_double(height)) if height is not None else None, text_type)

_lib.PdfTools_ToolboxPdfAnnots_TextStamp_GetTextType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_TextStamp_GetTextType.restype = c_int

def pdfannots_textstamp_gettexttype(text_stamp):
    return _lib.PdfTools_ToolboxPdfAnnots_TextStamp_GetTextType(text_stamp)


_lib.PdfTools_ToolboxPdfAnnots_CustomStamp_Create.argtypes = [c_void_p, POINTER(GeomRealRectangle)]
_lib.PdfTools_ToolboxPdfAnnots_CustomStamp_Create.restype = c_void_p

def pdfannots_customstamp_create(target_document, bounding_box):
    return _lib.PdfTools_ToolboxPdfAnnots_CustomStamp_Create(target_document, bounding_box)

_lib.PdfTools_ToolboxPdfAnnots_CustomStamp_GetAppearance.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_CustomStamp_GetAppearance.restype = c_void_p

def pdfannots_customstamp_getappearance(custom_stamp):
    return _lib.PdfTools_ToolboxPdfAnnots_CustomStamp_GetAppearance(custom_stamp)


_lib.PdfTools_ToolboxPdfAnnots_FreeText_CreateW.argtypes = [c_void_p, POINTER(GeomRealRectangle), c_wchar_p, c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_FreeText_CreateW.restype = c_void_p

def pdfannots_freetext_create(target_document, bounding_box, content, paint, stroke):
    return _lib.PdfTools_ToolboxPdfAnnots_FreeText_CreateW(target_document, bounding_box, string_to_utf16(content), paint, stroke)

_lib.PdfTools_ToolboxPdfAnnots_FreeText_GetFontSize.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_FreeText_GetFontSize.restype = c_double

def pdfannots_freetext_getfontsize(free_text):
    return _lib.PdfTools_ToolboxPdfAnnots_FreeText_GetFontSize(free_text)
_lib.PdfTools_ToolboxPdfAnnots_FreeText_SetFontSize.argtypes = [c_void_p, c_double]
_lib.PdfTools_ToolboxPdfAnnots_FreeText_SetFontSize.restype = c_bool

def pdfannots_freetext_setfontsize(free_text, val):
    return _lib.PdfTools_ToolboxPdfAnnots_FreeText_SetFontSize(free_text, val)
_lib.PdfTools_ToolboxPdfAnnots_FreeText_GetAlignment.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_FreeText_GetAlignment.restype = c_int

def pdfannots_freetext_getalignment(free_text):
    return _lib.PdfTools_ToolboxPdfAnnots_FreeText_GetAlignment(free_text)
_lib.PdfTools_ToolboxPdfAnnots_FreeText_GetPaint.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_FreeText_GetPaint.restype = c_void_p

def pdfannots_freetext_getpaint(free_text):
    return _lib.PdfTools_ToolboxPdfAnnots_FreeText_GetPaint(free_text)


_lib.PdfTools_ToolboxPdfAnnots_DrawingAnnotation_GetPaint.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_DrawingAnnotation_GetPaint.restype = c_void_p

def pdfannots_drawingannotation_getpaint(drawing_annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_DrawingAnnotation_GetPaint(drawing_annotation)
_lib.PdfTools_ToolboxPdfAnnots_DrawingAnnotation_GetPopup.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_DrawingAnnotation_GetPopup.restype = c_void_p

def pdfannots_drawingannotation_getpopup(drawing_annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_DrawingAnnotation_GetPopup(drawing_annotation)

_lib.PdfTools_ToolboxPdfAnnots_DrawingAnnotation_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_DrawingAnnotation_GetType.restype = c_int

def pdfannots_drawingannotation_gettype(object):
    return _lib.PdfTools_ToolboxPdfAnnots_DrawingAnnotation_GetType(object)

_lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_Create.argtypes = [c_void_p, POINTER(GeomRealPoint), POINTER(GeomRealPoint), c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_Create.restype = c_void_p

def pdfannots_lineannotation_create(target_document, start, end, stroke):
    return _lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_Create(target_document, start, end, stroke)

_lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_GetStart.argtypes = [c_void_p, POINTER(GeomRealPoint)]
_lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_GetStart.restype = c_bool

def pdfannots_lineannotation_getstart(line_annotation, ret_val):
    return _lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_GetStart(line_annotation, byref(ret_val))
_lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_GetEnd.argtypes = [c_void_p, POINTER(GeomRealPoint)]
_lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_GetEnd.restype = c_bool

def pdfannots_lineannotation_getend(line_annotation, ret_val):
    return _lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_GetEnd(line_annotation, byref(ret_val))
_lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_GetStartStyle.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_GetStartStyle.restype = c_int

def pdfannots_lineannotation_getstartstyle(line_annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_GetStartStyle(line_annotation)
_lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_GetEndStyle.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_GetEndStyle.restype = c_int

def pdfannots_lineannotation_getendstyle(line_annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_GetEndStyle(line_annotation)
_lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_GetLineEndingFill.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_GetLineEndingFill.restype = c_void_p

def pdfannots_lineannotation_getlineendingfill(line_annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_LineAnnotation_GetLineEndingFill(line_annotation)


_lib.PdfTools_ToolboxPdfAnnots_InkAnnotation_Create.argtypes = [c_void_p, c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_InkAnnotation_Create.restype = c_void_p

def pdfannots_inkannotation_create(target_document, path, stroke):
    return _lib.PdfTools_ToolboxPdfAnnots_InkAnnotation_Create(target_document, path, stroke)


_lib.PdfTools_ToolboxPdfAnnots_PolyLineAnnotation_Create.argtypes = [c_void_p, c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_PolyLineAnnotation_Create.restype = c_void_p

def pdfannots_polylineannotation_create(target_document, path, stroke):
    return _lib.PdfTools_ToolboxPdfAnnots_PolyLineAnnotation_Create(target_document, path, stroke)

_lib.PdfTools_ToolboxPdfAnnots_PolyLineAnnotation_GetStartStyle.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_PolyLineAnnotation_GetStartStyle.restype = c_int

def pdfannots_polylineannotation_getstartstyle(poly_line_annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_PolyLineAnnotation_GetStartStyle(poly_line_annotation)
_lib.PdfTools_ToolboxPdfAnnots_PolyLineAnnotation_GetEndStyle.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_PolyLineAnnotation_GetEndStyle.restype = c_int

def pdfannots_polylineannotation_getendstyle(poly_line_annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_PolyLineAnnotation_GetEndStyle(poly_line_annotation)
_lib.PdfTools_ToolboxPdfAnnots_PolyLineAnnotation_GetLineEndingFill.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_PolyLineAnnotation_GetLineEndingFill.restype = c_void_p

def pdfannots_polylineannotation_getlineendingfill(poly_line_annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_PolyLineAnnotation_GetLineEndingFill(poly_line_annotation)


_lib.PdfTools_ToolboxPdfAnnots_PolygonAnnotation_Create.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_PolygonAnnotation_Create.restype = c_void_p

def pdfannots_polygonannotation_create(target_document, path, stroke, fill):
    return _lib.PdfTools_ToolboxPdfAnnots_PolygonAnnotation_Create(target_document, path, stroke, fill)

_lib.PdfTools_ToolboxPdfAnnots_PolygonAnnotation_GetFill.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_PolygonAnnotation_GetFill.restype = c_void_p

def pdfannots_polygonannotation_getfill(polygon_annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_PolygonAnnotation_GetFill(polygon_annotation)


_lib.PdfTools_ToolboxPdfAnnots_RectangleAnnotation_Create.argtypes = [c_void_p, POINTER(GeomRealRectangle), c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_RectangleAnnotation_Create.restype = c_void_p

def pdfannots_rectangleannotation_create(target_document, bounding_box, stroke, fill):
    return _lib.PdfTools_ToolboxPdfAnnots_RectangleAnnotation_Create(target_document, bounding_box, stroke, fill)

_lib.PdfTools_ToolboxPdfAnnots_RectangleAnnotation_GetFill.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_RectangleAnnotation_GetFill.restype = c_void_p

def pdfannots_rectangleannotation_getfill(rectangle_annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_RectangleAnnotation_GetFill(rectangle_annotation)


_lib.PdfTools_ToolboxPdfAnnots_EllipseAnnotation_Create.argtypes = [c_void_p, POINTER(GeomRealRectangle), c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_EllipseAnnotation_Create.restype = c_void_p

def pdfannots_ellipseannotation_create(target_document, bounding_box, stroke, fill):
    return _lib.PdfTools_ToolboxPdfAnnots_EllipseAnnotation_Create(target_document, bounding_box, stroke, fill)

_lib.PdfTools_ToolboxPdfAnnots_EllipseAnnotation_GetFill.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_EllipseAnnotation_GetFill.restype = c_void_p

def pdfannots_ellipseannotation_getfill(ellipse_annotation):
    return _lib.PdfTools_ToolboxPdfAnnots_EllipseAnnotation_GetFill(ellipse_annotation)


_lib.PdfTools_ToolboxPdfAnnots_TextMarkup_GetPaint.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_TextMarkup_GetPaint.restype = c_void_p

def pdfannots_textmarkup_getpaint(text_markup):
    return _lib.PdfTools_ToolboxPdfAnnots_TextMarkup_GetPaint(text_markup)
_lib.PdfTools_ToolboxPdfAnnots_TextMarkup_GetPopup.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_TextMarkup_GetPopup.restype = c_void_p

def pdfannots_textmarkup_getpopup(text_markup):
    return _lib.PdfTools_ToolboxPdfAnnots_TextMarkup_GetPopup(text_markup)
_lib.PdfTools_ToolboxPdfAnnots_TextMarkup_GetMarkupArea.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_TextMarkup_GetMarkupArea.restype = c_void_p

def pdfannots_textmarkup_getmarkuparea(text_markup):
    return _lib.PdfTools_ToolboxPdfAnnots_TextMarkup_GetMarkupArea(text_markup)

_lib.PdfTools_ToolboxPdfAnnots_TextMarkup_GetType.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_TextMarkup_GetType.restype = c_int

def pdfannots_textmarkup_gettype(object):
    return _lib.PdfTools_ToolboxPdfAnnots_TextMarkup_GetType(object)

_lib.PdfTools_ToolboxPdfAnnots_Highlight_CreateFromQuadrilaterals.argtypes = [c_void_p, c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_Highlight_CreateFromQuadrilaterals.restype = c_void_p

def pdfannots_highlight_createfromquadrilaterals(target_document, markup_area, paint):
    return _lib.PdfTools_ToolboxPdfAnnots_Highlight_CreateFromQuadrilaterals(target_document, markup_area, paint)


_lib.PdfTools_ToolboxPdfAnnots_Underline_CreateFromQuadrilaterals.argtypes = [c_void_p, c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_Underline_CreateFromQuadrilaterals.restype = c_void_p

def pdfannots_underline_createfromquadrilaterals(target_document, markup_area, paint):
    return _lib.PdfTools_ToolboxPdfAnnots_Underline_CreateFromQuadrilaterals(target_document, markup_area, paint)


_lib.PdfTools_ToolboxPdfAnnots_StrikeThrough_CreateFromQuadrilaterals.argtypes = [c_void_p, c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_StrikeThrough_CreateFromQuadrilaterals.restype = c_void_p

def pdfannots_strikethrough_createfromquadrilaterals(target_document, markup_area, paint):
    return _lib.PdfTools_ToolboxPdfAnnots_StrikeThrough_CreateFromQuadrilaterals(target_document, markup_area, paint)


_lib.PdfTools_ToolboxPdfAnnots_Squiggly_CreateFromQuadrilaterals.argtypes = [c_void_p, c_void_p, c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_Squiggly_CreateFromQuadrilaterals.restype = c_void_p

def pdfannots_squiggly_createfromquadrilaterals(target_document, markup_area, paint):
    return _lib.PdfTools_ToolboxPdfAnnots_Squiggly_CreateFromQuadrilaterals(target_document, markup_area, paint)


_lib.PdfTools_ToolboxPdfAnnots_TextInsert_GetPaint.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_TextInsert_GetPaint.restype = c_void_p

def pdfannots_textinsert_getpaint(text_insert):
    return _lib.PdfTools_ToolboxPdfAnnots_TextInsert_GetPaint(text_insert)
_lib.PdfTools_ToolboxPdfAnnots_TextInsert_GetPopup.argtypes = [c_void_p]
_lib.PdfTools_ToolboxPdfAnnots_TextInsert_GetPopup.restype = c_void_p

def pdfannots_textinsert_getpopup(text_insert):
    return _lib.PdfTools_ToolboxPdfAnnots_TextInsert_GetPopup(text_insert)




# Struct functions
_lib.PdfTools_ToolboxGeomReal_AffineTransform_Translate.argtypes = [POINTER(GeomRealAffineTransform), c_double, c_double]
_lib.PdfTools_ToolboxGeomReal_AffineTransform_Translate.restype = c_bool

def geomreal_affinetransform_translate(affine_transform, tx, ty):
    return _lib.PdfTools_ToolboxGeomReal_AffineTransform_Translate(affine_transform, tx, ty)

_lib.PdfTools_ToolboxGeomReal_AffineTransform_Scale.argtypes = [POINTER(GeomRealAffineTransform), c_double, c_double]
_lib.PdfTools_ToolboxGeomReal_AffineTransform_Scale.restype = c_bool

def geomreal_affinetransform_scale(affine_transform, sx, sy):
    return _lib.PdfTools_ToolboxGeomReal_AffineTransform_Scale(affine_transform, sx, sy)

_lib.PdfTools_ToolboxGeomReal_AffineTransform_Rotate.argtypes = [POINTER(GeomRealAffineTransform), c_double, POINTER(GeomRealPoint)]
_lib.PdfTools_ToolboxGeomReal_AffineTransform_Rotate.restype = c_bool

def geomreal_affinetransform_rotate(affine_transform, angle, center):
    return _lib.PdfTools_ToolboxGeomReal_AffineTransform_Rotate(affine_transform, angle, center)

_lib.PdfTools_ToolboxGeomReal_AffineTransform_Skew.argtypes = [POINTER(GeomRealAffineTransform), c_double, c_double]
_lib.PdfTools_ToolboxGeomReal_AffineTransform_Skew.restype = c_bool

def geomreal_affinetransform_skew(affine_transform, alpha, beta):
    return _lib.PdfTools_ToolboxGeomReal_AffineTransform_Skew(affine_transform, alpha, beta)

_lib.PdfTools_ToolboxGeomReal_AffineTransform_Concatenate.argtypes = [POINTER(GeomRealAffineTransform), POINTER(GeomRealAffineTransform)]
_lib.PdfTools_ToolboxGeomReal_AffineTransform_Concatenate.restype = c_bool

def geomreal_affinetransform_concatenate(affine_transform, other):
    return _lib.PdfTools_ToolboxGeomReal_AffineTransform_Concatenate(affine_transform, other)

_lib.PdfTools_ToolboxGeomReal_AffineTransform_Invert.argtypes = [POINTER(GeomRealAffineTransform)]
_lib.PdfTools_ToolboxGeomReal_AffineTransform_Invert.restype = c_bool

def geomreal_affinetransform_invert(affine_transform):
    return _lib.PdfTools_ToolboxGeomReal_AffineTransform_Invert(affine_transform)

_lib.PdfTools_ToolboxGeomReal_AffineTransform_TransformPoint.argtypes = [POINTER(GeomRealAffineTransform), POINTER(GeomRealPoint), POINTER(GeomRealPoint)]
_lib.PdfTools_ToolboxGeomReal_AffineTransform_TransformPoint.restype = c_bool

def geomreal_affinetransform_transformpoint(affine_transform, original, ret_val):
    return _lib.PdfTools_ToolboxGeomReal_AffineTransform_TransformPoint(affine_transform, original, byref(ret_val))
_lib.PdfTools_ToolboxGeomReal_AffineTransform_TransformRectangle.argtypes = [POINTER(GeomRealAffineTransform), POINTER(GeomRealRectangle), POINTER(GeomRealQuadrilateral)]
_lib.PdfTools_ToolboxGeomReal_AffineTransform_TransformRectangle.restype = c_bool

def geomreal_affinetransform_transformrectangle(affine_transform, original, ret_val):
    return _lib.PdfTools_ToolboxGeomReal_AffineTransform_TransformRectangle(affine_transform, original, byref(ret_val))
_lib.PdfTools_ToolboxGeomReal_AffineTransform_TransformQuadrilateral.argtypes = [POINTER(GeomRealAffineTransform), POINTER(GeomRealQuadrilateral), POINTER(GeomRealQuadrilateral)]
_lib.PdfTools_ToolboxGeomReal_AffineTransform_TransformQuadrilateral.restype = c_bool

def geomreal_affinetransform_transformquadrilateral(affine_transform, original, ret_val):
    return _lib.PdfTools_ToolboxGeomReal_AffineTransform_TransformQuadrilateral(affine_transform, original, byref(ret_val))

_lib.PdfTools_ToolboxGeomReal_AffineTransform_GetIdentity.argtypes = [POINTER(GeomRealAffineTransform)]
_lib.PdfTools_ToolboxGeomReal_AffineTransform_GetIdentity.restype = c_bool

def geomreal_affinetransform_getidentity(ret_val):
    return _lib.PdfTools_ToolboxGeomReal_AffineTransform_GetIdentity(byref(ret_val))



# Utility functions

def print_error_message(message):
    print(f"{message} {getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
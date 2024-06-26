import logging
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)

MB_ROOT = getattr(
    settings,
    "MEDIA_BROWSER_ROOT",
    os.path.join(settings.BASE_DIR, "mediabrowser_files"),
)

MB_STORAGE_CONF = getattr(settings, "MEDIA_BROWSER_STORAGE", None)
if MB_STORAGE_CONF:
    MB_STORAGE = import_string(MB_STORAGE_CONF)
else:
    MB_STORAGE = FileSystemStorage(location=MB_ROOT)
MEDIA_BROWSER_AUTH_FUNCTION = getattr(
    settings, "MB_AUTH_FUNCTION", "rest_mediabrowser.utils.default_auth"
)
MB_THUMBNAIL_FORMAT = getattr(settings, "MEDIA_BROWSER_THUMBNAIL_FORMAT", "WEBP")
MB_PUBLISHED_ROOT = getattr(
    settings, "MEDIA_BROWSER_PUBLISHED_ROOT", "mediabrowser_published"
)
MB_PUBLISHED_FILE_PATH = os.path.join(settings.MEDIA_ROOT, MB_PUBLISHED_ROOT)

MB_VERSIONS_ROOT = getattr(settings, "MEDIA_BROWSER_VERSION_ROOT", MB_ROOT)

MB_VERSIONS = getattr(
    settings,
    "MEDIA_BROWSER_VERSIONS",
    {
        "original": "original",
        "thumbnail": {"width": 200, "height": 200, "format": "webp"},
    },
)

MB_IMAGE_EXTENSIONS = getattr(
    settings,
    "MEDIA_BROWSER_IMAGE_EXTENSIONS",
    [
        "jpg",
        "png",
        "gif",
        "webp",
        "tiff",
        "psd",
        "raw",
        "bmp",
        "heif",
        "indd",
        "jpeg",
    ],
)

MB_NODE_PAGINATION = getattr(
    settings,
    "MEDIA_BROWSER_NODE_PAGINATION",
    "rest_mediabrowser.paginations.DefaultPagination",
)

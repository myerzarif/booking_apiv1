from io import BytesIO
from django.core.files.storage import default_storage
from django.db import models
from django.conf import settings
from django.utils import timezone
from rest_framework import exceptions
from secrets import token_urlsafe
from django.utils.translation import ugettext
from PIL import Image
import filetype
import logging
import uuid
import openpyxl
from common.models import BaseModel
from config.limiter import is_limit_upload_file

logger = logging.getLogger("project.file.upload")


# Create your models here.
class FileManager(models.Manager):

    # TODO : Check Conditions

    def save_files(self, files, allow_formats=[], created_by=None):
        # Check all file format is correct
        for file in files:
            allow_file, file_format = self.check_file_format(
                file, allow_formats=allow_formats)
            if not allow_file:
                logger.warning("Not Allowed File in Uploading", extra={
                    "file_format": file_format,
                })
                raise exceptions.NotAcceptable(
                    ugettext("not_allow_file_format"))
        # save file formats
        obj_files = []
        for file in files:
            file.seek(0)
            obj_file = self.save_file(
                file=file,
                allow_formats=allow_formats,
                created_by=created_by
            )
            obj_files.append(obj_file)

        return obj_files

    def save_thumbnail(self, thumbnail_file, thumbnail_size, file_format, token_file, obj_file):
        path_file_thumbnail = settings.FILES_PATH / "thumbnail" / \
            file_format / f"{token_file}.{file_format}"  # URL
        thumbnail_path = str(path_file_thumbnail)
        obj_file.thumbnail_path = thumbnail_path
        obj_file.thumbnail_size = thumbnail_size

        default_storage.save(thumbnail_path, thumbnail_file)
        obj_file.save()

    def save_file(self, file, allow_formats=[], sub_dir="", ratio=None, created_by=None):
        allow_file, file_format = self.check_file_format(
            file, allow_formats=allow_formats)
        file_name = file.name
        file_size = file.size
        thumbnail = None
        if not allow_file:
            logger.warning("Not Allowed File in Uploading", extra={
                "file_format": file_format,
            })
            raise exceptions.NotAcceptable(ugettext("not_allow_file_format"))
        if ratio:
            self.check_ratio_image(file, ratio)
        if file_format in ["png", "jpg", "jpeg"]:
            file, file_size = self.compress_image(file, file_format)
            thumbnail, thumbnail_size = self.thumbnail_image(file, file_format)

        token_file = token_urlsafe(50)
        path_file = settings.FILES_PATH / sub_dir / \
            file_format / f"{token_file}.{file_format}"  # URL
        obj_file = self.create(
            path=str(path_file),
            size=file_size,
            format=file_format,
            name=file_name,
            created_by=created_by,
        )
        if thumbnail:
            self.save_thumbnail(
                thumbnail, thumbnail_size, file_format, token_file, obj_file)

        if created_by:
            limited = is_limit_upload_file(created_by.email, file_size)
        else:
            limited = is_limit_upload_file("anonymous", file_size)
        if limited:
            raise exceptions.Throttled(
                detail=ugettext("upload_file_limited_max_size"))

        default_storage.save(obj_file.path, file)
        return obj_file

    def compress_image(self, file, format):
        save_format = "JPEG"
        if format == "png":
            save_format = "PNG"
        new_content = BytesIO()
        file.seek(0)
        img = Image.open(file)
        img.save(new_content,
                 save_format, optimize=True, quality=50)
        file_size = new_content.getbuffer().nbytes
        return new_content, file_size

    def check_ratio_image(self, file, ratio):
        file.seek(0)
        img = Image.open(file)
        width = img.size[0]
        height = img.size[1]
        img_ratio = width/height
        if abs(ratio - img_ratio) > 0.7:
            raise exceptions.NotAcceptable(ugettext("bad_image_ratio"))

    def thumbnail_image(self, file, format):
        save_format = "JPEG"
        if format == "png":
            save_format = "PNG"
        new_content = BytesIO()
        file.seek(0)
        img = Image.open(file)
        img.thumbnail((300, 300))
        img.save(new_content,
                 save_format, optimize=True, quality=50)
        file_size = new_content.getbuffer().nbytes
        return new_content, file_size

    def check_file_format(self, file, allow_formats=[]):
        if "xlsx" in allow_formats:
            try:
                openpyxl.load_workbook(file)
                return True, "xlsx"
            except Exception as e:
                pass
            file.seek(0)
        kind = filetype.guess(file)
        if kind and kind.extension in allow_formats:
            return True, kind.extension
        if kind:
            return False, kind.extension
        return False, ""


class File(BaseModel):

    path = models.TextField()
    size = models.IntegerField()
    format = models.CharField(max_length=20)
    name = models.CharField(max_length=250)
    thumbnail_path = models.TextField(
        verbose_name="thumbnail", blank=True, null=True)
    thumbnail_size = models.IntegerField(null=True)

    created_by = models.ForeignKey(
        "account.User",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL
    )
    modified_by = models.ForeignKey(
        "account.User",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL
    )

    objects = FileManager()

    def __str__(self):
        return self.path

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["-created_at"]

    @property
    def path_url(self):
        if self.path:
            return default_storage.url(self.path)
        return None

    @property
    def thumbnail_path_url(self):
        if self.thumbnail_path:
            return default_storage.url(self.thumbnail_path)
        return None

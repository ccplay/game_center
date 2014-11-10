from django.db import models
from mezzanine.core.fields import FileField
from django.utils.timezone import now
import os
from mezzanine.core.models import TimeStamped, Ownable
from toolkit.helpers import sync_status_from
from model_utils.tracker import FieldTracker
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.conf import settings
from video.fields import VideoFileField
from video.storage import default_storage

VIDEO_DIRECTORY_DTFORMAT = 'videos/%Y/%m/%d/%H%M-%S-%f'


def video_upload_to(instance, filename):
    workspace_by_created(instance)
    basename = os.path.basename(filename)
    return "%s/%s" % (instance.workspace.name, basename)


def workspace_by_created(instance):
    if not str(instance.workspace):
        if not instance.created:
            instance.created = now().astimezone()
        else:
            instance.created = instance.created.astimezone()
        sd = instance.created
        instance.workspace = sd.strftime(VIDEO_DIRECTORY_DTFORMAT)


class Video(TimeStamped,
            Ownable,
            models.Model):

    class Meta:
        verbose_name_plural = verbose_name = '视频'
        index_together = (
            ('created', ),
            ('user', 'created', ),
        )

    preview = models.ImageField(upload_to=video_upload_to,
                                storage=default_storage,
                                default='',
                                blank=True,
                                max_length=500)

    title = models.CharField(max_length=50)

    workspace = FileField(default='',
                          blank=True,
                          max_length=500,
                          format='File')

    file = VideoFileField(storage=default_storage,
                          upload_to=video_upload_to,
                          max_length=500)

    tracker = FieldTracker()

    def __str__(self):
        return self.title

    def sync_status(self):
        return sync_status_from(self)

    def save(self, *args, **kwargs):
        workspace_by_created(self)
        return super(Video, self).save(*args, **kwargs)



#@receiver(pre_save, sender=Video)
def video_file_thumbnail(sender, instance, *args, **kwargs):
    from converter import Converter
    if not instance.pk and instance.file:
        c = Converter()
        shotname = "%s/shot.png" % instance.workspace.name
        c.thumbnail(instance.file.path, 1,
                    os.path.join(settings.MEDIA_ROOT, shotname))
        instance.preview = shotname


@receiver(post_save, sender=Video)
def video_make_workspace(sender, instance, created, *args, **kwargs):
    if created:
        path = os.path.join(settings.MEDIA_ROOT, str(instance.workspace))
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)



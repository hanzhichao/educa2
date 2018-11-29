from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .fields import OrderField


class Subject(models.Model):
    title = models.CharField("标题", max_length=200)
    slug = models.SlugField("链接", max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User, related_name='course_created', on_delete=models.CASCADE, verbose_name="所有者")
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE, verbose_name="所属主题")
    title = models.CharField("标题", max_length=200)
    slug = models.SlugField("链接", max_length=200, unique=True)
    overview = models.TextField("概述")
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE, verbose_name="所属课程")
    title = models.CharField("标题", max_length=200)
    description = models.TextField("描述", blank=True)
    order = OrderField(for_fields=['course'], blank=True)

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)

    class Meta:
        ordering = ['order']


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE, verbose_name="所属模块")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': ('text', 'file', 'image', 'video')},
                                     verbose_name = "内容类型")
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']



class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE, verbose_name="所有者")
    title = models.CharField("标题", max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string('courses/content/{}.html'.format(self._meta.model_name), {'item': self})


class Text(ItemBase):
    content = models.TextField("文本内容")


class File(ItemBase):
    file = models.FileField("上传文件", upload_to='files')


class Image(ItemBase):
    file = models.FileField("上传文件", upload_to='images')


class Video(ItemBase):
    url = models.URLField("视频地址")


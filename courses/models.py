from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .fields import OrderField

class Subject(models.Model):
    """ Модель название предмета """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']


    def __str__(self):
        return self.title


class Course(models.Model):
    """ Модель курса """
    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,
                                      related_name='courses_joined',
                                      blank=True)
    
    class Meta:
        """ Сортирует """
        ordering = ['-created']


    def __str__(self):
        return self.title


class Module(models.Model):
    """ Модуль курса """
    course = models.ForeignKey(
        Course, related_name='modules', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering =['order']

    def __str__(self):
        return f'{self.order}. {self.title}'




class Content(models.Model):
    """ Модель контент содержит: text, file, image, video """
    module = models.ForeignKey(
        Module,
        related_name='contents',
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={ 'model__in': (
                        'text',
                        'image',
                        'video',
                        'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])
    
    class Meta:
        ordering = ['order']



class ItemBase(models.Model):
    """ 
    Абстрактная модель в которой определяются поля: 
        owner, title, created, updated. Указанные поля
        будут общие для всех типов содержимого.
    """
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        abstract = True
    
    def __str__(self) -> str:
        return self.title

class Text(ItemBase):
    """ Для хранения текстового содержимого """
    file = models.FileField(upload_to='files')

class File(ItemBase):
    """ Для хранения файлов. """
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    """ Для хранения файлов изображений """
    file = models.FileField(upload_to='image')

class Video(ItemBase):
    """ Для хранения видео. """
    url = models.URLField()
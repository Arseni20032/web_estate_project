from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True)
    timezone = models.CharField(max_length=50, default='UTC')

    def __str__(self):
        return self.username


class Buyer(models.Model):
    phone_number_regex = RegexValidator(regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$')
    phone_number = models.CharField(max_length=255, validators=[phone_number_regex])
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)  # один юзер является одним покупателем
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания записи
    updated_at = models.DateTimeField(auto_now=True)  # Дата обновления записи

    def __str__(self):
        return self.full_name


class EstateType(models.Model):
    type_estate = models.CharField(max_length=255)

    def __str__(self):
        return self.type_estate


class Owner(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания записи
    updated_at = models.DateTimeField(auto_now=True)  # Дата обновления записи

    def __str__(self):
        return self.full_name


class Employee(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    deal_count = models.IntegerField()
    buyers = models.ManyToManyField(Buyer,
                                    through='Deal')  # множество сотрудников имеет связь с множеством покупателей через модель сделок
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания записи
    updated_at = models.DateTimeField(auto_now=True)  # Дата обновления записи
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    responsibilities = models.CharField(max_length=255, default="Sales manager")

    def __str__(self):
        return self.full_name


class Estate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    creation_date = models.DateField(auto_now_add=True)
    square = models.FloatField()
    number_rooms = models.IntegerField()
    ceiling_height = models.FloatField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    buyer = models.ManyToManyField(Buyer)
    responsible_employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    estate_type = models.ForeignKey(EstateType, on_delete=models.CASCADE)
    cost = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания записи
    updated_at = models.DateTimeField(auto_now=True)  # Дата обновления записи

    def __str__(self):
        return self.name


class Deal(models.Model):
    estate = models.OneToOneField(Estate, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    cost = models.FloatField()
    deal_date = models.DateField(auto_now_add=True)
    deal_date_end = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания записи
    updated_at = models.DateTimeField(auto_now=True)  # Дата обновления записи


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    photo = models.ImageField(upload_to='post/%Y/%m/%d/', blank=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Генерируем slug на основе title
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class JobVacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    text = models.TextField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    archived_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code

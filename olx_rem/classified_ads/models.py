from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.db import models
from django.db.models.signals import post_delete

from mptt.models import MPTTModel, TreeForeignKey


# file_system = FileSystemStorage(location='/media/photos')


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = ('parent', 'slug',)
        verbose_name_plural = 'categories'

    def get_slug_list(self):
        # try:
        ancestors = self.get_ancestors(include_self=True)
        # except:
        #     ancestors = []
        # else:
        ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i + 1]))
        return slugs[-1]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ItemImage(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='item_photos')


@receiver(post_delete, sender=ItemImage)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = TreeForeignKey('Category', on_delete=models.CASCADE)
    description = models.CharField(max_length=5000)
    # photos = models.ForeignKey(ItemImage, on_delete=models.CASCADE, related_name='item_photos')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    negotiable = models.BooleanField(default=False)

    def __str__(self):
        return self.name

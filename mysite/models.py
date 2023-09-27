from django.db import models
from django.utils.text import slugify

from mptt.models import MPTTModel, TreeForeignKey

class Product(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(unique=True)
    description = models.TextField(blank=True,null=True)
    category    = models.ForeignKey(
        'Category',
        related_name="products",
        on_delete=models.CASCADE
    ) 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return self.slug
    
    def __str__(self): 
      return f"[{self.title}] {self.category}"

class Category(MPTTModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"   

    def __str__(self):                           
        full_path = [self.name]            
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])
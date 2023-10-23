

from django.db import models

# Create your models here.
from django.db import models
from main.models import Author, CustomUser
from polymorphic.models import PolymorphicModel
from django.db.models import TextField, ImageField


class Publisher(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=150, primary_key=True)

    def __str__(self):
        return self.name



class Piece(models.Model):
    isbn = models.CharField(max_length=150, primary_key=True, blank=True)
    name = models.CharField(max_length=150)
    pages = models.IntegerField(null=True, blank=True)
    introduction = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    published_at = models.DateField()
    
    WRITING_STATUS = [
        ('A', 'Announced'),
        ('C', 'Completed'),
        ('DE', 'Deleted'),
        ('DR', 'Dropped'),
        ('E', 'Editing'),
        ('H', 'Hiatus'),
        ('ON', 'On-going'),
        ('OS', 'One Shot'),
        ('T', 'Translating'),
    ]

   # TYPE = [
   #     ('T', 'Text'), 
  #      ('I', 'Image'),
  #  ]
    
#type = models.CharField(max_length=2, choices=TYPE, null=True, blank=True)
    status = models.CharField(max_length=2, choices=WRITING_STATUS, null=True, blank=True)

    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True)

    author = models.ManyToManyField(Author, related_name='author')
    genre = models.ManyToManyField(Genre, related_name='pieces')

    def save(self, *args, **kwargs):
        if not self.isbn:
            self.isbn = self.name
        super(Piece, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.isbn}"



class Chapter(models.Model):
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='piece')
    name = models.CharField(max_length=150)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f" {self.name}{self.piece}" 


class PageContent(PolymorphicModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class TextContent(PageContent):
    text = TextField()

class ImageContent(PageContent):
    image = ImageField()

class Page(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='chapter')
    content = models.ForeignKey(PageContent, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.chapter



class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='comments', null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='comments', null=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='comments', null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content} {self.user.username}"


# piece = Piece.objects.get(id=1)  # Substitua 1 pelo ID do objeto Piece que você deseja

# all_pages = []
# for chapter in piece.chapters.all():
#     for page in chapter.pages.all():
#         all_pages.append(page)






# class TextPage(models.Model):
#     content = models.TextField()
#     chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='pages')

# class ImagePage(models.Model):
#     content = models.ImageField(upload_to='pages/')
#     chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='pages')














# class Chapter(models.Model):
#     name = models.CharField(max_length=150)
#     created_at = models.DateField(auto_now_add=True)
#     updated_at = models.DateField(auto_now=True)
#     TYPE = [
#         ('S', 'String'),
#         ('I', 'Image'),
#     ]
    
#     type = models.CharField(max_length=2, choices=TYPE, null=True, blank=True)

# class TextPage(models.Model):
#     chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='pages')
#     content = models.TextField()
#     created_at = models.DateField(auto_now_add=True)
#     updated_at = models.DateField(auto_now=True)
    

# class ImagePage(models.Model):
#     chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='pages')
#     content = models.ImageField(upload_to='pages/')
#     created_at = models.DateField(auto_now_add=True)
#     updated_at = models.DateField(auto_now=True)






# class Piece(models.Model):
#     isbn = models.CharField(max_length=150, primary_key=True, blank=True)
#     name = models.CharField(max_length=150)
#     pages = models.IntegerField(null=True, blank=True)
#     introduction = models.TextField()
#     created_at = models.DateField(auto_now_add=True)
#     updated_at = models.DateField(auto_now=True)
#     published_at = models.DateField()
    
#     WRITING_STATUS = [
#         ('A', 'Announced'),
#         ('C', 'Completed'),
#         ('DE', 'Deleted'),
#         ('DR', 'Dropped'),
#         ('E', 'Editing'),
#         ('H', 'Hiatus'),
#         ('ON', 'On-going'),
#         ('OS', 'One Shot'),
#         ('T', 'Translating'),
#     ]
    
#     publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
#     status = models.CharField(max_length=2, choices=WRITING_STATUS, null=True, blank=True)
#     author = models.ManyToManyField(Author, on_delete=models.CASCADE)
#     genre = models.ManyToManyField(Genre, related_name='pieces')

#     def save(self, *args, **kwargs):
#         if not self.isbn:
#             self.isbn = self.name
#         super(Piece, self).save(*args, **kwargs)
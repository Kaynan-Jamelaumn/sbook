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
        ('Announced', 'Announced'),
        ('Completed', 'Completed'),
        ('Deleted', 'Deleted'),
        ('Dropped', 'Dropped'),
        ('Editing', 'Editing'),
        ('Hiatus', 'Hiatus'),
        ('On-going', 'On-going'),
        ('One Shot', 'One Shot'),
        ('Translating', 'Translating'),
    ]

    OFFICIAL_CHOICES = [
        ('Official', 'Official'),
        ('Anonymous', 'Anonymous'),
    ]

    PIECE_TYPES = [
        ('Manga', 'Manga'),
        ('Manhwa', 'Manhwa'),
        ('Manwa', 'Manwa'),
        ('Novel', 'Novel'),

    ]

    is_official = models.CharField(
        max_length=10, choices=OFFICIAL_CHOICES, default='official', null=False, blank=False)

    status = models.CharField(
        max_length=20, choices=WRITING_STATUS, null=False, blank=False)

    piece_type = models.CharField(
        max_length=20, choices=PIECE_TYPES, null=False, blank=False)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, null=False)

    author = models.ManyToManyField(Author, blank=True)
    custom_user = models.ManyToManyField(
        CustomUser, blank=True, null=True),
    genre = models.ManyToManyField(Genre, related_name='pieces')

    def save(self, *args, **kwargs):
        if not self.isbn:
            self.isbn = self.name

        super(Piece, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.isbn}"


class Chapter(models.Model):
    piece = models.ForeignKey(
        Piece, on_delete=models.CASCADE, related_name='piece')
    name = models.CharField(max_length=150)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" {self.name}{self.piece.name}"


class PageContent(PolymorphicModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TextContent(PageContent):
    text = models.TextField()


class ImageContent(PageContent):
    image = models.ImageField(upload_to='images/')


class Page(models.Model):
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, related_name='chapter')
    content = models.ForeignKey(PageContent, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Page {self.id}"


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)
    piece = models.ForeignKey(
        Piece, on_delete=models.CASCADE, related_name='comments', null=True)
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, related_name='comments', null=True)
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='comments', null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content} {self.user.username}"


class PieceAnotation(models.Model):
    summary = models.TextField(null=True, blank=True, max_length=3000)
    STATUS_CHOICES = [
        ('Finished', 'Finished'),
        ('Abandoned', 'Abandoned'),
        ('In Progress', 'In Progress'),
        ('Paused', 'Paused'),
        ('Hoping to Start', 'Hoping to Start')
    ]
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=20, null=False, blank=False)
    summary = models.TextField(null=True, blank=True, max_length=3000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'piece'], name='unique_piece_anotation_for_user')
        ]

from django.db import models

# Create your models here.
class Image(models.Model):
  url = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')
  def __unicode__(self):
    return self.url

class Tag(models.Model):
  name = models.CharField(max_length=50)
  count = models.IntegerField()
  def __unicode__(self):
    return self.name

class ImgTagRel(models.Model):
  image = models.ForeignKey(Image)
  tag = models.ForeignKey(Tag)
  def __unicode__(self):
    return '{0} to {1}'.format(self.image.__str__(), self.tag.__str__())

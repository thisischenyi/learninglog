from django.db import models

# Create your models here.
class Topic(models.Model):
	"""user's learning topic"""
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		"""return text content"""
		return self.text

class Entry(models.Model):
	"""the entries relate to one topic"""
	topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
	text = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'entries'

	def __str__(self):
		"""return entry content"""
		if len(self.text)>=50:
			return self.text[:50] + "..."
		else:
			return self.text
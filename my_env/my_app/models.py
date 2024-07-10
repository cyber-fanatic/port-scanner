from django.db import models

class PortScanResult(models.Model):
    host_name = models.CharField(max_length=255)
    open_ports = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.host_name

 

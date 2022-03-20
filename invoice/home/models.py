from distutils.archive_util import make_zipfile
from django.db import models
import datetime


# Create your models here.

class UserInput(models.Model):
    customer_details = models.CharField(max_length=100)
    customer_address = models.CharField(max_length=100)
    customer_gst = models.CharField(max_length=20)
    customer_pan = models.CharField(max_length=20)
    customer_po = models.CharField(max_length=100)
    invoice_num = models.CharField(max_length=100,unique=True)
    invoice_date = models.DateField()
    candidate_name = models.CharField(max_length=100)
    candidate_designation = models.CharField(max_length=100)
    joining_date = models.DateField()
    due_date = models.DateField()
    candidate_ctc = models.CharField(max_length=100)
    ctc_percent = models.CharField(max_length=100)
    sac_code = models.CharField(max_length=100)
    amnt = models.CharField(max_length=100)
    igst_percent = models.CharField(max_length=100)
    igst_amnt = models.CharField(max_length=100)
    total_amt = models.CharField(max_length=100)
    total_amt_word = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    is_created = models.DateTimeField(auto_now_add=True, blank=True)
    is_modified = models.DateTimeField(null=True)

    class Meta:
        db_table = 'userinput'
        ordering = ['invoice_num']
        get_latest_by = 'invoice_num'

    def __str__(self):
        return self.invoice_num

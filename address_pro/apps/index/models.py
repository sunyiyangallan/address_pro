from django.db import models
from address_pro.utils.models import BaseModel
from django.utils.html import format_html
from django.contrib.auth.models import AbstractUser
import uuid as get_uuid



class AddressUser(BaseModel):
    uuid = models.UUIDField(verbose_name='用户唯一标识', default=get_uuid.uuid4)

from django.contrib import admin
from .models import Sequence, Primer, Setting, AnnealedPrimer, PrimerProduct, ResultProduct, ChimericResultProduct, ResultString, ResultSequenceString

# Register your models here.
admin.site.register(Sequence)
admin.site.register(Primer)
admin.site.register(Setting)
admin.site.register(AnnealedPrimer)
admin.site.register(PrimerProduct)
admin.site.register(ResultProduct)
admin.site.register(ChimericResultProduct)
admin.site.register(ResultString)
admin.site.register(ResultSequenceString)




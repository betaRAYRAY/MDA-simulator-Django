from django.forms import ModelForm
from .models import Sequence, Primer, Setting, AnnealedPrimer, PrimerProduct, ResultProduct, ChimericResultProduct, ResultString

class SequenceForm(ModelForm):
    class Meta:
        model = Sequence
        fields = '__all__'

class PrimerForm(ModelForm):
    class Meta:
        model = Primer
        fields = '__all__'

class SettingForm(ModelForm):
    class Meta:
        model = Setting
        fields = '__all__'

class AnnealedPrimerForm(ModelForm):
    class Meta:
        model = AnnealedPrimer
        fields = '__all__'

class PrimerProductForm(ModelForm):
    class Meta:
        model = PrimerProduct
        fields = '__all__'

class ResultProductForm(ModelForm):
    class Meta:
        model = ResultProduct
        fields = '__all__'

class ChimericResultProductForm(ModelForm):
    class Meta:
        model = ChimericResultProduct
        fields = '__all__'

class ResultStringForm(ModelForm):
    class Meta:
        model = ResultString
        fields = '__all__'

        
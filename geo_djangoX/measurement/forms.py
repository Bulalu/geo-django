from .models import Measurement
from django.forms import ModelForm


class MeasurementForm(ModelForm):
    class Meta:
        model = Measurement
        fields = ('destination',)
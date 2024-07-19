from django import forms

from .models import Schedule


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields= "__all__"
        exclude = ["doctor"]

    start_time = forms.TimeField( required=True, 
                                 label="The Start Time",
                                 widget=forms.TimeInput(attrs={'type':'time'}),
                                 input_formats=['%H:%M']
                                )
    end_time = forms.TimeField(required=True, label="The End Time",
                                widget=forms.TimeInput(attrs={'type':'time'}),
                                input_formats=['%H:%M']
                                )
    
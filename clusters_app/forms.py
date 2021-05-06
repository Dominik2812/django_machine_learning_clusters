from django import forms


class NumberInput(forms.TextInput):
    input_type = "number"


class BaseDataInputForm(forms.Form):
    base_data = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control m-10 p-1 text-center",
                "placeholder": "url of the csv file containing your data",
            }
        )
    )
    number_of_expected_clusters = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control m-10 p-1 text-center",
                "placeholder": "how many clusters do you expect?",
                "step": 1,
                "min": 0,
            }
        ),
    )



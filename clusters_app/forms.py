from django import forms


class BaseDataInputForm(forms.Form):
    base_data = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control m-3 p-3",
                "placeholder": "url of the csv file containing your data",
            }
        )
    )
    number_of_expected_clusters = forms.IntegerField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control m-3 p-3",
                "placeholder": "how many clusters do you expect?",
            }
        ),
    )


class NumberOfExpectedClustersForm(forms.Form):
    number_of_expected_clusters = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control m-3 p-3",
                "placeholder": "how many clusters do you expect?",
            }
        )
    )

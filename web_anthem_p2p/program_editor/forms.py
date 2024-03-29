from django import forms
from django.db import models

class InputForm(forms.Form):
    time_limit = forms.CharField(max_length=100, required=False)
    original_program = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"}), 
        initial="composite(I*J) :- I>1, J>1.\nprime(I) :- I = 2..n, not composite(I).")
    alternative_program = forms.CharField(
        widget=forms.Textarea(), 
        initial="composite(I*J) :- I = 2..n, J = 2..n.\nprime(I) :- I = 2..n, not composite(I).")
    user_guide = forms.CharField(
        widget=forms.Textarea(),
        initial="input: n -> integer.\nassume: n > 1.\noutput: prime/1.")
    helper_lemmas = forms.CharField(
        widget=forms.Textarea(), 
        initial="lemma: forall X, N1, N2 ( (N1 > 1 and N2 > 1 and X = N1 * N2) -> (N1 <= X and N2 <= X) ).\nlemma:  forall X (prime(X) <-  exists N1 (exists N2 (N2 = n and 2 <= N1 and N1 <= N2) and not composite_1(N1) and X = N1)).\nlemma:  forall X (prime(X)  -> exists N1 (exists N2 (N2 = n and 2 <= N1 and N1 <= N2) and not composite_1(N1) and X = N1)).",
        required=False)


class OutputForm(forms.Form):
    time_limit = forms.CharField(max_length=100, required=False)
    original_program = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"}), 
        initial="composite(I*J) :- I>1, J>1.\nprime(I) :- I = 2..n, not composite(I).")
    alternative_program = forms.CharField(
        widget=forms.Textarea(), 
        initial="composite(I*J) :- I = 2..n, J = 2..n.\nprime(I) :- I = 2..n, not composite(I).")
    user_guide = forms.CharField(
        widget=forms.Textarea(),
        initial="input: n -> integer.\nassume: n > 1.\noutput: prime/1.")
    helper_lemmas = forms.CharField(
        widget=forms.Textarea(), 
        initial="lemma: forall X, N1, N2 ( (N1 > 1 and N2 > 1 and X = N1 * N2) -> (N1 <= X and N2 <= X) ).\nlemma:  forall X (prime(X) <-  exists N1 (exists N2 (N2 = n and 2 <= N1 and N1 <= N2) and not composite_1(N1) and X = N1)).\nlemma:  forall X (prime(X)  -> exists N1 (exists N2 (N2 = n and 2 <= N1 and N1 <= N2) and not composite_1(N1) and X = N1)).",
        required=False)
    output = forms.CharField(widget=forms.Textarea(attrs={"id": "output", "readonly": "readonly"}))

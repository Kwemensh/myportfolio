from django import forms

SERVICE_CHOICES = [
    ("web_dev", "Web Design & Development"),
    ("seo", "SEO & Content Strategy"),
    ("automation", "AI & Automation"),
    ("branding", "Logo & Branding"),
    ("maintenance", "Site Care & Performance"),
]

class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=120, label="Full Name")
    email = forms.EmailField(label="Email")
    company = forms.CharField(max_length=120, required=False, label="Company (optional)")
    message = forms.CharField(widget=forms.Textarea, label="Message")
    services = forms.MultipleChoiceField(
        choices=SERVICE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Services Interested In"
    )

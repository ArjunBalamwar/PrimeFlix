from django import forms
from django.db.models import fields
from .models import Post

PREGNANT=[('Yes', 'Yes'), ('No', 'No')]
WEIGHT = [('light', 'till 30'), ('medium', 'from 30 to 70'), ('heavy', "above 70")]
GENDER = [('Male', 'Male'),('Female', 'Female'), ('Other', 'Other')]
CITY = [('Mumbai', 'Mumbai'), ('Pune', 'Pune'), ('Nagpur', 'Nagpur'), ('Delhi', 'Delhi'), ('Noida', 'Noida'), ('Chandigarh', 'Chandigarh'), ('Amritsar', 'Amritsar')]
BOOKING = [(1, 'Allow Covid Bed Registration'),(2, 'Allow Bed Registration'), (3, 'Delete Entry')]
SCHEME = [('Life Insurance', 'Life Insurance'), ('Govt. Scheme','Govt. Scheme'), ('MSME Loan','MSME Loan')]
AREA =[('Andheri','Andheri'),('Worli','Worli'),('Bandra','Bandra'),('Breach Candy','Breach Candy'),('Thane','Thane'),('Ghatkopar','Ghatkopar'),('Friends Colony','Friends Colony'),('Hinjawadi','Hinjwadi'),('Chandini Chowk','Chandani Chowk')]
OPTION1 = [(1, '👍🏼'), (2, '➕')]
OPTION2 = [(1, '👍🏼'), (2, '➖')]
OPTION3 = [(1, '👎🏼'), (2, '➕')]
OPTION4 = [(1, '👎🏼'), (2, '➖')]
# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ('name', 'content','weight', "pregnant", "anemia", "infectious_diseases", "doctors_prescription",
#             "days", "test", "covid"
#         )
#         widgets = {

#             'name' : forms.TextInput(attrs={'class':'form-control'}),
#             # 'category': forms.Select(choices=choice_list,attrs={'class':'form-control'}),
#             'content': forms.Textarea(attrs={'class':'form-control'}),
#             'covid_cap' : forms.Select(choices=ANEMIA, attrs={'class':'form-control'}),
#             'norm_cap': forms.Select(choices=ANEMIA,attrs={'class':'form-control'}),
        
#         }

# class PostForm(forms.ModelForm):
#     name =forms.CharField()
#     content=forms.Textarea()
#     covid_cap=forms.IntegerField(label='Number of covid beds?')
#     norm_cap = forms.IntegerField(label='Number of covid beds?')
#     city = forms.CharField(widget=forms.Select(choices=CITY))
#     area = forms.CharField(widget=forms.Select(choices=AREA))
#     address = forms.Textarea()

#     class Meta:
#         model = Post 
#         fields = ['name', 'content', 'covid_cap', 'norm_cap', 'city', 'area',
#                    'address'
#                  ]

# class BedForm(forms.ModelForm):
#     aadhar_number =forms.IntegerField()
#     phone_number =forms.IntegerField()
#     email = forms.EmailField()
#     name=forms.CharField(label='What is your name?')
#     address=forms.CharField(label='What is your Address?')
#     # proof=forms.ImageField()
#     city=forms.CharField(label='What is your City?', widget=forms.Select(choices=CITY))
#     pin_code =forms.IntegerField()
#     gender=forms.CharField(label='What is your gender?',widget=forms.Select(choices=GENDER))
#     age =forms.IntegerField()
#     co_mobidity=forms.CharField(label='What are your comobidity?',widget=forms.Select(choices=PREGNANT))
#     ambulance_required=forms.CharField(label='Do you require an ambulance?',widget=forms.Select(choices=PREGNANT))
#     scheme=forms.CharField(label='Scheme to apply for',widget=forms.Select(choices=SCHEME))

#     # preferance=forms.CharField(label='What is your gender?',widget=forms.Select(choices=GENDER))
#     # health_centre=forms.CharField(label='What is your gender?',widget=forms.Select(choices=GENDER))
#     # district=forms.CharField(max_length=10)
#     # Hospital=forms.CharField(max_length=10, label='Nearby hospitals?')

#     tested = forms.CharField(label='Was your COVID test positive?',widget=forms.Select(choices=PREGNANT))

#     # is_donor = forms.BooleanField(required=False)

#     symptoms = forms.Textarea()

#     class Meta:
#         model= Post
#         fields=('aadhar_number', 'name', 'email', 'phone_number', 'address' , 'city', 'pin_code',  'age', 'gender', 
#              'co_mobidity', 'ambulance_required', 'scheme', 'tested','symptoms'
#         #   'proof',
#         )
class PostForm(forms.ModelForm):
    class Meta:
        model= Post
        fields = ["name", "type", "genres", "rating", "director", "cast", "country", "duration", "release_date", "likes", "content"]


class PostForm1(forms.ModelForm):
    choice=forms.CharField(widget=forms.Select(choices=OPTION1))
    class Meta:
        model= Post
        fields = ["choice"]

class PostForm2(forms.ModelForm):
    choice=forms.CharField(widget=forms.Select(choices=OPTION2))
    class Meta:
        model= Post
        fields = ["choice"]

class PostForm3(forms.ModelForm):
    choice=forms.CharField(widget=forms.Select(choices=OPTION3))
    class Meta:
        model= Post
        fields = ["choice"]

class PostForm4(forms.ModelForm):
    choice=forms.CharField(widget=forms.Select(choices=OPTION4))
    class Meta:
        model= Post
        fields = ["choice"]

class Booking(forms.ModelForm):
    choice=forms.CharField(widget=forms.Select(choices=BOOKING))
    class Meta:
        model= Post
        fields = ["choice"]

class Search(forms.ModelForm):
    search=forms.CharField()
    class Meta:
        model= Post
        fields = ["search"]


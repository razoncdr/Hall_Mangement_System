from django import forms
from django.forms import DateInput, ModelChoiceField
from .models import *
from HallManagementApp.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
 

class LoginForm(forms.Form):    
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control',},))
    password = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control', 'type': 'password',},))


class UserGroupForm(UserCreationForm):
    id = forms.IntegerField()
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    is_active = models.BooleanField(default=True)
    user = User()
    group = Group()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['fullName', 'birthDate', 'picture', 'phone', 'email']  # Only include fields that need to be validated and updated

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disable the email field explicitly
        self.fields['email'].disabled = True  # Email should not be updated

        # Mark fields as required (optional for validation, depending on your requirements)
        self.fields['fullName'].required = True
        self.fields['birthDate'].required = True
        self.fields['phone'].required = True

        # Customize the birthDate field to use a DateInput widget
        self.fields['birthDate'].widget = forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',  # HTML5 date picker
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD',  # Placeholder text
            }
        )

        # Customize the phone field widget
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Phone number'})

        # Customize the picture field if necessary (e.g., limit size or type)
        self.fields['picture'].widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        # Override clean() to prevent validation of fields not included in the `fields` list
        cleaned_data = super().clean()
        # If you want to skip certain fields, you can remove them from the cleaned_data
        # For example, if `email` is not in the form but still part of the model:
        cleaned_data.pop('email', None)
        return cleaned_data


class UserFilterForm(forms.Form):
    username = forms.CharField(required=False, label='Username', widget=forms.TextInput(attrs={'class':'form-control-sm',},))
    email = forms.CharField(required=False, label='Email Address', widget=forms.TextInput(attrs={'class':'form-control-sm',},))
    is_active = forms.ChoiceField(choices=[('1', 'Active'), ('0', 'Inactive')], required=False, label='Status', widget=forms.Select(attrs={'class':'form-select-sm',},))
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False, label='User Group', widget=forms.Select(attrs={'class':'form-select-sm',},))


class HallForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Hall
 
        # specify fields to be used
        fields = [
            "name",
        ]


class RoomForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Room
 
        # specify fields to be used
        fields = [
            "hall",
            "name",
            "capacity",
        ]


class BatchForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Batch
 
        # specify fields to be used
        fields = [
            "name",
        ]


class DepartmentForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Department
 
        # specify fields to be used
        fields = [
            "name",
        ]


class SessionForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Session
 
        # specify fields to be used
        fields = [
            "name",
        ]


class SemesterForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Semester
 
        # specify fields to be used
        fields = [
            "name",
        ]


class DormitoryApplicationsForm(forms.ModelForm):
    class Meta:
        model = DormitoryApplications
        fields = '__all__'  # Use all fields from the model

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        # Make picture field not required for updates
        if instance and instance.pk:
            self.fields['picture'].required = False
        

        # Add required attribute to form fields
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = 'required'

        self.fields['semester'] = forms.ChoiceField(choices=[(tag.value, tag.name) for tag in Semester_Status], 
                                                required=False,)
        self.fields['application_status'] = forms.ChoiceField(choices=[(tag.value, tag.name) for tag in Application_Status], 
                                                required=False,)
        self.fields['remarks'] = forms.CharField(widget=forms.Textarea(attrs={"rows":4}), required=False)
        self.fields['token'] = forms.CharField(required=False)
        # Set date input for birthDate field    
        self.fields['birthDate'].widget = DateInput()






class DormitoryApplicationsFilterForm(forms.Form):
    session = ModelChoiceField(queryset=Session.objects.order_by('-name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    batch = ModelChoiceField(queryset=Batch.objects.order_by('-name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    department = ModelChoiceField(queryset=Department.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    
    # Adding an "all" option to semester
    semester = forms.ChoiceField(choices=[(None, '------')] + [(tag.value, tag.name) for tag in Semester_Status], 
                            required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    
    registration_number = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class':'form-select-sm',},))
    date_from = forms.DateField(widget=DateInput(attrs={'class':'form-select-sm','type': 'date'}), required=True)
    date_to = forms.DateField(widget=DateInput(attrs={'class':'form-select-sm','type': 'date'}), required=True)
    
    # Displaying application status choices
    application_status = forms.ChoiceField(choices=[(None, '------')] + [(tag.value, tag.name) for tag in Application_Status], 
                            required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))


# class DormitoryApplicationsFilterForm(forms.ModelForm):
#     date_from = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
#     date_to = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

#     class Meta:
#         model = DormitoryApplications
#         fields = ['session', 'batch', 'department', 'semester', 'registration_number', 'application_status']
#         widgets = {
#             'application_status': forms.Select(),
#         }


class FeesHeadForm(forms.ModelForm):
    class Meta:
        model = FeesHead
        fields = ["title", "amount"]


class StudentForm(forms.ModelForm):
    room = ModelChoiceField(queryset=Room.objects.order_by('name').all())
    batch = ModelChoiceField(queryset=Batch.objects.order_by('-name').all())
    session = ModelChoiceField(queryset=Session.objects.order_by('-name').all())

    class Meta:
        model = Student
        fields = ["fullName", "registration_number", "room", "session", "batch", "semester", "department", "status",]
        # widgets = {
        #     "batch": forms.Select(attrs={"class": 'form-select-sm',}),
        #     "session": forms.Select(attrs={"class": 'form-select-sm',}),
        #     "room": forms.Select(attrs={"class": 'form-select-sm',}),
        #     "semester": forms.Select(attrs={"class": 'form-select-sm',}),
        #     "department": forms.Select(attrs={"class": 'form-select-sm',}),
        # }


class StudentFilterForm(forms.Form):
    hall = ModelChoiceField(queryset=Hall.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    room = forms.CharField(label='Room Number', required=False, widget=forms.TextInput(attrs={'class':'form-control-sm',}))
    batch = ModelChoiceField(queryset=Batch.objects.order_by('-name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    semester = ModelChoiceField(queryset=Semester.objects.order_by('name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    registration_number = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class':'form-control-sm',},))
    status = forms.ChoiceField(
        choices=[('', '------')] + list(STATUS),  # Concatenate properly
        required=False, 
        widget=forms.Select(attrs={'class':'form-select-sm'})
    )

    
class StudentFeeForm(forms.Form):
    feesHead = ModelChoiceField(queryset=FeesHead.objects.order_by('-title').all(), widget=forms.Select(attrs={'class':'form-select-sm',},))
    session = ModelChoiceField(queryset=Session.objects.order_by('-name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    batch = ModelChoiceField(queryset=Batch.objects.order_by('-name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    semester = ModelChoiceField(queryset=Semester.objects.order_by('name').all(), widget=forms.Select(attrs={'class':'form-select-sm',},))
    registration_number = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class':'form-control-sm',},))


class StudentFeeFilterForm(forms.Form):
    feesHead = ModelChoiceField(queryset=FeesHead.objects.order_by('-title').all(), required=False,widget=forms.Select(attrs={'class':'form-select-sm',},) )
    batch = ModelChoiceField(queryset=Batch.objects.order_by('-name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    hall = ModelChoiceField(queryset=Hall.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    semester = ModelChoiceField(queryset=Semester.objects.order_by('name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    registration_number = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class':'form-select-sm',},))
    From_Date = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm', 'value': datetime.datetime.now().strftime('%Y-%m-%d')},))
    To_Date = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'class':'form-control-sm', 'value': datetime.datetime.now().strftime('%Y-%m-%d')},))
    payment_Status = forms.ChoiceField(choices=[(None, '------')] + [(tag.value, tag.name) for tag in Payment_Status], 
                                required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))


class StudentFeeStatementForm(forms.Form):
    session = ModelChoiceField(queryset=Session.objects.order_by('-name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    batch = ModelChoiceField(queryset=Batch.objects.order_by('-name').all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    hall = ModelChoiceField(queryset=Hall.objects.all(), required=False, widget=forms.Select(attrs={'class':'form-select-sm',},))
    registration_number = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class':'form-select-sm',},))


class HallListFilterForm(forms.Form):
    hall = ModelChoiceField(queryset=Hall.objects.all(), required=False)


class RoomListFilterForm(forms.Form):
    room = forms.CharField(label='Room Number', required=False)
    hall = forms.ModelChoiceField(queryset=Hall.objects.all(), label='Hall', required=False)
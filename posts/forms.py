from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import LunchPost, Profile

TEXT_ATTRS  = {'class': 'fi'}
SELECT_ATTRS = {'class': 'fs'}
TEXTAREA_ATTRS = {'class': 'fta'}


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username (ใช้สำหรับ login)'
        self.fields['username'].widget.attrs.update({'class': 'fi', 'placeholder': 'เช่น 680XXXXX'})
        self.fields['password1'].label = 'รหัสผ่าน'
        self.fields['password1'].widget.attrs.update({'class': 'fi'})
        self.fields['password2'].label = 'ยืนยันรหัสผ่าน'
        self.fields['password2'].widget.attrs.update({'class': 'fi'})


class LunchPostForm(forms.ModelForm):
    class Meta:
        model = LunchPost
        fields = ['restaurant', 'area', 'meal', 'time', 'slots', 'note', 'image']
        widgets = {
            'restaurant': forms.TextInput(attrs={**TEXT_ATTRS, 'placeholder': 'เช่น โรงอาหารตึก IT'}),
            'area':       forms.TextInput(attrs={**TEXT_ATTRS, 'placeholder': 'เช่น ใกล้ BTS บางนา'}),
            'meal':       forms.Select(attrs=SELECT_ATTRS),
            'time':       forms.TextInput(attrs={**TEXT_ATTRS, 'placeholder': 'เช่น 12:00'}),
            'slots':      forms.NumberInput(attrs={**TEXT_ATTRS}),
            'note':       forms.Textarea(attrs={**TEXTAREA_ATTRS, 'rows': 3, 'placeholder': 'รายละเอียดเพิ่มเติม...'}),
        }
        labels = {
            'restaurant': 'ร้านอาหาร',
            'area':       'พื้นที่',
            'meal':       'มื้ออาหาร',
            'time':       'เวลา (น.)',
            'slots':      'จำนวนที่นั่ง',
            'note':       'หมายเหตุ',
            'image':      'รูปภาพ',
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'avatar', 'bio']
        labels = {
            'display_name': 'ชื่อที่แสดงในโพสต์',
            'avatar':       'รูปโปรไฟล์',
            'bio':          'แนะนำตัว',
        }
        widgets = {
            'display_name': forms.TextInput(attrs={**TEXT_ATTRS, 'placeholder': 'เช่น งานการ ไม่ทำ'}),
            'bio':          forms.Textarea(attrs={**TEXTAREA_ATTRS, 'rows': 3}),
        }
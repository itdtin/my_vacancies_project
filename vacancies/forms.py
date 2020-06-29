from django.forms import ModelForm
from django import forms

from .models import Application, Company, Vacancy


class MyApplicationForm(ModelForm):
    """Класс для формы отклика на вакансию"""
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']

    written_username = forms.CharField(max_length=100, label='Вас зовут')
    written_phone = forms.CharField(max_length=30, required=True, label='Ваш телефон')
    written_cover_letter = forms.CharField(widget=forms.Textarea, label='Сопроводительное письмо')


class MyCompanyForm(ModelForm):
    """Класс для формы отклика на вакансию"""

    class Meta:
        model = Company
        fields = ['name', 'location', 'logo', 'description', 'employee_count']

    name = forms.CharField(label='Название компании')
    location = forms.CharField(label='География')
    logo = forms.ImageField(label='Логотип', required=False, widget=forms.FileInput)
    description = forms.CharField(widget=forms.Textarea, label='Информация о компании')
    employee_count = forms.IntegerField(label='Количество человек в компании')


class MyVacancyForm(ModelForm):
    """Класс для формы добавления/редактирования вакансии"""
    title = forms.CharField(max_length=120, label='Название вакансии', initial='Новая вакансия')

    class Meta:
        model = Vacancy
        fields = ['title', 'skills', 'description', 'salary_min', 'salary_max', 'specialty']


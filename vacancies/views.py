from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from vacancies.models import Company, Specialty, Vacancy
from vacancies.forms import MyApplicationForm, MyCompanyForm, MyVacancyForm


class MainView(View):
    """Представление для главной"""

    def get(self, request):
        specialties = Specialty.objects.annotate(Count('vacancies'))
        companies = Company.objects.annotate(Count('vacancies'))
        context = {}
        context['specialties'] = specialties
        context['companies'] = companies
        return render(request, 'index.html', context=context)


class VacancyView(DetailView):

    """Класс представления для каждой вакансии"""
    model = Vacancy
    template_name = 'vacancies/vacancy.html'
    success_template = 'vacancies/sent.html'
    form_class = MyApplicationForm

    for field in form_class.base_fields:
        form_class.base_fields[field].widget.attrs = {'class': 'form-control'}

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            if form.is_valid():
                object = self.get_object()

                obj = form.save(commit=False)
                obj.user = request.user
                if not User.objects.filter(id=obj.user.id).first():
                    form.add_error('user', 'Зарегистрируйтесь, чтобы отправить отклик')
                    return render(request, self.template_name, {'form': form})
                obj.vacancy = object
                obj.save()
                # Переопределить модель или придумтаь валидацию на формат номера
                return redirect('send_vac', vacancy_id=obj.vacancy.id)

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        context['form'] = MyApplicationForm()
        return context


class AllVacanciesView(ListView):
    """Класс представления для всех вакансий"""

    model = Vacancy
    template_name = 'vacancies/vacancies.html'
    queryset = Vacancy.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AllVacanciesView, self).get_context_data(**kwargs)
        context['title'] = 'Все вакансии'
        return context


class CathegoryVacancies(ListView):
    """Класс представления для вакансий по категории"""
    model = Vacancy
    template_name = 'vacancies/vacancies.html'

    def get_queryset(self):
        cat = self.kwargs['cathegory_name']
        queryset = Vacancy.objects.filter(specialty__code=cat)

        if len(queryset) == 0:
            raise Http404()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(CathegoryVacancies, self).get_context_data(**kwargs)
        context['title'] = self.kwargs['cathegory_name']
        return context


class CompanyVacanciesView(DetailView):
    """Класс представления для вакансий по компании"""
    template_name = 'vacancies/company.html'
    model = Company


class VacancySendView(View):
    def get(self, request, vacancy_id):
        context = {}
        context['title'] = "Отклик отправлен | Джуманджи"
        context['id'] = vacancy_id
        return render(request, 'vacancies/sent.html', context=context)


class MyCompanyView(View):
    """Класс представления для моей компании(если есть) иначе для создания"""

    form_class = MyCompanyForm
    for field in form_class.base_fields:
        form_class.base_fields[field].widget.attrs = {'class': 'form-control'}
    form_class.base_fields['logo'].widget.attrs = {'class': 'custom-file-input'}

    def get(self, request):
        context = {}
        try:
            company = request.user.companies
            template_name = 'vacancies/mycompany_edit.html'
            context['title'] = "Моя компания | Джуманджи"
            form = MyCompanyForm()
            form.fields['name'].initial = company.name
            form.fields['location'].initial = company.location
            form.fields['logo'].initial = company.logo
            form.fields['description'].initial = company.description
            form.fields['employee_count'].initial = company.employee_count
            form.save(commit=False)

            context['form'] = form
        except ObjectDoesNotExist:
            template_name = 'vacancies/mycompany_create.html'
            context['title'] = "Создать карточку компании | Джуманджи"

        return render(request, template_name=template_name, context=context)

    def post(self, request):
        if request.method == 'POST':
            com = Company.objects.get(pk=request.user.companies.id)
            form = self.form_class(request.POST, request.FILES, instance=com)
            if form.is_valid():
                form.save()
                return redirect('mycompany')
            else:
                print(form.errors)
                return redirect('mycompany')


class MyCompanyCreateView(View):
    """Класс представления для страницы с предложением создать компаниб"""
    def get(self, request):
        user = request.user
        context = {}
        context['title'] = "Моя компания | Джуманджи"
        try:
            user.companies
        except:
            company = Company.objects.create(name='new', location='new_location', owner=user)
            #Компания создается сразу, пользователь редактирует уже существующую
            company.save()
        finally:
            return redirect('mycompany')


class MyCompanyVacanciesView(View):
    """Класс представления для вакансий моей компании"""
    template_name = 'vacancies/mycompany_vacancies.html'

    def get(self, request):
        user = request.user
        context = {}
        context['title'] = "Вакансии компании | Джуманджи"
        mycompany_vacancies = Vacancy.objects.filter(company=user.companies)
        context['mycompany_vacancies'] = mycompany_vacancies
        return render(request, template_name=self.template_name, context=context)


class MyCompanyOneVacancyView(VacancyView):
    """Класс представления для одной вакансии моей компании"""
    object = None

    def get(self, request, *args, **kwargs):
        self.object = super(VacancyView, self).get_object()
        context = super(MyCompanyOneVacancyView, self).get_context_data(**kwargs)
        try:
            vacancy = Vacancy.objects.filter(company=request.user.companies.id).filter(pk=self.object.id).first()
            context['object'] = vacancy
            return render(request, 'vacancies/vacancy.html', context=context)
        except ObjectDoesNotExist:
            raise Http404


class CreateVacancyView(View):
    """Класс пердставления для создания вакансии"""
    form_class = MyVacancyForm()
    for field in form_class.base_fields:
        form_class.base_fields[field].widget.attrs = {'class': 'form-control'}

    template_name = 'vacancies/vacancy_edit.html'
    context = {}
    context['title'] = "Создать вакансию | Джуманджи"

    def get(self, request):
        form = MyVacancyForm()
        form.fields['title'].initial = 'Новая вакансия'
        form.fields['specialty'].initial = 'Бэкенд'
        form.fields['description'].initial = 'Описание вакансии'
        form.fields['skills'].initial = 'Требуемые навыки'
        form.fields['salary_min'].initial = 120000
        form.fields['salary_max'].initial = 150000
        form.save(commit=False)
        self.context['form'] = form
        return render(request, template_name=self.template_name, context=self.context)

    def post(self, request):
        if request.method == 'POST':
            form = MyVacancyForm(request.POST)
            if form.is_valid():
                my_data = form.save(commit=False)
                my_data.company = request.user.companies
                my_data.save()
                return redirect('mycompany_vacancies')
            else:
                return redirect('vacancy_create')


class EditVacancyView(View):
    """Класс представления для редактирования вакансии"""
    form_class = MyVacancyForm()
    for field in form_class.base_fields:
        form_class.base_fields[field].widget.attrs = {'class': 'form-control'}

    template_name = 'vacancies/vacancy_edit.html'
    context = {}
    context['title'] = "Редактировать вакансию | Джуманджи"

    def get(self, request, pk):
        vacancy = Vacancy.objects.filter(id=pk).first()

        form = MyVacancyForm()
        form.fields['title'].initial = vacancy.title
        form.fields['specialty'].initial = vacancy.specialty
        form.fields['description'].initial = vacancy.description
        form.fields['skills'].initial = vacancy.skills
        form.fields['salary_min'].initial = vacancy.salary_min
        form.fields['salary_max'].initial = vacancy.salary_max

        form.save(commit=False)
        self.context['form'] = form
        self.context['vacancy'] = vacancy
        return render(request, template_name=self.template_name, context=self.context)

    def post(self, request, pk):
        if request.method == 'POST':
            vacancy = Vacancy.objects.filter(id=pk).first()
            form = MyVacancyForm(request.POST, instance=vacancy)

            if form.is_valid():
                form.save()
                return redirect('vacancy_edit', pk=pk)
            else:
                raise Http404


class DeleteVacancyView(View):
    def get(self, pk):
        Vacancy.objects.filter(id=pk).delete()
        return redirect('mycompany_vacancies')

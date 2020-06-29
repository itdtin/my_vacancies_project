from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from vacancies.views import AllVacanciesView, CathegoryVacancies, VacancyView, CompanyVacanciesView, \
    VacancySendView, MyCompanyView, MyCompanyCreateView, MyCompanyVacanciesView, MyCompanyOneVacancyView, \
    CreateVacancyView, EditVacancyView, DeleteVacancyView


urlpatterns = [
    path('vacancies/', AllVacanciesView.as_view(), name='vacancies'),
    path('vacancies/<int:pk>/', VacancyView.as_view(), name='vacancy'),
    path('vacancies/cat/<str:cathegory_name>/', CathegoryVacancies.as_view(), name='cathegory'),
    path('companies/<int:pk>/', CompanyVacanciesView.as_view(), name='company'),
    path('vacancies/<int:vacancy_id>/send/', VacancySendView.as_view(), name='send_vac'),

    path('mycompany/', MyCompanyView.as_view(), name='mycompany'),
    path('mycompany/new', MyCompanyCreateView.as_view(), name='mycompany_create'),
    path('mycompany/vacancies/', MyCompanyVacanciesView.as_view(), name='mycompany_vacancies'),
    path('mycompany/vacancies/<int:pk>', MyCompanyOneVacancyView.as_view(), name='mycompany_vacancy'),
    path('mycompany/vacancies/create', CreateVacancyView.as_view(), name='vacancy_create'),
    path('mycompany/vacancies/<int:pk>/edit', EditVacancyView.as_view(), name='vacancy_edit'),
    path('mycompany/vacancies/<int:pk>/delete', DeleteVacancyView.as_view(), name='vacancy_delete')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.core.management.base import BaseCommand
from vacancies.models import Company, Specialty, Vacancy
from vac_data import jobs, specialties, companies


class Command(BaseCommand):

    def handle(self, *args, **options):
        for specialty in specialties:
            sp = Specialty(code=specialty['code'], title=specialty['title'], picture='https://place-hold.it/100x60')
            sp.save()

        for company in companies:
            cm = Company(name=company['title'], logo='https://place-hold.it/100x60')
            cm.save()

        for job in jobs:
            vc = Vacancy(title=job['title'], specialty=Specialty.objects.filter(code=job['cat']).first(),
                         company=Company.objects.filter(name=job['company']).first(), salary_min=job['salary_from'],
                         salary_max=job['salary_to'], published_at=job['posted'], description=job['desc'])
            vc.save()

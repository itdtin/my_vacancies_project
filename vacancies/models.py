from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


from stepik_vacancies.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):
    """Класс модели для компании"""
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=155, blank=True)
    logo = models.ImageField(max_length=100, default="https://place-hold.it/130x80",
                             upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = models.TextField(blank=True)
    employee_count = models.IntegerField(default=1)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='companies', blank=True,
                                 null=True, default=None)

    def __str__(self):
        return self.name


@receiver(models.signals.pre_delete, sender=Company, weak=False)
def logo_delete_handler(sender, **kwargs):
    freezer = kwargs['instance']
    storage, path = freezer.logo.storage, freezer.logo.path
    storage.delete(path)


class Specialty(models.Model):
    """Класс модели для специализации"""
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=120)
    picture = models.ImageField(max_length=100, upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    """Класс модели для вакансии"""
    title = models.CharField(max_length=120)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies',
                                  verbose_name='Специализация')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.CharField(max_length=155, verbose_name='Требуемые навыки')
    description = models.TextField(verbose_name='Описание вакансии')
    salary_min = models.IntegerField(verbose_name='Зарплата от')
    salary_max = models.IntegerField(verbose_name='Зарплата до')
    published_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = models.CharField(max_length=100)
    written_phone = models.CharField(max_length=20)
    written_cover_letter = models.CharField(max_length=300)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")

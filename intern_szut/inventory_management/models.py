from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class MyUserManager(BaseUserManager):
    def create_user(self, person_id, username, first_name, last_name, password=None):
        if not person_id or not username or not first_name or not last_name:
            raise ValueError(_('Users must have a person_id, username, first_name and last_name.'))

        user = self.model(
            person_id=person_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.email = self.normalize_email(username + '@schule.bremen.de')
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, person_id, username, first_name, last_name, password=None):
        user = self.create_user(
            person_id=person_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        user.email = self.normalize_email(username + '@schule.bremen.de')
        user.allow_auto_role = False
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    person_id = models.CharField(verbose_name=_('itslearning – Person ID'), max_length=10, unique=True)
    username = models.CharField(verbose_name=_('Benutzername'), max_length=25, unique=True)
    first_name = models.CharField(verbose_name=_('Vorname'), max_length=25)
    last_name = models.CharField(verbose_name=_('Nachname'), max_length=25)
    language = models.CharField(verbose_name=_('Sprache'), max_length=10, default='de-DE')
    profile_image_url = models.CharField(verbose_name=_('Profilbild-URL'), max_length=100, null=True, blank=True)
    use_12_hour_time_format = models.BooleanField(verbose_name=_('Zwölf-Stunden Zeitformat'), default=False)
    allow_auto_role = models.BooleanField(verbose_name=_('Automatische Rollen via itslearning'), default=True)
    is_guest = models.BooleanField(verbose_name=_('Ist Gast'), default=False)
    is_staff = models.BooleanField(verbose_name=_('Ist Lehrer'), default=False)
    is_admin = models.BooleanField(verbose_name=_('Ist Admin'), default=False)
    is_superuser = models.BooleanField(verbose_name=_('Ist System-Admin'), default=False)
    is_active = models.BooleanField(verbose_name=_('Ist Aktiv'), default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['person_id', 'first_name', 'last_name']
    objects = MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Room(models.Model):
    class Meta:
        verbose_name = 'Raum'
        verbose_name_plural = 'Räume'

    name = models.CharField(max_length=10, default=None)
    BA = (
        ('1', '1. Bauabschnitt'),
        ('2', '2. Bauabschnitt'),
    )
    bauabschnitt = models.CharField(choices=BA, max_length=1)
    Geschoss = (
        ('-1', 'Kellergeschoss'),
        ('0', 'Erdgeschoss'),
        ('1', '1. Obergeschoss'),
        ('2', '2. Obergeschoss')
    )
    etage = models.CharField(choices=Geschoss, max_length=2)

    def __str__(self):
        return self.name


class DeviceClasses(models.Model):
    class Meta:
        verbose_name = 'Geräte-Klasse'
        verbose_name_plural = 'Geräte-Klassen'

    # geraete_klasse_name = models.OptionalChoiceField(choices=(
    #    ('Anzeigegerät', 'Anzeigegerät'),
    #    ('Kamera', 'Kamera'),
    #    ('Licht', 'Licht'),
    #    ('Lampe', 'Lampe'),
    #    ('Schalter', 'Schalter'),
    #    ('Wandtür', 'Wandtür'),
    #    ('Wandlampe', 'Wandlampe'),
    #    ('Wandlicht', 'Wandlicht'),
    #    ('Wandtür', 'Wandtür')))
    icon = models.ImageField(upload_to='static/images', default=None)

    # def __str__(self):
    #    return self.geraete_klasse_name


class Device(models.Model):
    class Meta:
        verbose_name = 'Gerät'
        verbose_name_plural = 'Geräte'

    geraete_name = models.CharField(max_length=30, default=None)
    geraete_status = models.CharField(max_length=10, default=None)
    geraete_kosten = models.IntegerField(default=None)
    geraete_hersteller = models.CharField(max_length=10, default=None)
    geraete_anschaffungsdatum = models.DateField()
    geraete_garantiedauer_start = models.TimeField()
    geraete_garantiedauer_ende = models.TimeField()
    geraete_seriennummer = models.CharField(max_length=50, default=None)
    geraete_garantie_information = models.CharField(max_length=50, default=None)
    geraete_information = models.CharField(max_length=100, default=None)

    # geraete_klasse = models.ForeignKey(Geraete_Klasse, on_delete=models.CASCADE)

    # raeume = models.ForeignKey(Raeume, on_delete=models.CASCADE)

    def __str__(self):
        return self.geraete_name


class Ticket(models.Model):
    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    # ticket_name = models.CharField(Raeume, on_delete=models.CASCADE)
    ticket_header = models.CharField(max_length=30, default=None)
    ticket_message = models.CharField(max_length=300, default=None)

    # ticket_typ_name = models.ForeignKey(Typ_Name, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticket_header

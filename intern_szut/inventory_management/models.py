from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

bootstrap_icon_validator = RegexValidator(regex=r'^bi bi-[a-z0-9-]+$', message=_('Bitte nutzten Sie das folgende Format: "bi bi-<icon-name>"'))


class MyUserManager(BaseUserManager):
    def create_user(self, person_id, username, first_name, last_name, password=None):
        if not person_id or not username or not first_name or not last_name:
            raise ValueError(_('Benutzer müssen eine Person-ID, einen Benutzernamen, Vornamen und Nachnamen haben.'))

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
    person_id = models.CharField(verbose_name=_('itslearning Person-ID'), max_length=10, unique=True)
    username = models.CharField(verbose_name=_('Benutzername'), max_length=25, unique=True)
    first_name = models.CharField(verbose_name=_('Vorname'), max_length=25)
    last_name = models.CharField(verbose_name=_('Nachname'), max_length=25)
    language = models.CharField(verbose_name=_('Sprache'), max_length=10, default='de-DE')
    profile_image_url = models.CharField(verbose_name=_('Profilbild-URL'), max_length=100, null=True, blank=True)
    use_12_hour_time_format = models.BooleanField(verbose_name=_('Zwölf-Stunden Zeitformat'), default=False)
    allow_auto_role = models.BooleanField(verbose_name=_('Automatische Rollen via itslearning'), default=True)
    is_guest = models.BooleanField(verbose_name=_('Ist Gast'), default=False)
    is_staff = models.BooleanField(verbose_name=_('Ist Mitarbeiter'), default=False)
    is_admin = models.BooleanField(verbose_name=_('Ist Admin'), default=False)
    is_superuser = models.BooleanField(verbose_name=_('Ist System-Admin'), default=False)
    is_active = models.BooleanField(verbose_name=_('Ist aktiv'), default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['person_id', 'first_name', 'last_name']
    objects = MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class BuildingSection(models.Model):
    class Meta:
        verbose_name = _('Bauabschnitt')
        verbose_name_plural = _('Bauabschnitte')

    name = models.CharField(verbose_name=_('Name'), max_length=35, unique=True)
    description = models.TextField(verbose_name=_('Beschreibung'), max_length=280, null=True, blank=True)

    def __str__(self):
        return self.name


class Floor(models.Model):
    class Meta:
        verbose_name = _('Etage')
        verbose_name_plural = _('Etagen')

    name = models.CharField(verbose_name=_('Name'), max_length=35, unique=True)
    description = models.TextField(verbose_name=_('Beschreibung'), max_length=280, null=True, blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    class Meta:
        verbose_name = _('Raum')
        verbose_name_plural = _('Räume')

    name = models.CharField(verbose_name=_('Name'), max_length=35, unique=True)
    building_section = models.ForeignKey(BuildingSection, verbose_name=_('Bauabschnitt'), on_delete=models.PROTECT, default=None)
    floor = models.ForeignKey(Floor, verbose_name=_('Etage'), on_delete=models.PROTECT, default=None)
    description = models.TextField(verbose_name=_('Beschreibung'), max_length=280, null=True, blank=True)

    def __str__(self):
        return self.name


class DeviceCategory(models.Model):
    class Meta:
        verbose_name = _('Gerätekategorie')
        verbose_name_plural = _('Gerätekategorien')

    name = models.CharField(verbose_name=_('Name'), max_length=35, unique=True)
    icon = models.CharField(verbose_name=_('Bootstrap-Icon (icons.getbootstrap.com)'), max_length=60, validators=[bootstrap_icon_validator], null=True, blank=True)
    description = models.TextField(verbose_name=_('Beschreibung'), max_length=280, null=True, blank=True)

    def __str__(self):
        return self.name


class DeviceManufacturer(models.Model):
    class Meta:
        verbose_name = _('Gerätehersteller')
        verbose_name_plural = _('Gerätehersteller')

    name = models.CharField(verbose_name=_('Name'), max_length=35, unique=True)
    description = models.TextField(verbose_name=_('Beschreibung'), max_length=280, null=True, blank=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    class Meta:
        verbose_name = _('Gerät')
        verbose_name_plural = _('Geräte')

    class StatusOptions(models.IntegerChoices):
        FULLY_FUNCTIONAL = 2, _('Voll funktionsfähig')
        LIMITED_FUNCTIONALITY = 1, _('Eingeschränkt funktionsfähig')
        NOT_FUNCTIONAL = 0, _('Nicht funktionsfähig')

    device_category = models.ForeignKey(DeviceCategory, verbose_name=_('Gerätekategorie'), on_delete=models.CASCADE, default=None)
    room = models.ForeignKey(Room, verbose_name=_('Raum'), on_delete=models.CASCADE, default=None)
    name = models.CharField(verbose_name=_('Name'), max_length=35)
    price = models.DecimalField(verbose_name=_('Preis'), max_digits=10, decimal_places=2, null=True, blank=True)
    device_manufacturer = models.ForeignKey(DeviceManufacturer, verbose_name=_('Gerätehersteller'), on_delete=models.CASCADE, null=True, blank=True)
    purchase_data = models.DateField(verbose_name=_('Anschaffungsdatum'), null=True, blank=True)
    serial_number = models.CharField(verbose_name=_('Seriennummer'), max_length=35, null=True, blank=True)
    warranty_period_years = models.IntegerField(verbose_name=_('Garantiezeit in Jahren'), choices=[(i, i) for i in range(1, 100)], null=True, blank=True)
    warranty_period_months = models.IntegerField(verbose_name=_('Garantiezeit in Monaten'), choices=[(i, i) for i in range(1, 12)], null=True, blank=True)
    status = models.IntegerField(verbose_name=_('Aktueller Status'), choices=StatusOptions.choices, null=True, blank=True)
    description = models.TextField(verbose_name=_('Beschreibung'), max_length=280, null=True, blank=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')

    class StatusOptions(models.IntegerChoices):
        OPEN = 2, _('Offen')
        IN_WORK = 1, _('In Bearbeitung')
        CLOSED = 0, _('Geschlossen')

    device = models.ForeignKey(Device, verbose_name=_('Gerät'), on_delete=models.CASCADE, default=None)
    title = models.CharField(verbose_name=_('Titel'), max_length=35)
    description = models.TextField(verbose_name=_('Beschreibung'), max_length=280, null=True, blank=True)
    status = models.IntegerField(verbose_name=_('Aktueller Status'), choices=StatusOptions.choices)
    created_at = models.DateTimeField(verbose_name=_('Erstellt am'), auto_now=True)
    created_by = models.ForeignKey(MyUser, verbose_name=_('Erstellt von'), on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class TicketComment(models.Model):
    class Meta:
        verbose_name = _('Ticket-Antwort')
        verbose_name_plural = _('Ticket-Antworten')

    ticket = models.ForeignKey(Ticket, verbose_name=_('Ticket'), on_delete=models.CASCADE, default=None)
    comment = models.TextField(verbose_name=_('Antwort'), max_length=280)
    created_at = models.DateTimeField(verbose_name=_('Erstellt am'), auto_now=True)
    created_by = models.ForeignKey(MyUser, verbose_name=_('Erstellt von'), on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

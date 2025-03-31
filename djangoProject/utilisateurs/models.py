from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UtilisateurManager(BaseUserManager):
    def create_user(self, nom_utilisateur, email, mot_de_passe=None):
        if not email:
            raise ValueError('Les utilisateurs doivent avoir une adresse email')
        if not nom_utilisateur:
            raise ValueError('Les utilisateurs doivent avoir un nom d\'utilisateur')

        user = self.model(
            email=self.normalize_email(email),
            nom_utilisateur=nom_utilisateur,
        )
        user.set_password(mot_de_passe)
        user.save(using=self._db)
        return user

    def create_superuser(self, nom_utilisateur, email, mot_de_passe):
        user = self.create_user(
            nom_utilisateur=nom_utilisateur,
            email=self.normalize_email(email),
            mot_de_passe=mot_de_passe,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Utilisateur(AbstractBaseUser, PermissionsMixin):
    nom_utilisateur = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # Override groups and user_permissions with custom related_names
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='utilisateur_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='utilisateur_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    objects = UtilisateurManager()

    USERNAME_FIELD = 'nom_utilisateur'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.nom_utilisateur

    class Meta:
        db_table = 'utilisateurs'
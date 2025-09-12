from productos.models import Profile
from django.contrib.auth.models import User

# Eliminar perfiles duplicados (dejar solo uno por usuario)
users_with_profiles = {}
for profile in Profile.objects.all():
    if profile.user_id in users_with_profiles:
        print(f"Eliminando perfil duplicado para usuario ID {profile.user_id}")
        profile.delete()
    else:
        users_with_profiles[profile.user_id] = profile.id

# Crear perfiles faltantes para usuarios sin perfil
for user in User.objects.all():
    if not hasattr(user, 'profile'):
        print(f"Creando perfil para usuario: {user.username}")
        Profile.objects.create(user=user)
print("Limpieza completada.")

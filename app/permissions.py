from flask_principal import Principal, RoleNeed, Permission
from flask_login import current_user

# Roller
admin_role = RoleNeed('admin')
musteri_role = RoleNeed('musteri')
muteahhit_role = RoleNeed('muteahhit')
emlak_role = RoleNeed('emlak')

# İzinler
admin_permission = Permission(admin_role)
musteri_permission = Permission(musteri_role)
muteahhit_permission = Permission(muteahhit_role)
emlak_permission = Permission(emlak_role)


from flask_principal import Principal, RoleNeed, Permission
from flask_login import current_user

# Roller
admin_role = RoleNeed('admin')
sef_role = RoleNeed('sef')
raportor_role = RoleNeed('raportor')
koordinator_role = RoleNeed('koordinator')

# İzinler
admin_permission = Permission(admin_role)
sef_permission = Permission(sef_role)
raportor_permission = Permission(raportor_role)
koordinator_permission = Permission(koordinator_role)
# İzinler
riskli_islem_permission = Permission(admin_role, sef_role, raportor_role)


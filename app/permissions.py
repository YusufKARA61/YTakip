from flask_principal import Principal, RoleNeed, Permission
from flask_login import current_user

# Roller
admin_role = RoleNeed('admin')
riskli_sef_role = RoleNeed('Riskli Yapı Şefi')
etüt_sef_role = RoleNeed('Etüt ve Proje Şefi')
bolge_sef_role = RoleNeed('Yapı Kontrol Şefi')
kesin_hesap_sef_role = RoleNeed('Kesin Hesap Şefi')
kontrol_role = RoleNeed('Kontrol Mühendisi')
raportor_role = RoleNeed('raportor')
bolge_role = RoleNeed('Bölge Mühendisi')
koordinator_role = RoleNeed('koordinator')

# İzinler
admin_permission = Permission(admin_role)
riskli_sef_permission = Permission(riskli_sef_role)
etüt_sef_permission = Permission(etüt_sef_role)
bolge_sef_permission = Permission(bolge_sef_role)
kesin_hesap_sef_permission = Permission(kesin_hesap_sef_role)
bolge_muh_permission = Permission(bolge_role)
raportor_permission = Permission(raportor_role)
koordinator_permission = Permission(koordinator_role)
riskli_islem_permission = Permission(admin_role, riskli_sef_role, raportor_role)
etut_islem_permission = Permission(admin_role, etüt_sef_role, koordinator_role)
bolge_islem_permission = Permission(admin_role, bolge_sef_role, raportor_role, bolge_role)
kesin_hesap_permission = Permission(admin_role, kesin_hesap_sef_role, kontrol_role)


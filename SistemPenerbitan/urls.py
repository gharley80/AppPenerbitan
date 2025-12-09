from django.contrib import admin
from django.urls import path
# Hapus import LogoutView yang lama, ganti dengan logout_view dari views kita
from core_production.views import (
    CustomLoginView, 
    dashboard_admin, 
    dashboard_prepress, 
    dashboard_produksi,
    update_prepress,
    logout_view  # <--- IMPORT FUNGSI BARU INI
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CustomLoginView.as_view(), name='login'),
    
    # GANTI BARIS LOGOUT MENJADI INI:
    path('logout/', logout_view, name='logout'),

    path('dashboard/admin/', dashboard_admin, name='dash_admin'),
    path('dashboard/produksi/', dashboard_produksi, name='dash_produksi'),
    path('dashboard/pre-press/', dashboard_prepress, name='dash_prepress'),
    path('dashboard/pre-press/update/<int:workflow_id>/', update_prepress, name='update_prepress'),
]
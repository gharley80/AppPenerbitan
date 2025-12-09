from django.contrib import admin
from .models import Order, BookSpecification, ProductionWorkflow

# --- Konfigurasi Inline (Formulir Tempelan) ---
class BookSpecInline(admin.StackedInline):
    model = BookSpecification
    can_delete = False
    verbose_name_plural = 'Spesifikasi Buku (Edit setelah Order dibuat)'
    fk_name = 'order'

class WorkflowInline(admin.StackedInline):
    model = ProductionWorkflow
    can_delete = False
    verbose_name_plural = 'Tracking Produksi (Edit setelah Order dibuat)'
    fk_name = 'order'

# --- Konfigurasi Utama Order ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'nomor_order', 
        'judul_buku', 
        'nama_pemesan', 
        'status_global', 
        'deadline_color_code', 
        'total_harga'
    )
    
    list_filter = ('status_global', 'deadline')
    search_fields = ('nomor_order', 'judul_buku', 'nama_pemesan')
    
    # Fieldset: Mengatur tampilan form Order utama
    fieldsets = (
        ('Informasi Utama', {
            'fields': ('nomor_order', 'judul_buku', 'status_global')
        }),
        ('Data Klien', {
            'fields': ('nama_pemesan', 'deadline', 'total_harga')
        }),
    )

    # --- LOGIKA KUNCI: CONDITIONAL INLINES ---
    def get_inlines(self, request, obj=None):
        """
        Logika: 
        - Jika obj ada (artinya sedang Edit Order) -> Tampilkan Inline Spesifikasi & Workflow.
        - Jika obj None (artinya sedang Buat Baru) -> Sembunyikan Inline (Biar Signal yang kerja).
        """
        if obj:
            return [BookSpecInline, WorkflowInline]
        return []

    # Fitur visual deadline (seperti sebelumnya)
    def deadline_color_code(self, obj):
        from django.utils import timezone
        today = timezone.now().date()
        if obj.deadline < today and obj.status_global != 'SIAP':
            return f"⚠️ TERLAMBAT"
        return obj.deadline
    
    deadline_color_code.short_description = 'Deadline'
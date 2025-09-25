# Generated manually due to database configuration issues

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='category',
            field=models.CharField(choices=[
                ('declaracao_simples', 'Declaração Simples'),
                ('declaracao_laboral', 'Declaração Laboral/Financeira'),
                ('declaracao_complexa', 'Declaração Complexa'),
                ('contrato_simples', 'Contrato Simples'),
                ('contrato_servicos', 'Contrato de Prestação de Serviços'),
                ('contrato_complexo', 'Contrato Complexo'),
                ('fatura_simples', 'Fatura Simples'),
                ('fatura_comercial', 'Fatura Comercial'),
                ('documento_auxiliar', 'Documento Auxiliar'),
                ('cv_basico', 'CV Básico'),
                ('cv_profissional', 'CV Profissional'),
                ('cv_multilingue', 'CV Multilíngue'),
                ('contract', 'Contrato'),
                ('invoice', 'Factura'),
                ('report', 'Relatório'),
                ('certificate', 'Certificado'),
            ], max_length=50),
        ),
        migrations.AddField(
            model_name='template',
            name='subcategory',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='template',
            name='price_kz',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
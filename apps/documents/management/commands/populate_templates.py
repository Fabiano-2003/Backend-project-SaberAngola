"""
Management command to populate document templates in the database.
"""

from django.core.management.base import BaseCommand
from documents.models import Template


class Command(BaseCommand):
    help = 'Populate database with document templates'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Criando templates de documentos...'))
        
        # Criar templates de Declarações Simples (200 KZ)
        self.create_declaration_templates()
        
        # Criar templates de Declarações Laborais/Financeiras (300 KZ)
        self.create_labor_declaration_templates()
        
        # Criar templates de Declarações Complexas (400 KZ)
        self.create_complex_declaration_templates()
        
        # Criar templates de Contratos
        self.create_contract_templates()
        
        self.stdout.write(self.style.SUCCESS('Templates criados com sucesso!'))

    def create_declaration_templates(self):
        """Criar templates de declarações simples"""
        
        # Declaração de Residência
        Template.objects.get_or_create(
            name='Declaração de Residência',
            category='declaracao_simples',
            defaults={
                'description': 'Declaração simples de residência para comprovar domicílio',
                'subcategory': 'residencia',
                'price_kz': 200.00,
                'fields': {
                    'nome_completo': {
                        'label': 'Nome Completo',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Digite o nome completo'
                    },
                    'numero_bi': {
                        'label': 'Número do Bilhete de Identidade',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Ex: 123456789LA123'
                    },
                    'endereco_completo': {
                        'label': 'Endereço Completo',
                        'type': 'textarea',
                        'required': True,
                        'placeholder': 'Rua, número, bairro, município, província'
                    },
                    'tempo_residencia': {
                        'label': 'Tempo de Residência',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Ex: 5 anos'
                    },
                    'finalidade': {
                        'label': 'Finalidade da Declaração',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Para que será usada a declaração'
                    },
                    'data_declaracao': {
                        'label': 'Data da Declaração',
                        'type': 'date',
                        'required': True
                    }
                }
            }
        )

        # Declaração de União de Facto
        Template.objects.get_or_create(
            name='Declaração de União de Facto',
            category='declaracao_simples',
            defaults={
                'description': 'Declaração para comprovar união de facto entre duas pessoas',
                'subcategory': 'uniao_facto',
                'price_kz': 200.00,
                'fields': {
                    'nome_declarante': {
                        'label': 'Nome do Declarante',
                        'type': 'text',
                        'required': True
                    },
                    'bi_declarante': {
                        'label': 'BI do Declarante',
                        'type': 'text',
                        'required': True
                    },
                    'nome_companheiro': {
                        'label': 'Nome do Companheiro(a)',
                        'type': 'text',
                        'required': True
                    },
                    'bi_companheiro': {
                        'label': 'BI do Companheiro(a)',
                        'type': 'text',
                        'required': True
                    },
                    'data_inicio_uniao': {
                        'label': 'Data de Início da União',
                        'type': 'date',
                        'required': True
                    },
                    'endereco_residencia': {
                        'label': 'Endereço de Residência Comum',
                        'type': 'textarea',
                        'required': True
                    },
                    'finalidade': {
                        'label': 'Finalidade',
                        'type': 'text',
                        'required': True
                    }
                }
            }
        )

        # Declaração de Estado Civil
        Template.objects.get_or_create(
            name='Declaração de Estado Civil',
            category='declaracao_simples',
            defaults={
                'description': 'Declaração para comprovar estado civil',
                'subcategory': 'estado_civil',
                'price_kz': 200.00,
                'fields': {
                    'nome_completo': {
                        'label': 'Nome Completo',
                        'type': 'text',
                        'required': True
                    },
                    'numero_bi': {
                        'label': 'Número do BI',
                        'type': 'text',
                        'required': True
                    },
                    'data_nascimento': {
                        'label': 'Data de Nascimento',
                        'type': 'date',
                        'required': True
                    },
                    'estado_civil': {
                        'label': 'Estado Civil',
                        'type': 'select',
                        'required': True,
                        'options': ['Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)', 'União de Facto']
                    },
                    'finalidade': {
                        'label': 'Finalidade',
                        'type': 'text',
                        'required': True
                    }
                }
            }
        )

        # Declaração de Matrícula Básica
        Template.objects.get_or_create(
            name='Declaração de Matrícula Básica',
            category='declaracao_simples',
            defaults={
                'description': 'Declaração simples para confirmar matrícula em instituição',
                'subcategory': 'matricula_basica',
                'price_kz': 200.00,
                'fields': {
                    'nome_estudante': {
                        'label': 'Nome do Estudante',
                        'type': 'text',
                        'required': True
                    },
                    'numero_bi': {
                        'label': 'Número do BI',
                        'type': 'text',
                        'required': True
                    },
                    'nome_instituicao': {
                        'label': 'Nome da Instituição',
                        'type': 'text',
                        'required': True
                    },
                    'curso_classe': {
                        'label': 'Curso/Classe',
                        'type': 'text',
                        'required': True
                    },
                    'ano_letivo': {
                        'label': 'Ano Letivo',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Ex: 2024/2025'
                    },
                    'finalidade': {
                        'label': 'Finalidade',
                        'type': 'text',
                        'required': True
                    }
                }
            }
        )

        # Declaração de Frequência Simples
        Template.objects.get_or_create(
            name='Declaração de Frequência Simples',
            category='declaracao_simples',
            defaults={
                'description': 'Declaração para comprovar frequência escolar/acadêmica',
                'subcategory': 'frequencia_simples',
                'price_kz': 200.00,
                'fields': {
                    'nome_estudante': {
                        'label': 'Nome do Estudante',
                        'type': 'text',
                        'required': True
                    },
                    'numero_bi': {
                        'label': 'Número do BI',
                        'type': 'text',
                        'required': True
                    },
                    'nome_instituicao': {
                        'label': 'Nome da Instituição',
                        'type': 'text',
                        'required': True
                    },
                    'curso_classe': {
                        'label': 'Curso/Classe',
                        'type': 'text',
                        'required': True
                    },
                    'periodo': {
                        'label': 'Período de Frequência',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Ex: Janeiro a Dezembro 2024'
                    },
                    'situacao': {
                        'label': 'Situação',
                        'type': 'select',
                        'required': True,
                        'options': ['Frequentando', 'Concluído', 'Interrompido']
                    }
                }
            }
        )

        self.stdout.write('✓ Templates de Declarações Simples criados')

    def create_labor_declaration_templates(self):
        """Criar templates de declarações laborais/financeiras"""
        
        # Declaração de Vínculo Empregatício
        Template.objects.get_or_create(
            name='Declaração de Vínculo Empregatício',
            category='declaracao_laboral',
            defaults={
                'description': 'Declaração para comprovar vínculo empregatício',
                'subcategory': 'vinculo_empregaticio',
                'price_kz': 300.00,
                'fields': {
                    'nome_funcionario': {
                        'label': 'Nome do Funcionário',
                        'type': 'text',
                        'required': True
                    },
                    'numero_bi': {
                        'label': 'Número do BI',
                        'type': 'text',
                        'required': True
                    },
                    'nome_empresa': {
                        'label': 'Nome da Empresa',
                        'type': 'text',
                        'required': True
                    },
                    'nif_empresa': {
                        'label': 'NIF da Empresa',
                        'type': 'text',
                        'required': True
                    },
                    'cargo': {
                        'label': 'Cargo/Função',
                        'type': 'text',
                        'required': True
                    },
                    'data_admissao': {
                        'label': 'Data de Admissão',
                        'type': 'date',
                        'required': True
                    },
                    'tipo_contrato': {
                        'label': 'Tipo de Contrato',
                        'type': 'select',
                        'required': True,
                        'options': ['Efetivo', 'Termo Certo', 'Estágio', 'Prestação de Serviços']
                    },
                    'salario': {
                        'label': 'Salário Mensal (Kz)',
                        'type': 'number',
                        'required': True
                    },
                    'finalidade': {
                        'label': 'Finalidade',
                        'type': 'text',
                        'required': True
                    }
                }
            }
        )

        # Declaração de Salário
        Template.objects.get_or_create(
            name='Declaração de Salário',
            category='declaracao_laboral',
            defaults={
                'description': 'Declaração detalhada de salário e vencimentos',
                'subcategory': 'salario',
                'price_kz': 300.00,
                'fields': {
                    'nome_funcionario': {
                        'label': 'Nome do Funcionário',
                        'type': 'text',
                        'required': True
                    },
                    'numero_bi': {
                        'label': 'Número do BI',
                        'type': 'text',
                        'required': True
                    },
                    'nome_empresa': {
                        'label': 'Nome da Empresa',
                        'type': 'text',
                        'required': True
                    },
                    'cargo': {
                        'label': 'Cargo',
                        'type': 'text',
                        'required': True
                    },
                    'salario_base': {
                        'label': 'Salário Base (Kz)',
                        'type': 'number',
                        'required': True
                    },
                    'subsidios': {
                        'label': 'Subsídios (Kz)',
                        'type': 'number',
                        'required': False,
                        'placeholder': '0'
                    },
                    'salario_liquido': {
                        'label': 'Salário Líquido (Kz)',
                        'type': 'number',
                        'required': True
                    },
                    'periodo_referencia': {
                        'label': 'Período de Referência',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Ex: Janeiro a Dezembro 2024'
                    },
                    'finalidade': {
                        'label': 'Finalidade',
                        'type': 'text',
                        'required': True
                    }
                }
            }
        )

        # Declaração de Rendimentos
        Template.objects.get_or_create(
            name='Declaração de Rendimentos',
            category='declaracao_laboral',
            defaults={
                'description': 'Declaração completa de rendimentos anuais',
                'subcategory': 'rendimentos',
                'price_kz': 300.00,
                'fields': {
                    'nome_contribuinte': {
                        'label': 'Nome do Contribuinte',
                        'type': 'text',
                        'required': True
                    },
                    'numero_bi': {
                        'label': 'Número do BI',
                        'type': 'text',
                        'required': True
                    },
                    'nif': {
                        'label': 'NIF',
                        'type': 'text',
                        'required': True
                    },
                    'ano_fiscal': {
                        'label': 'Ano Fiscal',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Ex: 2024'
                    },
                    'rendimento_trabalho': {
                        'label': 'Rendimento do Trabalho (Kz)',
                        'type': 'number',
                        'required': True
                    },
                    'rendimento_outros': {
                        'label': 'Outros Rendimentos (Kz)',
                        'type': 'number',
                        'required': False,
                        'placeholder': '0'
                    },
                    'total_rendimentos': {
                        'label': 'Total de Rendimentos (Kz)',
                        'type': 'number',
                        'required': True
                    },
                    'impostos_retidos': {
                        'label': 'Impostos Retidos (Kz)',
                        'type': 'number',
                        'required': False,
                        'placeholder': '0'
                    }
                }
            }
        )

        # Declaração de Situação Fiscal
        Template.objects.get_or_create(
            name='Declaração de Situação Fiscal',
            category='declaracao_laboral',
            defaults={
                'description': 'Declaração para comprovar situação fiscal do contribuinte',
                'subcategory': 'situacao_fiscal',
                'price_kz': 300.00,
                'fields': {
                    'nome_contribuinte': {
                        'label': 'Nome do Contribuinte',
                        'type': 'text',
                        'required': True
                    },
                    'numero_bi': {
                        'label': 'Número do BI',
                        'type': 'text',
                        'required': True
                    },
                    'nif': {
                        'label': 'NIF',
                        'type': 'text',
                        'required': True
                    },
                    'situacao_fiscal': {
                        'label': 'Situação Fiscal',
                        'type': 'select',
                        'required': True,
                        'options': ['Em dia', 'Com débitos', 'Isento', 'Regularizado']
                    },
                    'ano_referencia': {
                        'label': 'Ano de Referência',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Ex: 2024'
                    },
                    'debitos_pendentes': {
                        'label': 'Débitos Pendentes (Kz)',
                        'type': 'number',
                        'required': False,
                        'placeholder': '0 se não houver débitos'
                    },
                    'ultima_declaracao': {
                        'label': 'Data da Última Declaração',
                        'type': 'date',
                        'required': False
                    },
                    'finalidade': {
                        'label': 'Finalidade',
                        'type': 'text',
                        'required': True
                    }
                }
            }
        )

        # Declaração de Experiência Profissional
        Template.objects.get_or_create(
            name='Declaração de Experiência Profissional',
            category='declaracao_laboral',
            defaults={
                'description': 'Declaração detalhada de experiência profissional',
                'subcategory': 'experiencia_profissional',
                'price_kz': 300.00,
                'fields': {
                    'nome_funcionario': {
                        'label': 'Nome do Funcionário',
                        'type': 'text',
                        'required': True
                    },
                    'numero_bi': {
                        'label': 'Número do BI',
                        'type': 'text',
                        'required': True
                    },
                    'nome_empresa': {
                        'label': 'Nome da Empresa',
                        'type': 'text',
                        'required': True
                    },
                    'nif_empresa': {
                        'label': 'NIF da Empresa',
                        'type': 'text',
                        'required': True
                    },
                    'cargo_atual': {
                        'label': 'Cargo Atual',
                        'type': 'text',
                        'required': True
                    },
                    'data_admissao': {
                        'label': 'Data de Admissão',
                        'type': 'date',
                        'required': True
                    },
                    'responsabilidades': {
                        'label': 'Principais Responsabilidades',
                        'type': 'textarea',
                        'required': True,
                        'placeholder': 'Descreva as principais atividades e responsabilidades'
                    },
                    'experiencia_anterior': {
                        'label': 'Experiência Anterior',
                        'type': 'textarea',
                        'required': False,
                        'placeholder': 'Outras experiências relevantes'
                    },
                    'qualificacoes': {
                        'label': 'Qualificações e Certificações',
                        'type': 'textarea',
                        'required': False,
                        'placeholder': 'Cursos, certificações, formações relevantes'
                    },
                    'tempo_experiencia': {
                        'label': 'Tempo Total de Experiência',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Ex: 5 anos'
                    },
                    'finalidade': {
                        'label': 'Finalidade',
                        'type': 'text',
                        'required': True
                    }
                }
            }
        )

        self.stdout.write('✓ Templates de Declarações Laborais/Financeiras criados')

    def create_complex_declaration_templates(self):
        """Criar templates de declarações complexas"""
        
        # Declaração de Bens Patrimoniais
        Template.objects.get_or_create(
            name='Declaração de Bens Patrimoniais',
            category='declaracao_complexa',
            defaults={
                'description': 'Declaração detalhada de patrimônio e bens',
                'subcategory': 'bens_patrimoniais',
                'price_kz': 400.00,
                'fields': {
                    'nome_declarante': {
                        'label': 'Nome do Declarante',
                        'type': 'text',
                        'required': True
                    },
                    'numero_bi': {
                        'label': 'Número do BI',
                        'type': 'text',
                        'required': True
                    },
                    'nif': {
                        'label': 'NIF',
                        'type': 'text',
                        'required': True
                    },
                    'imoveis': {
                        'label': 'Imóveis (descrição detalhada)',
                        'type': 'textarea',
                        'required': False,
                        'placeholder': 'Descreva todos os imóveis com localização e valor estimado'
                    },
                    'veiculos': {
                        'label': 'Veículos (descrição detalhada)',
                        'type': 'textarea',
                        'required': False,
                        'placeholder': 'Descreva todos os veículos com marca, modelo, ano e valor'
                    },
                    'contas_bancarias': {
                        'label': 'Contas Bancárias',
                        'type': 'textarea',
                        'required': False,
                        'placeholder': 'Liste bancos e saldos aproximados'
                    },
                    'outros_bens': {
                        'label': 'Outros Bens',
                        'type': 'textarea',
                        'required': False,
                        'placeholder': 'Outros bens de valor significativo'
                    },
                    'valor_total_estimado': {
                        'label': 'Valor Total Estimado (Kz)',
                        'type': 'number',
                        'required': True
                    },
                    'data_referencia': {
                        'label': 'Data de Referência',
                        'type': 'date',
                        'required': True
                    },
                    'finalidade': {
                        'label': 'Finalidade',
                        'type': 'text',
                        'required': True
                    }
                }
            }
        )

        # Declaração de Transferência Escolar
        Template.objects.get_or_create(
            name='Declaração de Transferência Escolar',
            category='declaracao_complexa',
            defaults={
                'description': 'Declaração completa para transferência entre instituições de ensino',
                'subcategory': 'transferencia_escolar',
                'price_kz': 400.00,
                'fields': {
                    'nome_estudante': {
                        'label': 'Nome do Estudante',
                        'type': 'text',
                        'required': True
                    },
                    'numero_bi': {
                        'label': 'Número do BI',
                        'type': 'text',
                        'required': True
                    },
                    'instituicao_origem': {
                        'label': 'Instituição de Origem',
                        'type': 'text',
                        'required': True
                    },
                    'curso_classe_origem': {
                        'label': 'Curso/Classe de Origem',
                        'type': 'text',
                        'required': True
                    },
                    'periodo_frequencia': {
                        'label': 'Período de Frequência',
                        'type': 'text',
                        'required': True
                    },
                    'notas_disciplinas': {
                        'label': 'Notas por Disciplina',
                        'type': 'textarea',
                        'required': True,
                        'placeholder': 'Liste todas as disciplinas e respectivas notas'
                    },
                    'instituicao_destino': {
                        'label': 'Instituição de Destino',
                        'type': 'text',
                        'required': True
                    },
                    'motivo_transferencia': {
                        'label': 'Motivo da Transferência',
                        'type': 'textarea',
                        'required': True
                    },
                    'situacao_academica': {
                        'label': 'Situação Acadêmica',
                        'type': 'select',
                        'required': True,
                        'options': ['Aprovado', 'Reprovado', 'Em curso', 'Trancado']
                    }
                }
            }
        )

        # Declaração de Conclusão de Curso
        Template.objects.get_or_create(
            name='Declaração de Conclusão de Curso',
            category='declaracao_complexa',
            defaults={
                'description': 'Declaração oficial de conclusão de curso acadêmico',
                'subcategory': 'conclusao_curso',
                'price_kz': 400.00,
                'fields': {
                    'nome_estudante': {
                        'label': 'Nome do Estudante',
                        'type': 'text',
                        'required': True
                    },
                    'numero_bi': {
                        'label': 'Número do BI',
                        'type': 'text',
                        'required': True
                    },
                    'nome_instituicao': {
                        'label': 'Nome da Instituição',
                        'type': 'text',
                        'required': True
                    },
                    'codigo_instituicao': {
                        'label': 'Código da Instituição',
                        'type': 'text',
                        'required': True
                    },
                    'nome_curso': {
                        'label': 'Nome do Curso',
                        'type': 'text',
                        'required': True
                    },
                    'grau_academico': {
                        'label': 'Grau Acadêmico',
                        'type': 'select',
                        'required': True,
                        'options': ['Licenciatura', 'Mestrado', 'Doutoramento', 'Técnico Médio', 'Ensino Médio']
                    },
                    'data_inicio': {
                        'label': 'Data de Início do Curso',
                        'type': 'date',
                        'required': True
                    },
                    'data_conclusao': {
                        'label': 'Data de Conclusão',
                        'type': 'date',
                        'required': True
                    },
                    'nota_final': {
                        'label': 'Nota Final/Classificação',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Ex: 16 valores, Bom, etc.'
                    },
                    'numero_diploma': {
                        'label': 'Número do Diploma',
                        'type': 'text',
                        'required': False,
                        'placeholder': 'Se já emitido'
                    },
                    'disciplinas_principais': {
                        'label': 'Principais Disciplinas',
                        'type': 'textarea',
                        'required': True,
                        'placeholder': 'Liste as principais disciplinas cursadas'
                    },
                    'carga_horaria_total': {
                        'label': 'Carga Horária Total',
                        'type': 'number',
                        'required': True,
                        'placeholder': 'Horas'
                    },
                    'finalidade': {
                        'label': 'Finalidade',
                        'type': 'text',
                        'required': True
                    }
                }
            }
        )

        # Declaração de Situação Fiscal Detalhada
        Template.objects.get_or_create(
            name='Declaração de Situação Fiscal Detalhada',
            category='declaracao_complexa',
            defaults={
                'description': 'Declaração completa e detalhada da situação fiscal',
                'subcategory': 'situacao_fiscal_detalhada',
                'price_kz': 400.00,
                'fields': {
                    'nome_contribuinte': {
                        'label': 'Nome do Contribuinte',
                        'type': 'text',
                        'required': True
                    },
                    'numero_bi': {
                        'label': 'Número do BI',
                        'type': 'text',
                        'required': True
                    },
                    'nif': {
                        'label': 'NIF',
                        'type': 'text',
                        'required': True
                    },
                    'tipo_contribuinte': {
                        'label': 'Tipo de Contribuinte',
                        'type': 'select',
                        'required': True,
                        'options': ['Pessoa Singular', 'Pessoa Coletiva', 'Empresário em Nome Individual']
                    },
                    'actividade_principal': {
                        'label': 'Atividade Principal',
                        'type': 'text',
                        'required': True
                    },
                    'codigo_actividade': {
                        'label': 'Código da Atividade (CAE)',
                        'type': 'text',
                        'required': True
                    },
                    'situacao_actual': {
                        'label': 'Situação Atual',
                        'type': 'select',
                        'required': True,
                        'options': ['Ativo', 'Inativo', 'Suspenso', 'Cancelado']
                    },
                    'historico_declaracoes': {
                        'label': 'Histórico de Declarações',
                        'type': 'textarea',
                        'required': True,
                        'placeholder': 'Últimas declarações submetidas com datas'
                    },
                    'impostos_pagos': {
                        'label': 'Impostos Pagos nos Últimos 3 Anos (Kz)',
                        'type': 'number',
                        'required': True
                    },
                    'debitos_existentes': {
                        'label': 'Débitos Existentes (Kz)',
                        'type': 'number',
                        'required': False,
                        'placeholder': '0 se não houver'
                    },
                    'plano_pagamento': {
                        'label': 'Plano de Pagamento Ativo',
                        'type': 'select',
                        'required': True,
                        'options': ['Sim', 'Não', 'N/A']
                    },
                    'certidoes_emitidas': {
                        'label': 'Certidões Emitidas Recentemente',
                        'type': 'textarea',
                        'required': False,
                        'placeholder': 'Liste certidões emitidas nos últimos 12 meses'
                    },
                    'periodo_referencia': {
                        'label': 'Período de Referência',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Ex: 2022-2024'
                    }
                }
            }
        )

        # Declaração de Reconhecimento de Firma
        Template.objects.get_or_create(
            name='Declaração de Reconhecimento de Firma',
            category='declaracao_complexa',
            defaults={
                'description': 'Declaração para reconhecimento de firma e assinatura',
                'subcategory': 'reconhecimento_firma',
                'price_kz': 400.00,
                'fields': {
                    'nome_requerente': {
                        'label': 'Nome do Requerente',
                        'type': 'text',
                        'required': True
                    },
                    'numero_bi': {
                        'label': 'Número do BI',
                        'type': 'text',
                        'required': True
                    },
                    'documento_reconhecer': {
                        'label': 'Documento a Reconhecer',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Tipo de documento que precisa de reconhecimento'
                    },
                    'finalidade_documento': {
                        'label': 'Finalidade do Documento',
                        'type': 'textarea',
                        'required': True,
                        'placeholder': 'Para que será usado o documento com firma reconhecida'
                    },
                    'tipo_reconhecimento': {
                        'label': 'Tipo de Reconhecimento',
                        'type': 'select',
                        'required': True,
                        'options': ['Por semelhança', 'Por comparação', 'Presencial']
                    },
                    'testemunhas': {
                        'label': 'Dados das Testemunhas',
                        'type': 'textarea',
                        'required': False,
                        'placeholder': 'Nome, BI e contato das testemunhas (se necessário)'
                    },
                    'local_reconhecimento': {
                        'label': 'Local do Reconhecimento',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Cartório, Conservatória, etc.'
                    },
                    'documento_identidade': {
                        'label': 'Documento de Identidade Apresentado',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'BI, Passaporte, etc.'
                    },
                    'observacoes': {
                        'label': 'Observações Especiais',
                        'type': 'textarea',
                        'required': False,
                        'placeholder': 'Qualquer observação relevante'
                    },
                    'urgencia': {
                        'label': 'Urgência',
                        'type': 'select',
                        'required': True,
                        'options': ['Normal', 'Urgente', 'Muito Urgente']
                    }
                }
            }
        )

        self.stdout.write('✓ Templates de Declarações Complexas criados')

    def create_contract_templates(self):
        """Criar templates de contratos"""
        
        # Contratos Simples (500 KZ)
        
        # Contrato de Compra e Venda de Bem Móvel
        Template.objects.get_or_create(
            name='Contrato de Compra e Venda de Bem Móvel',
            category='contrato_simples',
            defaults={
                'description': 'Contrato simples para compra e venda de bens móveis',
                'subcategory': 'compra_venda_movel',
                'price_kz': 500.00,
                'fields': {
                    'vendedor_nome': {
                        'label': 'Nome do Vendedor',
                        'type': 'text',
                        'required': True
                    },
                    'vendedor_bi': {
                        'label': 'BI do Vendedor',
                        'type': 'text',
                        'required': True
                    },
                    'vendedor_endereco': {
                        'label': 'Endereço do Vendedor',
                        'type': 'textarea',
                        'required': True
                    },
                    'comprador_nome': {
                        'label': 'Nome do Comprador',
                        'type': 'text',
                        'required': True
                    },
                    'comprador_bi': {
                        'label': 'BI do Comprador',
                        'type': 'text',
                        'required': True
                    },
                    'comprador_endereco': {
                        'label': 'Endereço do Comprador',
                        'type': 'textarea',
                        'required': True
                    },
                    'bem_descricao': {
                        'label': 'Descrição do Bem',
                        'type': 'textarea',
                        'required': True,
                        'placeholder': 'Descreva detalhadamente o bem a ser vendido'
                    },
                    'valor_venda': {
                        'label': 'Valor da Venda (Kz)',
                        'type': 'number',
                        'required': True
                    },
                    'forma_pagamento': {
                        'label': 'Forma de Pagamento',
                        'type': 'select',
                        'required': True,
                        'options': ['À vista', 'Parcelado', 'Transferência bancária', 'Cheque']
                    },
                    'local_entrega': {
                        'label': 'Local de Entrega',
                        'type': 'text',
                        'required': True
                    },
                    'data_entrega': {
                        'label': 'Data de Entrega',
                        'type': 'date',
                        'required': True
                    }
                }
            }
        )

        # Contrato de Prestação de Serviço Simples
        Template.objects.get_or_create(
            name='Contrato de Prestação de Serviço Simples',
            category='contrato_simples',
            defaults={
                'description': 'Contrato básico para prestação de serviços',
                'subcategory': 'servico_simples',
                'price_kz': 500.00,
                'fields': {
                    'prestador_nome': {
                        'label': 'Nome do Prestador',
                        'type': 'text',
                        'required': True
                    },
                    'prestador_bi': {
                        'label': 'BI do Prestador',
                        'type': 'text',
                        'required': True
                    },
                    'contratante_nome': {
                        'label': 'Nome do Contratante',
                        'type': 'text',
                        'required': True
                    },
                    'contratante_bi': {
                        'label': 'BI do Contratante',
                        'type': 'text',
                        'required': True
                    },
                    'servico_descricao': {
                        'label': 'Descrição do Serviço',
                        'type': 'textarea',
                        'required': True,
                        'placeholder': 'Descreva detalhadamente o serviço a ser prestado'
                    },
                    'valor_servico': {
                        'label': 'Valor do Serviço (Kz)',
                        'type': 'number',
                        'required': True
                    },
                    'prazo_execucao': {
                        'label': 'Prazo de Execução',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Ex: 30 dias'
                    },
                    'local_execucao': {
                        'label': 'Local de Execução',
                        'type': 'text',
                        'required': True
                    },
                    'forma_pagamento': {
                        'label': 'Forma de Pagamento',
                        'type': 'select',
                        'required': True,
                        'options': ['À vista', 'Parcelado', '50% antecipado + 50% final', 'Após conclusão']
                    }
                }
            }
        )

        # Contrato de Aluguel Residencial Básico
        Template.objects.get_or_create(
            name='Contrato de Aluguel Residencial Básico',
            category='contrato_simples',
            defaults={
                'description': 'Contrato básico de aluguel residencial',
                'subcategory': 'aluguel_residencial',
                'price_kz': 500.00,
                'fields': {
                    'proprietario_nome': {
                        'label': 'Nome do Proprietário',
                        'type': 'text',
                        'required': True
                    },
                    'proprietario_bi': {
                        'label': 'BI do Proprietário',
                        'type': 'text',
                        'required': True
                    },
                    'inquilino_nome': {
                        'label': 'Nome do Inquilino',
                        'type': 'text',
                        'required': True
                    },
                    'inquilino_bi': {
                        'label': 'BI do Inquilino',
                        'type': 'text',
                        'required': True
                    },
                    'imovel_descricao': {
                        'label': 'Descrição do Imóvel',
                        'type': 'textarea',
                        'required': True,
                        'placeholder': 'Endereço completo, tipo, número de quartos, etc.'
                    },
                    'valor_aluguel': {
                        'label': 'Valor do Aluguel (Kz)',
                        'type': 'number',
                        'required': True
                    },
                    'valor_caucao': {
                        'label': 'Valor da Caução (Kz)',
                        'type': 'number',
                        'required': True
                    },
                    'prazo_contrato': {
                        'label': 'Prazo do Contrato',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'Ex: 12 meses'
                    },
                    'data_inicio': {
                        'label': 'Data de Início',
                        'type': 'date',
                        'required': True
                    },
                    'dia_vencimento': {
                        'label': 'Dia de Vencimento',
                        'type': 'number',
                        'required': True,
                        'placeholder': 'Dia do mês para pagamento'
                    }
                }
            }
        )

        # Contratos de Prestação de Serviços (600 KZ)
        
        # Contrato de Serviços Profissionais
        Template.objects.get_or_create(
            name='Contrato de Serviços Profissionais',
            category='contrato_servicos',
            defaults={
                'description': 'Contrato para prestação de serviços profissionais especializados',
                'subcategory': 'servicos_profissionais',
                'price_kz': 600.00,
                'fields': {
                    'prestador_nome': {
                        'label': 'Nome do Prestador',
                        'type': 'text',
                        'required': True
                    },
                    'prestador_qualificacao': {
                        'label': 'Qualificação Profissional',
                        'type': 'text',
                        'required': True
                    },
                    'prestador_nif': {
                        'label': 'NIF do Prestador',
                        'type': 'text',
                        'required': True
                    },
                    'contratante_nome': {
                        'label': 'Nome do Contratante',
                        'type': 'text',
                        'required': True
                    },
                    'contratante_nif': {
                        'label': 'NIF do Contratante',
                        'type': 'text',
                        'required': True
                    },
                    'objeto_contrato': {
                        'label': 'Objeto do Contrato',
                        'type': 'textarea',
                        'required': True,
                        'placeholder': 'Descreva detalhadamente os serviços profissionais'
                    },
                    'valor_honorarios': {
                        'label': 'Valor dos Honorários (Kz)',
                        'type': 'number',
                        'required': True
                    },
                    'forma_pagamento': {
                        'label': 'Forma de Pagamento',
                        'type': 'select',
                        'required': True,
                        'options': ['Mensal', 'Por etapa', 'À vista', 'Quinzenal']
                    },
                    'prazo_execucao': {
                        'label': 'Prazo de Execução',
                        'type': 'text',
                        'required': True
                    },
                    'obrigacoes_prestador': {
                        'label': 'Obrigações do Prestador',
                        'type': 'textarea',
                        'required': True
                    },
                    'obrigacoes_contratante': {
                        'label': 'Obrigações do Contratante',
                        'type': 'textarea',
                        'required': True
                    },
                    'confidencialidade': {
                        'label': 'Cláusula de Confidencialidade',
                        'type': 'select',
                        'required': True,
                        'options': ['Sim', 'Não']
                    }
                }
            }
        )

        # Contratos Complexos (700 KZ)
        
        # Contrato de Compra e Venda de Imóvel
        Template.objects.get_or_create(
            name='Contrato de Compra e Venda de Imóvel',
            category='contrato_complexo',
            defaults={
                'description': 'Contrato completo para compra e venda de imóveis',
                'subcategory': 'compra_venda_imovel',
                'price_kz': 700.00,
                'fields': {
                    'vendedor_nome': {
                        'label': 'Nome do Vendedor',
                        'type': 'text',
                        'required': True
                    },
                    'vendedor_bi': {
                        'label': 'BI do Vendedor',
                        'type': 'text',
                        'required': True
                    },
                    'vendedor_estado_civil': {
                        'label': 'Estado Civil do Vendedor',
                        'type': 'select',
                        'required': True,
                        'options': ['Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)']
                    },
                    'comprador_nome': {
                        'label': 'Nome do Comprador',
                        'type': 'text',
                        'required': True
                    },
                    'comprador_bi': {
                        'label': 'BI do Comprador',
                        'type': 'text',
                        'required': True
                    },
                    'imovel_endereco': {
                        'label': 'Endereço do Imóvel',
                        'type': 'textarea',
                        'required': True,
                        'placeholder': 'Endereço completo e detalhado'
                    },
                    'imovel_descricao': {
                        'label': 'Descrição do Imóvel',
                        'type': 'textarea',
                        'required': True,
                        'placeholder': 'Área, número de quartos, características, etc.'
                    },
                    'numero_titulo': {
                        'label': 'Número do Título de Propriedade',
                        'type': 'text',
                        'required': True
                    },
                    'area_terreno': {
                        'label': 'Área do Terreno (m²)',
                        'type': 'number',
                        'required': True
                    },
                    'area_construida': {
                        'label': 'Área Construída (m²)',
                        'type': 'number',
                        'required': True
                    },
                    'valor_venda': {
                        'label': 'Valor da Venda (Kz)',
                        'type': 'number',
                        'required': True
                    },
                    'forma_pagamento': {
                        'label': 'Forma de Pagamento',
                        'type': 'select',
                        'required': True,
                        'options': ['À vista', 'Entrada + parcelas', 'Financiamento bancário']
                    },
                    'valor_entrada': {
                        'label': 'Valor da Entrada (Kz)',
                        'type': 'number',
                        'required': False,
                        'placeholder': 'Se aplicável'
                    },
                    'data_escritura': {
                        'label': 'Data da Escritura',
                        'type': 'date',
                        'required': True
                    },
                    'encargos_vendedor': {
                        'label': 'Encargos do Vendedor',
                        'type': 'textarea',
                        'required': True,
                        'placeholder': 'Impostos, certidões, etc.'
                    },
                    'encargos_comprador': {
                        'label': 'Encargos do Comprador',
                        'type': 'textarea',
                        'required': True,
                        'placeholder': 'Taxas de transferência, etc.'
                    }
                }
            }
        )

        self.stdout.write('✓ Templates de Contratos criados')
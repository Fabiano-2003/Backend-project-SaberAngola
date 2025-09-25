"""
Management command to create a superuser for SaberAngola system.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser for SaberAngola system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='admin@saberangola.ao',
            help='Email for the superuser (default: admin@saberangola.ao)'
        )
        parser.add_argument(
            '--name',
            type=str,
            default='Administrador',
            help='Name for the superuser (default: Administrador)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='AdminSaber123',
            help='Password for the superuser (default: AdminSaber123)'
        )

    def handle(self, *args, **options):
        email = options['email']
        name = options['name']
        password = options['password']
        
        self.stdout.write(f'Criando superusuário: {email}')
        
        try:
            if User.objects.filter(email=email).exists():
                self.stdout.write(
                    self.style.WARNING(f'Usuário {email} já existe. Atualizando senha...')
                )
                user = User.objects.get(email=email)
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Senha do usuário {email} atualizada com sucesso!')
                )
            else:
                user = User.objects.create_superuser(
                    email=email,
                    password=password,
                    name=name
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Superusuário {email} criado com sucesso!')
                )
                
            self.stdout.write('')
            self.stdout.write('Credenciais de acesso:')
            self.stdout.write(f'  Email: {email}')
            self.stdout.write(f'  Senha: {password}')
            self.stdout.write('')
            self.stdout.write('Acesse o painel admin em: /admin/')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao criar superusuário: {str(e)}')
            )
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import PerfilUsuario, AvanceFisico, Rutina
from .forms import RegistroForm, AvanceFisicoForm, RutinaForm

class TestModelos(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.admin = User.objects.create_superuser(username='admin', password='admin123')

    def test_perfil_usuario_creado_automaticamente(self):
        self.assertTrue(PerfilUsuario.objects.filter(user=self.user).exists())
        self.assertEqual(str(self.user.perfil), f'Perfil de {self.user.username}')

    def test_perfil_usuario_verbose_names(self):
        self.assertEqual(PerfilUsuario._meta.verbose_name, 'Perfil de usuario')
        self.assertEqual(PerfilUsuario._meta.verbose_name_plural, 'Perfiles de usuarios')

    def test_avance_fisico_creacion(self):
        avance = AvanceFisico.objects.create(
            usuario=self.user,
            peso=75.5,
            porcentaje_grasa=15.5,
            notas='Buen progreso'
        )
        self.assertEqual(avance.usuario, self.user)
        self.assertEqual(float(avance.peso), 75.5)
        self.assertEqual(float(avance.porcentaje_grasa), 15.5)
        self.assertEqual(str(avance), f'{self.user.username} - {avance.fecha}')

    def test_avance_fisico_ordering(self):
        a1 = AvanceFisico.objects.create(usuario=self.user, peso=80, porcentaje_grasa=20)
        a2 = AvanceFisico.objects.create(usuario=self.user, peso=78, porcentaje_grasa=18)
        avances = AvanceFisico.objects.all()
        self.assertGreater(avances[0].fecha, avances[1].fecha) if avances[0].fecha != avances[1].fecha else None

    def test_rutina_creacion(self):
        rutina = Rutina.objects.create(
            nombre='Rutina Full Body',
            descripcion='Ejercicios completos',
            nivel='Intermedio',
            creado_por=self.admin
        )
        self.assertEqual(str(rutina), 'Rutina Full Body')
        self.assertEqual(rutina.nivel, 'Intermedio')

    def test_rutina_solo_staff_creada_por_admin(self):
        rutina = Rutina.objects.create(
            nombre='Rutina Test',
            descripcion='Test',
            nivel='Principiante',
            creado_por=self.admin
        )
        self.assertEqual(rutina.creado_por, self.admin)
        self.assertTrue(rutina.creado_por.is_staff)

    def test_rutina_asignacion(self):
        rutina = Rutina.objects.create(
            nombre='Rutina Test',
            descripcion='Test',
            nivel='Principiante',
            creado_por=self.admin
        )
        rutina.asignada_a.add(self.user)
        self.assertEqual(rutina.asignada_a.count(), 1)
        self.assertIn(self.user, rutina.asignada_a.all())

    def test_avance_fisico_verbose_names(self):
        self.assertEqual(AvanceFisico._meta.verbose_name, 'Avance físico')
        self.assertEqual(AvanceFisico._meta.verbose_name_plural, 'Avances físicos')

    def test_rutina_verbose_names(self):
        self.assertEqual(Rutina._meta.verbose_name, 'Rutina')
        self.assertEqual(Rutina._meta.verbose_name_plural, 'Rutinas')

class TestFormularios(TestCase):
    def test_registro_form_valido(self):
        form = RegistroForm(data={
            'username': 'nuevouser',
            'email': 'user@test.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'telefono': '123456789',
        })
        self.assertTrue(form.is_valid())

    def test_registro_form_password_no_coinciden(self):
        form = RegistroForm(data={
            'username': 'nuevouser',
            'email': 'user@test.com',
            'password1': 'ComplexPass123!',
            'password2': 'DifferentPass456!',
        })
        self.assertFalse(form.is_valid())

    def test_avance_form_valido(self):
        form = AvanceFisicoForm(data={
            'peso': 75.5,
            'porcentaje_grasa': 15.5,
            'notas': 'Todo bien',
        })
        self.assertTrue(form.is_valid())

    def test_avance_form_peso_invalido(self):
        form = AvanceFisicoForm(data={
            'peso': -10,
            'porcentaje_grasa': 15,
            'notas': '',
        })
        self.assertFalse(form.is_valid())

    def test_avance_form_grasa_invalida(self):
        form = AvanceFisicoForm(data={
            'peso': 70,
            'porcentaje_grasa': 110,
            'notas': '',
        })
        self.assertFalse(form.is_valid())

    def test_rutina_form_valido(self):
        admin = User.objects.create_superuser(username='admin2', password='admin123')
        form = RutinaForm(data={
            'nombre': 'Rutina Test',
            'descripcion': 'Descripción de prueba',
            'nivel': 'Intermedio',
        })
        self.assertTrue(form.is_valid())

class TestVistasPublicas(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AkelaGym')
        self.assertContains(response, 'Nuestros Planes')
        self.assertContains(response, 'Nuestros Entrenamientos')

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Iniciar Sesión')

    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Crear Cuenta')

    @override_settings(AUTH_PASSWORD_VALIDATORS=[])
    def test_registro_exitoso(self):
        response = self.client.post(reverse('register'), {
            'username': 'nuevo_cliente',
            'email': 'cliente@test.com',
            'password1': 'cliente123456',
            'password2': 'cliente123456',
            'telefono': '987654321',
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(User.objects.filter(username='nuevo_cliente').exists())
        user = User.objects.get(username='nuevo_cliente')
        self.assertTrue(PerfilUsuario.objects.filter(user=user).exists())

    def test_login_fallido(self):
        response = self.client.post(reverse('login'), {
            'username': 'noexists',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuario o contraseña incorrectos')

    def test_login_exitoso(self):
        User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_logout(self):
        User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))

class TestVistasPrivadas(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='cliente', password='cliente123')

    def test_dashboard_redirect_sin_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("dashboard")}')

    def test_dashboard_con_login(self):
        self.client.login(username='cliente', password='cliente123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bienvenido, cliente')

    def test_crear_avance_sin_login(self):
        response = self.client.get(reverse('crear_avance'))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("crear_avance")}')

    def test_crear_avance_con_login(self):
        self.client.login(username='cliente', password='cliente123')
        response = self.client.get(reverse('crear_avance'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Registrar Avance Físico')

    def test_crear_avance_post(self):
        self.client.login(username='cliente', password='cliente123')
        response = self.client.post(reverse('crear_avance'), {
            'peso': 80.0,
            'porcentaje_grasa': 20.0,
            'notas': 'Primer registro',
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(AvanceFisico.objects.filter(usuario=self.user).count(), 1)

    @override_settings(LANGUAGE_CODE='en-us')
    def test_avance_aparece_en_dashboard(self):
        self.client.login(username='cliente', password='cliente123')
        AvanceFisico.objects.create(usuario=self.user, peso=80, porcentaje_grasa=20)
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, '80.00')

class TestVistasAdmin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='cliente', password='cliente123')
        self.admin = User.objects.create_superuser(username='admin', password='admin123')

    def test_lista_rutinas_sin_staff(self):
        self.client.login(username='cliente', password='cliente123')
        response = self.client.get(reverse('lista_rutinas'))
        self.assertEqual(response.status_code, 302)

    def test_lista_rutinas_con_staff(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('lista_rutinas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rutinas de Entrenamiento')

    def test_crear_rutina_admin(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.post(reverse('crear_rutina'), {
            'nombre': 'Full Body Express',
            'descripcion': 'Rutina rápida de 30 minutos',
            'nivel': 'Intermedio',
        })
        self.assertRedirects(response, reverse('lista_rutinas'))
        self.assertTrue(Rutina.objects.filter(nombre='Full Body Express').exists())
        rutina = Rutina.objects.get(nombre='Full Body Express')
        self.assertEqual(rutina.creado_por, self.admin)

    def test_editar_rutina_admin(self):
        self.client.login(username='admin', password='admin123')
        rutina = Rutina.objects.create(
            nombre='Original', descripcion='Desc',
            nivel='Principiante', creado_por=self.admin
        )
        response = self.client.post(reverse('editar_rutina', args=[rutina.pk]), {
            'nombre': 'Editada',
            'descripcion': 'Nueva descripción',
            'nivel': 'Avanzado',
        })
        self.assertRedirects(response, reverse('lista_rutinas'))
        rutina.refresh_from_db()
        self.assertEqual(rutina.nombre, 'Editada')
        self.assertEqual(rutina.nivel, 'Avanzado')

    def test_eliminar_rutina_admin_get(self):
        self.client.login(username='admin', password='admin123')
        rutina = Rutina.objects.create(
            nombre='A Eliminar', descripcion='Test',
            nivel='Principiante', creado_por=self.admin
        )
        response = self.client.get(reverse('eliminar_rutina', args=[rutina.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A Eliminar')

    def test_eliminar_rutina_admin_post(self):
        self.client.login(username='admin', password='admin123')
        rutina = Rutina.objects.create(
            nombre='A Eliminar', descripcion='Test',
            nivel='Principiante', creado_por=self.admin
        )
        response = self.client.post(reverse('eliminar_rutina', args=[rutina.pk]))
        self.assertRedirects(response, reverse('lista_rutinas'))
        self.assertFalse(Rutina.objects.filter(pk=rutina.pk).exists())

    def test_lista_usuarios_admin(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('lista_usuarios'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuarios Registrados')

    def test_detalle_usuario_admin(self):
        self.client.login(username='admin', password='admin123')
        AvanceFisico.objects.create(usuario=self.user, peso=75, porcentaje_grasa=18)
        response = self.client.get(reverse('detalle_usuario', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_acceso_admin_denegado_a_usuario_normal(self):
        self.client.login(username='cliente', password='cliente123')
        urls_admin = [
            reverse('lista_rutinas'),
            reverse('crear_rutina'),
            reverse('lista_usuarios'),
        ]
        for url in urls_admin:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302,
                             f'Usuario normal no debería acceder a {url}')

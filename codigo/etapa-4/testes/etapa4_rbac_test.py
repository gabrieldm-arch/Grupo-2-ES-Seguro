import unittest

# Prática 1: Controle de Autorização (RBAC)
# Decorator que valida o papel do usuário antes de permitir acesso à função

def require_role(required_role):
    def decorator(func):
        def wrapper(user, *args, **kwargs):
            # Validação Server-Side do Controle de Acesso
            if user.get("role") != required_role:
                # O evento seria logado aqui em um sistema real
                raise PermissionError(f"403 Forbidden: Papel '{user.get('role')}' não possui acesso a este recurso.")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

# Endpoint administrativo protegido
@require_role("admin")
def update_commission(user, new_rate):
    return f"200 OK: Comissão global atualizada para {new_rate}%"

class TestAuthorization(unittest.TestCase):
    def setUp(self):
        # Mocks de tokens JWT decodificados
        self.user_partner = {"id": "123", "role": "restaurant"}
        self.user_admin = {"id": "999", "role": "admin"}

    def test_ts01_restaurant_cannot_access_admin_function(self):
        # TS01: Operador de Restaurante tenta chamar a função de zerar comissões
        with self.assertRaises(PermissionError) as context:
            update_commission(self.user_partner, 0)
        self.assertIn("403 Forbidden", str(context.exception))
        print("TS01 Passou: Acesso negado para restaurante.")

    def test_ts02_admin_can_access_admin_function(self):
        # TS02: Administrador chama a função de atualizar comissões
        response = update_commission(self.user_admin, 10)
        self.assertEqual(response, "200 OK: Comissão global atualizada para 10%")
        print("TS02 Passou: Acesso permitido para administrador.")

if __name__ == '__main__':
    unittest.main(verbosity=2)

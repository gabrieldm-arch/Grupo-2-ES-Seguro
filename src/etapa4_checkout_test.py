import unittest

# Banco de dados simulado de produtos
DB_PRODUCTS = {
    "PZ01": {"name": "Pizza Marguerita", "price": 50.00},
    "PZ02": {"name": "Pizza Calabresa", "price": 45.00},
    "B01": {"name": "Refrigerante 2L", "price": 10.00}
}

# Prática 2: Prevenção de Mass Assignment

def process_checkout(cart_items, client_total_amount):
    server_calculated_total = 0.0

    # Recálculo obrigatório no servidor consultando a fonte de verdade
    for item_id in cart_items:
        if item_id in DB_PRODUCTS:
            server_calculated_total += DB_PRODUCTS[item_id]["price"]
        else:
            raise ValueError(f"404 Not Found: Produto {item_id} não encontrado no catálogo.")

    # Validação de divergência financeira
    if server_calculated_total != client_total_amount:
        # Evento de fraude seria disparado aqui para a equipe de monitoramento
        raise ValueError(
            f"400 Bad Request: Fraude detectada. O valor fornecido pelo cliente (R${client_total_amount}) "
            f"não confere com o cálculo do servidor (R${server_calculated_total})."
        )

    return f"200 OK: Pedido aceito. Total cobrado com segurança: R${server_calculated_total:.2f}"

class TestCheckoutValidation(unittest.TestCase):
    
    def test_ts03_client_tampers_total_amount(self):
        # TS03: Cliente malicioso envia um pedido de 3 pizzas mas altera o total_amount para 0.00
        malicious_cart = ["PZ01", "PZ01", "PZ01"]
        client_fake_total = 0.00
        
        with self.assertRaises(ValueError) as context:
            process_checkout(malicious_cart, client_fake_total)
            
        self.assertIn("Fraude detectada", str(context.exception))
        print("TS03 Passou: Fraude de alteração de valor (Mass Assignment) bloqueada.")

    def test_ts04_client_sends_valid_order(self):
        # TS04: Cliente legítimo envia pedido com os valores e produtos idênticos ao catálogo
        valid_cart = ["PZ02", "B01"]
        client_valid_total = 55.00
        
        response = process_checkout(valid_cart, client_valid_total)
        self.assertIn("200 OK", response)
        self.assertIn("R$55.00", response)
        print("TS04 Passou: Pedido legítimo processado com sucesso.")

if __name__ == '__main__':
    unittest.main(verbosity=2)

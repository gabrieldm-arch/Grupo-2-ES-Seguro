# Etapa 4 — Código Seguro e Testes de Segurança

## 4.1 Escolha das Práticas

Para garantir que a implementação do App de Delivery cumpra os Requisitos de Segurança definidos na Etapa 3, selecionamos duas práticas fundamentais de código seguro com base na documentação da **OWASP Cheat Sheet Series**. Ambas focam na mitigação direta dos riscos de maior impacto sistêmico e financeiro da plataforma.

### Prática 1: Controle de Acesso e Autorização (RBAC *Server-Side*)
* **Referência OWASP:** *Access Control Cheat Sheet* / *Authorization Cheat Sheet*.
* **Risco Atendido:** **R06** — Escalonamento de Privilégio via Broken Access Control no Painel Administrativo.
* **Requisito de Segurança Relacionado:** **RS-02** — O sistema deve implementar controle de acesso baseado em papéis (RBAC) verificado no servidor para todas as rotas administrativas (`/admin/*`).
* **Justificativa:** Conforme preconizado pela OWASP, a autorização deve ser aplicada de maneira centralizada no *backend* e nunca depender exclusivamente da ocultação de botões na interface do usuário (UI). A implementação desta prática assegura que qualquer requisição direcionada aos endpoints administrativos rejeite tokens de parceiros ou clientes (HTTP 403), exigindo a presença explícita da *claim* de Administrador no JWT.

### Prática 2: Validação de Entrada e Lógica de Negócio
* **Referência OWASP:** *Input Validation Cheat Sheet* / *Mass Assignment Cheat Sheet*.
* **Risco Atendido:** **R02** — Manipulação do Valor do Pedido na Requisição (Tampering).
* **Requisito de Segurança Relacionado:** **RS-03** — O sistema deve recalcular obrigatoriamente o valor total de todo pedido no servidor com base nos preços registrados no banco de dados.
* **Justificativa:** A regra fundamental da OWASP para transações é tratar toda entrada proveniente do cliente como não confiável (*untrusted data*). Ao aplicar o recálculo *server-side*, o sistema ignora qualquer manipulação do parâmetro `total_amount` feita via *proxies* interceptadores. Adicionalmente, o uso de assinaturas HMAC garante a integridade da requisição, inviabilizando fraudes diretas na API de Checkout e no Gateway de Pagamento.

## 4.2 Testes e Implementação

Abaixo estão definidos os casos de uso válidos e inválidos para cada uma das práticas escolhidas, seguidos da explicação de como foram implementados.

*Nota: O código-fonte completo em Python, incluindo os testes executáveis (TDD), foi criado e disponibilizado na pasta `codigo/etapa-4/testes/` do repositório (`etapa4_rbac_test.py` e `etapa4_checkout_test.py`).*

### Prática 1: Controle de Acesso (RBAC)

| Teste | Entrada ou ação | Resultado esperado |
| :--- | :--- | :--- |
| **TS01** *(Inválido)* | Operador de Restaurante tenta acessar a função administrativa de comissões | A solicitação é recusada com erro `HTTP 403 Forbidden` |
| **TS02** *(Válido)* | Administrador autorizado acessa a mesma função | A solicitação é permitida (`HTTP 200 OK`) |

**Forma de realização:** Criamos um *decorator* Python `@require_role("admin")` que envolve os endpoints administrativos. Antes de executar a função, ele extrai o papel (role) do objeto do usuário (simulando um token JWT) e valida contra a regra. Se falhar, lança uma `PermissionError` (403), cumprindo o TS01.

### Prática 2: Validação Server-Side (Mass Assignment)

| Teste | Entrada ou ação | Resultado esperado |
| :--- | :--- | :--- |
| **TS03** *(Inválido)* | Cliente envia um pedido de R$ 150, mas altera maliciosamente o parâmetro `total_amount` para R$ 0.00 | O servidor rejeita a transação por detecção de fraude financeira (`HTTP 400 Bad Request`) |
| **TS04** *(Válido)* | Cliente envia pedido com total exato correspondente ao catálogo | A transação é processada com sucesso (`HTTP 200 OK`) |

**Forma de realização:** Implementamos a função `process_checkout` que obrigatoriamente itera sobre os itens do carrinho e busca os preços reais em um dicionário simulando o banco de dados (`DB_PRODUCTS`). O cálculo final do servidor é comparado com o valor enviado pelo cliente. Qualquer divergência lança um `ValueError`, cumprindo o TS03 e evitando o recebimento de pedidos adulterados.

## 4.4 Referências

As referências abaixo embasaram diretamente as escolhas de práticas, a estrutura dos testes e a implementação dos controles descritos nas seções 4.1, 4.2 e 4.3.

**Prática 1 — Controle de Acesso e Autorização (RBAC Server-Side)**

- OWASP. *Access Control Cheat Sheet*. Disponível em: https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html
- OWASP. *Authorization Cheat Sheet*. Disponível em: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP Top 10 2021 — A01: Broken Access Control. Disponível em: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- MITRE. *CWE-285: Improper Authorization*. Disponível em: https://cwe.mitre.org/data/definitions/285.html
- MITRE. *CWE-862: Missing Authorization*. Disponível em: https://cwe.mitre.org/data/definitions/862.html

**Prática 2 — Validação de Entrada e Lógica de Negócio (Mass Assignment / Server-Side Recalculation)**

- OWASP. *Input Validation Cheat Sheet*. Disponível em: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
- OWASP. *Mass Assignment Cheat Sheet*. Disponível em: https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html
- OWASP Top 10 2021 — A04: Insecure Design. Disponível em: https://owasp.org/Top10/A04_2021-Insecure_Design/
- MITRE. *CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes*. Disponível em: https://cwe.mitre.org/data/definitions/915.html

**Referências gerais utilizadas ao longo da Etapa 4**

- OWASP. *OWASP Cheat Sheet Series*. Disponível em: https://cheatsheetseries.owasp.org/
- OWASP. *Testing Guide v4.2 — Testing for Privilege Escalation*. Disponível em: https://owasp.org/www-project-web-security-testing-guide/
- OWASP. *JSON Web Token Cheat Sheet for Java*. Disponível em: https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html

### Considerações Finais — Etapa 4

A Etapa 4 materializou as decisões de arquitetura da Etapa 3 em implementações concretas e verificáveis, demonstrando que os controles de segurança propostos são tecnicamente viáveis e testáveis antes mesmo da existência de um sistema completo em produção.

As duas práticas implementadas — controle de acesso RBAC server-side e validação de lógica de negócio com recálculo server-side — foram escolhidas por atacarem diretamente os dois riscos de maior impacto sistêmico e financeiro do registro: R06 (Broken Access Control) e R02 (Manipulação de Valor do Pedido). A abordagem TDD adotada — escrever os testes de segurança antes da lógica de negócio — garantiu que os critérios de rejeição de ataques (TS01 e TS03) fossem tratados como requisitos de primeira classe, e não como verificações opcionais adicionadas ao final do desenvolvimento.

Um resultado relevante desta etapa foi demonstrar que segurança por design não exige complexidade excessiva: o decorator `@require_role("admin")` e a função `process_checkout` com recálculo obrigatório são implementações concisas que eliminam completamente as condições habilitadoras de R06 e R02 quando aplicadas de forma consistente em todos os endpoints relevantes. A dificuldade não está na complexidade técnica dos controles, mas na disciplina de aplicá-los sem exceções.

A principal limitação desta etapa é que os testes foram executados em ambiente isolado com dados simulados, sem integração com o banco de dados real, o gateway de pagamento ou o fluxo completo de autenticação JWT. A validação em ambiente integrado e com tráfego real será realizada na Etapa 5, onde o OWASP ZAP verificará dinamicamente se os controles implementados resistem a vetores de ataque automatizados.


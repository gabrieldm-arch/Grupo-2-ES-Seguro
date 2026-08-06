# Casos de Abuso — App de Delivery de Comida

> **Disciplina:** Engenharia de Software Seguro — Codefólio
> **Sistema Analisado:** App de Delivery de Comida *(Plataforma Integrada de Pedidos e Entregas Online)*
> **Referência:** Seção 8.5 — Modelagem STRIDE

---

## Visão Geral

Os **casos de abuso** descrevem cenários nos quais atores mal-intencionados exploram funcionalidades legítimas ou vulnerabilidades do sistema para causar dano. Eles são derivados diretamente da análise STRIDE e complementam os casos de uso normais ao revelar as **intenções hostis** que o sistema deve estar preparado para resistir.

Cada caso de abuso está vinculado a:

- Uma **categoria STRIDE** (ameaça raiz),
- Um **ativo crítico** identificado na seção 8.3,
- Um **ator malicioso** (interno ou externo),
- E uma **contramedida** de mitigação recomendada.

---

## CA-01 — Sequestro de Sessão de Entregador *(Spoofing)*

| Campo                  | Detalhe |
|------------------------|---------|
| **ID**                 | CA-01 |
| **Categoria STRIDE**   | Spoofing |
| **Ativo Afetado**      | Sessões e Tokens de Autenticação (JWT/OAuth2) |
| **Ator Malicioso**     | Atacante externo |
| **Pré-condição**       | O atacante obteve acesso ao token JWT de um entregador ativo (via phishing, sniffing em rede insegura ou malware no dispositivo móvel) |

### Descrição do Abuso

Um atacante captura o token de sessão (JWT) de um entregador legítimo em atividade e utiliza esse token em um dispositivo diferente para se autenticar no app do entregador. Com a sessão sequestrada, o atacante aceita chamadas de corrida em nome do entregador real e coleta as refeições nos restaurantes, desviando as mercadorias sem jamais realizar a entrega.

### Fluxo de Abuso (Passo a Passo)

```
1. Atacante intercepta token JWT do entregador (phishing, MITM, malware).
2. Atacante configura o token no cabeçalho Authorization de um cliente HTTP.
3. Atacante acessa a API do app do entregador com identidade legítima.
4. Atacante aceita corridas, coleta pedidos nos restaurantes.
5. Pedido nunca é entregue ao cliente.
6. Sistema registra a corrida como aceita pelo entregador legítimo.
```

### Impacto

- Roubo de mercadorias e prejuízo financeiro aos restaurantes parceiros.
- Risco à segurança física dos clientes (pedido nunca chega).
- Dano reputacional severo à plataforma.
- Possível banimento injusto do entregador legítimo cujo token foi roubado.

### Contramedidas Recomendadas

- Vinculação do token JWT ao `device_id` e ao endereço IP de origem, invalidando uso em dispositivos não reconhecidos.
- Implementação de renovação de tokens com expiração curta (ex.: 15 minutos) e uso de refresh tokens com rotação.
- Autenticação multifator (MFA/TOTP) obrigatória para o login inicial do entregador.
- Alerta automático ao entregador via push/SMS ao detectar sessão simultânea em outro dispositivo.
- Monitoramento de anomalias: sessão ativa em geolocalização incompatível com a última posição registrada.

---

## CA-02 — Manipulação do Valor de Pedido na Requisição *(Tampering)*

| Campo                  | Detalhe |
|------------------------|---------|
| **ID**                 | CA-02 |
| **Categoria STRIDE**   | Tampering |
| **Ativo Afetado**      | APIs de Checkout e Gateway de Pagamento |
| **Ator Malicioso**     | Cliente mal-intencionado |
| **Pré-condição**       | O cliente utiliza um proxy HTTP (ex.: Burp Suite, mitmproxy) para interceptar o tráfego entre o app mobile e a API de backend |

### Descrição do Abuso

Durante o fluxo de finalização do pedido, o cliente intercepta a requisição HTTP enviada pelo app mobile e altera o parâmetro `total_amount` (ou equivalente) para `0.00` antes que ela chegue à API de cobrança. Se o backend não revalidar o valor no servidor — confiando cegamente nos dados enviados pelo cliente — o pedido é processado sem cobrança.

### Fluxo de Abuso (Passo a Passo)

```
1. Cliente adiciona itens ao carrinho normalmente pelo app.
2. Cliente configura proxy HTTP no dispositivo para interceptar tráfego.
3. No momento do "confirmar pedido", o app envia requisição POST /checkout.
4. Atacante intercepta e edita o campo total_amount de R$ 89,90 para R$ 0,00.
5. Requisição modificada é encaminhada ao servidor.
6. Se o backend não revalida o preço, o pedido é aprovado sem cobrança.
7. Pedido é processado normalmente: restaurante prepara, entregador leva.
```

### Impacto

- Fraude financeira direta contra a plataforma.
- Perda de receita e falha no repasse ao restaurante parceiro.
- Possível cadeia de fraudes sistemáticas se a vulnerabilidade não for detectada.

### Contramedidas Recomendadas

- **Nunca confiar em valores enviados pelo cliente**: o backend deve recalcular o total do pedido com base nos preços armazenados no banco de dados no momento do checkout.
- Assinar criptograficamente (HMAC) o payload do carrinho para detectar qualquer modificação em trânsito.
- Validação de integridade: se `total_amount` recebido divergir do valor calculado pelo servidor, rejeitar a transação e registrar tentativa de fraude.
- Aplicar TLS mútuo (mTLS) nos endpoints de checkout para dificultar interceptação.
- Monitoramento de pedidos com valor zerado ou abaixo do mínimo como sinal de alerta de fraude.

---

## CA-03 — Golpe do Estorno por Falsa Não-Entrega *(Repudiation)*

| Campo                  | Detalhe |
|------------------------|---------|
| **ID**                 | CA-03 |
| **Categoria STRIDE**   | Repudiation |
| **Ativo Afetado**      | App do Entregador, Logs de Auditoria |
| **Ator Malicioso**     | Cliente desonesto |
| **Pré-condição**       | O sistema não registra provas irrefutáveis da conclusão da entrega (ex.: confirmação com código OTP, foto, assinatura digital ou log de geolocalização no endereço do cliente) |

### Descrição do Abuso

Um cliente recebe corretamente o pedido, mas aciona o suporte da plataforma alegando que o entregador nunca compareceu. Sem provas auditáveis suficientes da conclusão da entrega, a plataforma realiza o estorno ao cliente (chargeback). O entregador, que realizou o serviço de boa-fé, fica com reputação prejudicada e pode ser penalizado ou banido injustamente.

### Fluxo de Abuso (Passo a Passo)

```
1. Entregador conclui a entrega normalmente no endereço do cliente.
2. Cliente recebe o pedido, mas não confirma a entrega pelo app (ou confirma e depois contesta).
3. Cliente abre chamado alegando não-entrega.
4. Plataforma, sem logs ou provas sólidas, defere o estorno.
5. Restaurante e/ou entregador arcam com o prejuízo.
6. Cliente repete o golpe em pedidos futuros.
```

### Impacto

- Prejuízo financeiro recorrente para a plataforma e restaurantes.
- Banimento injusto de entregadores honestos.
- Degradação da confiança dos parceiros logísticos na plataforma.

### Contramedidas Recomendadas

- **Código OTP de confirmação de entrega**: gerado para o pedido e informado pelo cliente ao entregador no momento da entrega; a conclusão só é registrada com a validação do código.
- Registro de geolocalização com timestamp no momento da marcação de "entregue" no app do entregador.
- Foto obrigatória da entrega (via app) em pedidos acima de determinado valor, armazenada em log imutável.
- Log de auditoria com assinatura criptográfica para impedir adulteração posterior dos registros.
- Análise de comportamento: clientes com histórico de estornos frequentes devem ser sinalizados para revisão manual.

---

## CA-04 — Extração em Massa de Dados Pessoais por IDOR *(Information Disclosure)*

| Campo                  | Detalhe |
|------------------------|---------|
| **ID**                 | CA-04 |
| **Categoria STRIDE**   | Information Disclosure |
| **Ativo Afetado**      | Banco de Dados Central (PII e Pedidos), Serviços de Roteamento (GPS) |
| **Ator Malicioso**     | Atacante externo (ou insider com acesso limitado) |
| **Pré-condição**       | Existência de vulnerabilidade IDOR (Insecure Direct Object Reference) em endpoints da API que retornam dados de usuários por identificadores sequenciais ou previsíveis |

### Descrição do Abuso

Um atacante autenticado como cliente comum descobre que a API retorna dados de outros usuários ao manipular o parâmetro de ID na requisição (ex.: `GET /api/users/1042` → testa `GET /api/users/1043`, `1044`...). Com um script automatizado, o atacante itera sobre os IDs e extrai em massa CPFs, endereços residenciais, históricos de pedidos e coordenadas GPS de clientes e entregadores.

### Fluxo de Abuso (Passo a Passo)

```
1. Atacante cria conta legítima de cliente na plataforma.
2. Atacante observa sua própria requisição: GET /api/profile/10432.
3. Atacante testa: GET /api/profile/10431, /10430... — recebe dados de outros usuários.
4. Atacante automatiza iteração com script, extraindo milhares de registros.
5. Dados são exfiltrados: CPFs, endereços, GPS, histórico de compras.
6. Dados vendidos em fóruns underground ou usados para ataques direcionados.
```

### Impacto

- Multas milionárias por violação à LGPD (Lei 13.709/2018).
- Exposição física de clientes e entregadores (risco de perseguição, assalto).
- Destruição da reputação e confiança na plataforma.
- Possível ação civil coletiva das vítimas.

### Contramedidas Recomendadas

- **Autorização baseada em objeto**: todo endpoint deve verificar se o usuário autenticado tem permissão para acessar o recurso solicitado, independentemente do ID informado.
- Uso de UUIDs ou identificadores não sequenciais para tornar a enumeração impraticável.
- Rate limiting nos endpoints de perfil para detectar e bloquear varreduras automatizadas.
- Logging e alertas automáticos para requisições a múltiplos IDs distintos em curto intervalo.
- Testes regulares de IDOR como parte do processo de pentest e code review.

---

## CA-05 — Ataque de Negação de Serviço por Botnet em Horário de Pico *(Denial of Service)*

| Campo                  | Detalhe |
|------------------------|---------|
| **ID**                 | CA-05 |
| **Categoria STRIDE**   | Denial of Service (DoS / DDoS) |
| **Ativo Afetado**      | Servidores e Infraestrutura de Backend, Filas de Mensagens |
| **Ator Malicioso**     | Atacante externo (operador de botnet) |
| **Pré-condição**       | A plataforma não possui mecanismos robustos de rate limiting, WAF ou proteção anti-DDoS ativados nos endpoints públicos |

### Descrição do Abuso

Um atacante controla uma botnet e direciona milhares de requisições simultâneas aos endpoints públicos da plataforma (ex.: busca de restaurantes, catálogo de itens, cálculo de frete) durante um horário de pico como sexta-feira à noite. Os servidores e filas de mensagens ficam saturados, o que derruba o sistema para todos os usuários legítimos — clientes, entregadores e restaurantes — durante o período de maior faturamento.

### Fluxo de Abuso (Passo a Passo)

```
1. Atacante agenda ataque para horário de pico (ex.: 19h de sexta-feira).
2. Botnet envia ~50.000 requisições/segundo aos endpoints /search e /catalog.
3. Balanceadores de carga e servidores atingem limite de capacidade.
4. Filas de mensagens (RabbitMQ/Kafka) acumulam backlog inprocessável.
5. Novos pedidos não são aceitos; pedidos em andamento ficam sem status.
6. Plataforma fica indisponível por minutos a horas.
```

### Impacto

- Indisponibilidade total do aplicativo no horário de maior faturamento.
- Perda direta e mensurável de receita.
- Quebra de SLA com restaurantes parceiros.
- Dano à reputação perante usuários e parceiros.

### Contramedidas Recomendadas

- **Rate limiting** por IP e por usuário autenticado em todos os endpoints públicos.
- Web Application Firewall (WAF) com regras de detecção de tráfego anômalo.
- Proteção anti-DDoS no nível de infraestrutura (ex.: Cloudflare, AWS Shield).
- Auto-scaling configurado para absorver picos de demanda legítimos e inesperados.
- Filas de mensagens com circuit breaker para evitar propagação de falhas em cascata.
- Monitoramento em tempo real com alertas automáticos para picos anômalos de tráfego.

---

## CA-06 — Escalonamento de Privilégio via Broken Access Control *(Elevation of Privilege)*

| Campo                  | Detalhe |
|------------------------|---------|
| **ID**                 | CA-06 |
| **Categoria STRIDE**   | Elevation of Privilege |
| **Ativo Afetado**      | Painel Admin Web, Gestão de Identidade e Acesso (IAM) |
| **Ator Malicioso**     | Operador de restaurante mal-intencionado (usuário interno com acesso limitado) |
| **Pré-condição**       | Existência de falha de Broken Access Control: endpoints administrativos são protegidos apenas por verificação de autenticação (se o usuário está logado), mas não por verificação de autorização (se o usuário tem o papel/role de administrador) |

### Descrição do Abuso

Um operador de restaurante parceiro, autenticado com seu perfil legítimo no portal web, descobre — por inspeção do tráfego ou análise do código-fonte do front-end — endpoints de API restritos ao painel administrativo. Ao chamar diretamente `PATCH /api/admin/commissions/{restaurant_id}` com seu token de sessão, o atacante consegue alterar a própria taxa de comissão de 15% para 0%, pois o backend valida apenas a autenticação, não o papel (role) do usuário.

### Fluxo de Abuso (Passo a Passo)

```
1. Operador de restaurante autentica-se normalmente no portal parceiro.
2. Operador inspeciona chamadas de rede no DevTools ou com proxy HTTP.
3. Operador identifica endpoint: PATCH /api/admin/commissions/998.
4. Operador replica a requisição com seu próprio token JWT.
5. Backend valida que o token é válido (autenticado), mas não verifica o role (administrador).
6. Alteração é aceita: comissão do restaurante 998 é zerada.
7. Operador pode expandir o ataque: alterar comissões de outros restaurantes, aprovar cadastros pendentes, acessar dados financeiros globais.
```

### Impacto

- Comprometimento sistêmico das regras de negócio da plataforma.
- Fraudes financeiras em larga escala (perda de receita de comissões).
- Possível acesso a dados sensíveis de toda a base de parceiros e clientes.
- Risco de manipulação de aprovações, estornos e disputas administrativas.

### Contramedidas Recomendadas

- **Autorização baseada em papéis (RBAC)**: todo endpoint deve verificar explicitamente o papel do usuário autenticado, não apenas sua identidade.
- Princípio do menor privilégio: usuários de restaurantes nunca devem ter acesso — nem mesmo de leitura — a endpoints `/admin/`.
- Separação de tokens: tokens de parceiros e tokens de administradores devem ser distintos, com escopos e audiences diferentes no JWT.
- Testes de segurança automatizados (SAST/DAST) cobrindo cenários de escalonamento de privilégio.
- Auditoria de todos os acessos a endpoints administrativos com alertas para requisições de tokens fora do escopo esperado.

---

## Resumo dos Casos de Abuso

| ID    | Caso de Abuso                                      | STRIDE                  | Ativo Principal                      | Criticidade |
|-------|----------------------------------------------------|-------------------------|--------------------------------------|-------------|
| CA-01 | Sequestro de sessão de entregador                  | Spoofing                | Tokens JWT/OAuth2                    | Alta        |
| CA-02 | Manipulação do valor de pedido na requisição        | Tampering               | API de Checkout / Gateway            | Alta        |
| CA-03 | Golpe do estorno por falsa não-entrega             | Repudiation             | Logs de Auditoria / App Entregador   | Média       |
| CA-04 | Extração em massa de dados pessoais por IDOR       | Information Disclosure  | Banco de Dados PII / GPS             | Crítica     |
| CA-05 | DDoS por botnet em horário de pico                 | Denial of Service       | Infraestrutura Backend / Filas       | Alta        |
| CA-06 | Escalonamento de privilégio via Broken Access Control | Elevation of Privilege | Painel Admin / IAM                   | Crítica     |

---

## Relação com o Restante do Documento

| Seção do Documento | Conexão com os Casos de Abuso |
|--------------------|-------------------------------|
| **8.1 – Identificação do Sistema** | Os casos de abuso refletem os múltiplos perfis de acesso (clientes, entregadores, restaurantes, admins) e a superfície ampla de ataque descrita na justificativa. |
| **8.2 – Descrição do Sistema** | Cada CA ataca uma funcionalidade central: autenticação (CA-01), checkout (CA-02), logística/OTP (CA-03), dados pessoais/GPS (CA-04), infraestrutura (CA-05), IAM (CA-06). |
| **8.3 – Usuários, Ativos e Pontos de Interação** | Todos os ativos críticos listados (DB PII, APIs de pagamento, GPS, infraestrutura, sessões) possuem ao menos um caso de abuso correspondente. |
| **8.5 – Modelagem STRIDE** | Os casos de abuso expandem os cenários da tabela STRIDE com fluxos detalhados, pré-condições e contramedidas acionáveis. |

# Etapa 6 — Monitoramento e Detecção de Intrusões

## 6.1 Fundamentação Teórica

### O que é detecção de intrusões

A detecção de intrusões é o processo de monitorar continuamente os eventos que ocorrem em um sistema computacional ou rede, analisando-os em busca de sinais de possíveis incidentes, violações de políticas de segurança ou atividades maliciosas. Funciona como um "alarme" de segurança, identificando quando as defesas primárias falharam ou estão sob ataque.

No contexto do aplicativo de delivery, isso significa monitorar as interações entre usuários, APIs e banco de dados para identificar padrões que fujam do comportamento esperado — como um entregador autenticando em dois dispositivos simultaneamente, um usuário iterando sobre centenas de IDs de perfis em segundos, ou um volume anormal de requisições em endpoints públicos durante horários de pico.

### A diferença entre prevenir e detectar

Prevenção e detecção são camadas complementares de segurança, não excludentes:

**Prevenir** consiste em criar barreiras para impedir que o ataque ocorra — exigir MFA no login, bloquear conexões via WAF, recalcular valores no servidor. O foco é não deixar o invasor entrar.

**Detectar** consiste em assumir que, eventualmente, uma prevenção falhará ou que um usuário legítimo se comportará de forma maliciosa. O foco é identificar o comportamento anômalo *enquanto* ou *logo após* ele acontecer, permitindo uma resposta rápida antes que o dano escale.

Essa distinção é especialmente importante no delivery porque vários vetores de ataque identificados utilizam credenciais legítimas — CA-01 (sequestro de sessão de entregador) e CA-06 (Broken Access Control com token de parceiro). Nesses casos, a prevenção sozinha é insuficiente: o sistema precisa detectar o comportamento anômalo mesmo quando a autenticação foi bem-sucedida.

### Eventos que o sistema de delivery deve registrar

Para viabilizar uma detecção eficiente sem sobrecarregar o armazenamento, o sistema não precisa registrar cada clique, mas deve auditar obrigatoriamente os eventos críticos listados abaixo:

| Categoria | Eventos a registrar |
| :--- | :--- |
| **Autenticação e Sessão** | Logins bem-sucedidos e falhos com IP e `device_id`; login em dispositivo diferente do habitual; emissão e revogação de tokens JWT; redefinição de senha |
| **Autorização e Controle de Acesso** | Tentativas negadas (HTTP 403) de acesso a rotas `/admin/*` por perfis não administrativos; iteração sobre URLs de perfis alheios (IDOR); alteração de `role` em requisições |
| **Transacionais e de Negócio** | Divergências entre valor enviado pelo cliente e valor calculado no servidor; aplicação de cupons; solicitações de estorno (chargeback); alterações em comissões e repasses |
| **Logísticos** | Confirmação de OTP na entrega; recusas de pedido; timestamps de geolocalização ao marcar "entregue"; cancelamentos em sequência pelo mesmo usuário |
| **Infraestrutura** | Volume de requisições por IP acima do threshold de rate limiting; ativação de auto-scaling; erros HTTP 5xx em volume anormal; backlog acima do limite nas filas de mensagens |

---

## 6.2 Regras de Detecção

As regras a seguir foram projetadas para acionar o sistema de alerta do delivery caso as ameaças mapeadas na Etapa 1 e priorizadas na Etapa 2 tentem contornar as prevenções implementadas. Cada regra referencia diretamente o risco correspondente para manter a rastreabilidade com o registro de riscos da seção 2.4.

| ID | Risco observado | Fonte de dados | Condição de alerta | Resposta inicial |
| :---: | :--- | :--- | :--- | :--- |
| **RD-01** | **R01** — Sequestro de Sessão / Força Bruta (Spoofing / CA-01) | Logs de autenticação do serviço de IAM (campos: `user_id`, `device_id`, `ip_address`, `timestamp`, `success`) | Mais de 5 tentativas de login malsucedidas para a mesma conta de entregador em menos de 60 segundos; **ou** login bem-sucedido a partir de um `device_id` ou IP geograficamente incompatível com o último acesso registrado nos últimos 30 dias | Invalidar imediatamente todas as sessões ativas do usuário; bloquear a conta temporariamente; notificar o entregador por push notification e SMS; exigir nova autenticação com MFA e redefinição de senha; registrar o evento como incidente para análise da equipe de SecOps |
| **RD-02** | **R04** — Extração em Massa de Dados / IDOR (Information Disclosure / CA-04) | Logs de acesso da API no Gateway (campos: `user_id`, `ip`, `endpoint`, `resource_id`, `http_status`, `timestamp`) | Um mesmo `user_id` ou IP realiza mais de 10 requisições com `resource_id` distintos nos endpoints `/api/profile/*` ou `/api/orders/*` em uma janela de 60 segundos, independentemente do código de resposta retornado | Acionar rate limiting estrito para o `user_id` e IP; bloquear o IP no WAF por 24 horas; suspender a sessão do usuário investigado até análise manual; gerar alerta de prioridade alta com histórico completo de requisições do intervalo para avaliação de possível violação de dados sob a LGPD |
| **RD-03** | **R02** — Fraude Financeira / Tampering (Tampering / CA-02) | Logs transacionais e de pagamento (campos: `user_id`, `order_id`, `client_amount`, `server_amount`, `http_status`, `timestamp`) | O mesmo `user_id` ou carrinho gera 3 ou mais rejeições de checkout (HTTP 400) por divergência entre o valor enviado pelo cliente (`client_amount`) e o valor recalculado no servidor (`server_amount`) em uma janela de 10 minutos | Cancelar a transação instantaneamente; registrar o payload completo da requisição como evidência auditável; sinalizar o perfil do cliente com flag de risco alto na base de dados; encaminhar para monitoramento antifraude ativo e análise manual antes de permitir novas transações |

### Considerações Finais — Etapa 6

A Etapa 6 completou o ciclo de segurança do sistema de delivery adicionando a camada de visibilidade operacional — sem a qual os controles preventivos das etapas anteriores operariam de forma cega, sem capacidade de identificar quando estão sendo contornados ou quando falham.

As três regras de detecção definidas (RD-01, RD-02 e RD-03) foram construídas diretamente sobre os riscos de maior criticidade do registro — R01 (Sequestro de Sessão), R04 (Extração por IDOR) e R02 (Manipulação de Valor) — mantendo rastreabilidade completa com a análise da Etapa 2. A escolha dessas três regras não foi arbitrária: são exatamente os riscos cujos vetores de ataque utilizam comportamentos que os controles preventivos sozinhos não conseguem eliminar completamente. Um entregador pode ter seu dispositivo comprometido mesmo com MFA ativo; um atacante pode explorar um endpoint não coberto pelo RBAC; uma variante de manipulação de valor pode não ser capturada pelo recálculo se houver uma edge case não testada. As regras de detecção garantem que esses eventos não passem despercebidos.

Um aspecto importante desta etapa foi a definição de janelas de tempo e thresholds numéricos concretos nas condições de alerta — 5 tentativas em 60 segundos para força bruta, 10 requisições a IDs distintos em 60 segundos para IDOR, 3 rejeições em 10 minutos para tampering financeiro. Thresholds vagos como "muitas tentativas" ou "volume anormal" são inúteis na prática porque não podem ser configurados em sistemas de monitoramento reais. A especificidade é o que transforma uma regra conceitual em um alerta funcional.

A principal limitação desta etapa é que as regras foram definidas conceitualmente sem calibração com dados reais de tráfego da plataforma. Em produção, thresholds muito baixos gerariam falsos positivos bloqueando usuários legítimos; thresholds muito altos deixariam ataques reais passarem despercebidos. A calibração correta exige observação do comportamento normal do sistema por um período mínimo antes de ativar os alertas em modo de bloqueio automático — iniciando em modo de observação passiva e evoluindo gradualmente para resposta ativa conforme a confiança nos thresholds aumenta.

---


# Documento Principal de Modelagem de Ameaças e Análise de Riscos — ESS

> **Disciplina:** Engenharia de Software Seguro — Codefólio  
> **Sistema Analisado:** App de Delivery de Comida *(Plataforma Integrada de Pedidos e Entregas Online)*

---

## 8.1 Identificação do Sistema

* **Nome do Sistema:** App de Delivery de Comida *(Plataforma Integrada de Pedidos e Entregas Online)*
* **Endereço do Repositório:** [https://github.com/gabrieldm-arch/Grupo-2-ES-Seguro](https://github.com/gabrieldm-arch/Grupo-2-ES-Seguro)
* **Integrantes do Grupo:**
  * **Gabriel Martinez**
  * **Kaique Schio**
  * **Pedro Ayres**

### Justificativa para a Escolha do Sistema
O ecossistema de um aplicativo de entrega de comida foi selecionado por ser um ambiente computacional amplamente distribuído e crucial do ponto de vista da segurança da informação. Os principais motivos que nos levam a escolher são:
1. **Múltiplos perfis e níveis de privilégio:** A plataforma conecta ao mesmo tempo Clientes, que são os consumidores finais, Restaurantes/Estabelecimentos, Entregadores e Administradores, o que demanda um controle estrito de autenticação e divisão de privilégios.
2. **Ativos críticos e dados sensíveis:** Armazenamento e circulação de dados pessoais, como CPF, endereço residencial, números de telefone, dados bancários/cartões de crédito, histórico de pedidos e rastreamento de geolocalização em tempo real, em conformidade com a LGPD.
3. **Operações financeiras e vulnerabilidade à fraude:** Transações constantes por meio de PIX, cartões e carteiras digitais, além de procedimentos de estorno, cupons de desconto e transferências de pagamento, que costumam ser alvos de fraudes por agentes mal-intencionados.
4. **Superfície de ataque ampliada:** Integração abrangente com APIs externas, gateways de pagamento, serviços de geolocalização, como o maps, e sistemas de mensagem/notificação, possibilitando a aplicação de todas as categorias de ameaças da metodologia **STRIDE**.

---

## 8.2 Descrição do Sistema

O **App de Delivery de Comida** é uma plataforma distribuída constituída por aplicativos móveis (Android/iOS), portal web para estabelecimentos e painel administrativo, interligados via serviços de API backend.

### 1. Qual problema o sistema resolve
O sistema resolve o problema de intermediação eficiente e em tempo real entre o **setor de alimentação**, **consumidores** e **entregadores independentes**. Ele consolida em uma única plataforma:
* A digitalização de cardápios e recebimento automatizado de pedidos para os restaurantes.
* A facilidade de descoberta, pagamento digital e acompanhamento logístico para os clientes.
* A distribuição otimizada de rotas de entrega e repasses financeiros para os entregadores parceiros.

### 2. Quem utiliza o sistema (Atores e Perfis de Acesso)
* **Clientes (Consumidores):** Usuários que buscam restaurantes, realizam pedidos, efetuam pagamentos digitais, utilizam cupons promocionais e acompanham a geolocalização do pedido até a entrega.
* **Restaurantes / Estabelecimentos Parceiros:** Operadores que utilizam o portal parceiro para cadastrar itens, definir preços, gerenciar estoque, aceitar/recusar pedidos e visualizar relatórios de repasses financeiros.
* **Entregadores (Parceiros Logísticos):** Usuários móveis que recebem chamadas de corrida, visualizam endereços de coleta e entrega, confirmam retiradas com códigos de segurança e comunicam-se via chat restrito com clientes e restaurantes.
* **Administradores da Plataforma:** Equipe técnica e operacional com poderes elevados para gestão de cadastros, aprovação de estabelecimentos/entregadores, moderação de disputas (estornos, denúncias), parametrização de comissões e auditoria do sistema.

### 3. Quais são as principais funcionalidades
* **Gestão de Identidade e Acesso (IAM):** Cadastro e autenticação de usuários, autenticação multifator (MFA/TOTP) para operações sensíveis, recuperação de credenciais e gestão de perfis em conformidade com a LGPD.
* **Catálogo Georreferenciado e Pedidos:** Busca de estabelecimentos próximos com base nas coordenadas GPS, personalização do pedido, cálculo automático de frete e gestão do carrinho de compras.
* **Gateway e Processamento de Pagamentos:** Cobrança via cartões de crédito/débito, PIX e saldo em carteira digital, com aplicação de regras de antifraude, validação de cupons promocionais e processamento do repasse aos parceiros.
* **Logística e Rastreamento em Tempo Real:** Roteamento e despacho de entregadores, acompanhamento GPS ao vivo da coleta à entrega e validação de conclusão de entrega via código OTP.
* **Mensageria e Notificações:** Sistema de chat integrado entre Cliente-Entregador e Cliente-Restaurante (com mascaramento de telefone para proteção da privacidade) e envio de notificações push/SMS sobre o status do pedido.

### 4. Quais informações são armazenadas ou transmitidas
* **Dados Pessoais Sensíveis e Cadastrais (LGPD):** Nome completo, CPF, e-mail, telefone, endereço residencial/entrega e data de nascimento.
* **Dados Financeiros e de Faturamento:** Tokens vinculados a cartões bancários (via gateway PCI-DSS), chaves PIX, histórico de pedidos, cupons aplicados, extratos de repasse e notas fiscais.
* **Dados Geolocalizados:** Histórico de rotas e coordenadas GPS precisas e contínuas de entregadores em serviço e endereços de destino de clientes.
* **Dados Operacionais e de Auditoria:** Logs de requisições às APIs, registros de chat entre usuários, avaliações/reviews de lojas e entregadores e históricos de cancelamento/estorno.

### 5. Quais recursos precisam ser protegidos
Para subsidiar a modelagem de ameaças e mitigação de abusos, destacam-se os principais ativos de segurança da plataforma:
* **Banco de Dados Central (PII e Pedidos):** Base que armazena todas as informações pessoais dos clientes, parceiros e histórico transacional; alvo principal para ataques de vazamento de informações (*Information Disclosure*).
* **APIs de Checkout e Gateway de Pagamento:** Endpoints de cobrança, aplicação de cupons e repasse financeiro que devem ser imunes a manipulação de preços ou autorizações indevidas (*Tampering / Elevation of Privilege*).
* **Sessões e Tokens de Autenticação (JWT/OAuth2):** Chaves de acesso e tokens de sessão que garantem a autenticação e autorização de cada usuário sem permitir sequestro de contas (*Spoofing*).
* **Serviço de Comunicação e Roteamento GPS:** Mecanismos que garantem a disponibilidade logística e impedem rastreamento indevido ou interceptação de conversas privadas entre clientes e parceiros.
* **Servidores e Infraestrutura de Backend:** Ambiente de execução de microserviços, filas de mensagens e balanceadores de carga, que precisam estar protegidos contra ataques de negação de serviço (*Denial of Service - DoS*).

---

## 8.3 Usuários, ativos e pontos de interação

O sistema de Delivery interliga dezenas de componentes. Abaixo estão mapeados os principais elementos e recursos do ecossistema, segmentados por categoria:

### Usuários e Perfis de Acesso
- **Cliente:** O consumidor final, com acesso via App Mobile e Web.
- **Parceiro (Restaurante):** O operador do estabelecimento, com acesso via Portal Web do Parceiro.
- **Entregador:** O parceiro logístico motorizado/ciclista, com acesso via App Mobile do Entregador.
- **Administrador:** O integrante do suporte/gestão da plataforma, com acesso via Painel Admin Web.

### Credenciais e Autenticação
- Senhas com hash criptográfico, tokens temporários (OTP/PIN via SMS e E-mail).
- Tokens de sessão (JWT) e tokens OAuth2 para logins sociais (Google/Apple).

### Pagamentos e Financeiro
- Dados bancários, cartões de crédito (acessíveis à plataforma apenas de forma tokenizada pelo Gateway parceiro).
- Chaves PIX, histórico de compras, carteiras digitais (cashback/saldo) e registros de repasses/comissões.

### Localização, Mensagens e Avaliações
- **GPS:** Histórico e coordenadas em tempo real (posição do entregador e endereço exato de residência do cliente).
- **Chat:** Sistema de mensageria interna para dúvidas sobre o pedido e contato direto (com mascaramento de números).
- **Reviews:** Avaliações de qualidade, fotos de recebimentos e comentários sobre a conduta de entregadores/lojas.

### Arquitetura: Servidores, Bancos de Dados e Aplicações
- **Aplicações (Front-end):** Aplicativos nativos iOS/Android (Clientes e Entregadores) e SPAs Web (Painéis de Restaurantes/Admin).
- **Servidores (Back-end):** Servidores Cloud em provedor de nuvem, APIs de Backend (microsserviços REST/GraphQL), balanceadores de carga e filas de mensagens para processamento assíncrono (RabbitMQ/Kafka).
- **Banco de Dados:** Bancos relacionais (ex.: PostgreSQL para transações, pedidos e controle de saldos) e não-relacionais (ex.: MongoDB para logs, histórico de chat e avaliações).

### Serviços Externos e APIs
- **APIs de Pagamento:** Conexões externas para processamento de cobranças e estornos (ex.: Stripe, MercadoPago, Pagar.me).
- **APIs de Mapeamento:** Conexões para cálculo de rota e distância (ex.: Google Maps, Mapbox).
- **APIs de Comunicação:** Serviços de envio de e-mails, SMS e Push Notifications (ex.: Twilio, Firebase, SendGrid).

### Ativos Críticos Destacados
Os recursos que podem causar os maiores prejuízos, como financeiros, regulatórios, legais ou de reputação, caso sejam acessados, alterados, destruídos ou indisponibilizados indevidamente são:

1. **Bancos de Dados de Pagamentos e PII (Informações Pessoalmente Identificáveis):**
   * Contém CPFs, endereços, perfis comportamentais e saldos. Uma falha de segurança levaria a multas milionárias da LGPD e destruição da confiança da base de clientes.
2. **APIs e Gateway de Pagamentos:**
   * Se um atacante forjar requisições ou se passar por um restaurante, pode drenar fundos, aprovar pedidos sem pagar ou alterar as contas de repasse.
3. **Serviços de Roteamento (GPS) e Chat Privado:**
   * A interceptação em tempo real do GPS ou das conversas pode colocar em risco a segurança física dos usuários, como entregadores e clientes, em caso de perseguições, assaltos ou golpes no momento da entrega.
4. **Infraestrutura Cloud de Microsserviços e Filas de Mensagens:**
   * A indisponibilidade da nuvem ou interrupção no despacho de pedidos por algumas poucas horas, especialmente em horários de pico, como finais de semana, gera um prejuízo direto no faturamento.

## 8.5 Modelagem STRIDE

A tabela a seguir apresenta a análise de ameaças utilizando a metodologia STRIDE. Cada categoria foi mapeada com foco estrito nas operações, ativos críticos e perfis de acesso (clientes, restaurantes, entregadores e administradores) presentes no ecossistema da plataforma de delivery.

| Categoria STRIDE | Descrição da Ameaça | Ativo/Ponto de Interação Afetado | Cenário de Ataque (Casos de Abuso no Delivery) | Impacto Principal |
| :--- | :--- | :--- | :--- | :--- |
| **Spoofing** (Falsificação de Identidade) | Um ator malicioso assume a identidade de um usuário legítimo (cliente, entregador ou restaurante). | Sessões e Tokens de Autenticação (JWT/OAuth2). | Um atacante consegue roubar o token de sessão de um entregador e utiliza seu perfil no aplicativo para aceitar corridas com o único intuito de furtar as refeições coletadas nos restaurantes. | Roubo de mercadorias, risco à segurança física dos clientes e dano severo à reputação da plataforma. |
| **Tampering** (Violação / Modificação) | Alteração indevida de dados em trânsito ou informações armazenadas no sistema. | APIs de Checkout e Gateway de Pagamento. | Um cliente mal-intencionado intercepta a requisição HTTP de finalização do pedido e altera o parâmetro do valor final para R$ 0,00 antes de enviá-la para a API de cobrança. | Fraude financeira direta, perda de receita para a plataforma e falha no repasse aos restaurantes parceiros. |
| **Repudiation** (Repúdio) | Um usuário nega ter realizado uma ação (ex: compra, entrega) e o sistema não possui logs/provas suficientes para contestá-lo. | App do Entregador, Logs de Auditoria. | Um cliente recebe seu pedido corretamente, mas entra em contato com o suporte afirmando que o entregador nunca apareceu, exigindo o estorno do valor (golpe do estorno/chargeback). | Prejuízos financeiros para a plataforma ou restaurante, além de possível banimento injusto do parceiro logístico. |
| **Information Disclosure** (Divulgação de Informações) | Exposição ou vazamento de dados sensíveis e pessoais a agentes não autorizados. | Banco de Dados Central (PII e Pedidos), Serviços de Roteamento (GPS). | Uma vulnerabilidade no banco de dados central (IDOR) permite que um atacante extraia em massa CPFs, endereços residenciais e o histórico de coordenadas de entregas. | Multas milionárias por infração à LGPD, exposição física dos usuários e quebra total de confiança. |
| **Denial of Service** (Negação de Serviço) | Sobrecarga de recursos que torna o sistema indisponível para usuários legítimos. | Servidores e Infraestrutura de Backend, Filas de Mensagens. | Uma *botnet* inunda as APIs de catálogo de restaurantes e roteamento com milhares de requisições simultâneas durante um horário de pico (ex: sexta-feira à noite). | Indisponibilidade total do aplicativo, impedindo novos pedidos e gerando prejuízo massivo no faturamento diário. |
| **Elevation of Privilege** (Elevação de Privilégio) | Um usuário comum obtém permissões de acesso superiores às do seu perfil (ex: administrador). | Painel Admin Web, Gestão de Identidade (IAM). | Um perfil de restaurante explora uma falha de autorização (Broken Access Control) no portal web e consegue acessar endpoints exclusivos da equipe de Administração, alterando a própria taxa de comissão para 0%. | Comprometimento sistêmico, fraudes internas em larga escala e manipulação das regras de negócio do delivery. |

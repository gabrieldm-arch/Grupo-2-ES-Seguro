# Etapa 2 — Análise, Priorização e Tratamento de Riscos (NIST CSF 2.0)

## 2. Análise e priorização dos riscos

Nesta etapa, transformamos as ameaças mapeadas na Etapa 1 em eventos de risco concretos para o aplicativo de delivery, adotando as escalas de probabilidade e impacto sugeridas para quantificação.

### 2.1 Critérios de probabilidade

A probabilidade avalia a chance de a ameaça ser explorada com sucesso, considerando as características do nosso sistema, o perfil dos atacantes e as vulnerabilidades do delivery. Utilizamos a seguinte escala:

| Valor | Classificação | Critério |
| :---: | :--- | :--- |
| **1** | **Baixa** | O evento depende de condições incomuns, acesso muito específico ou grande capacidade técnica. |
| **2** | **Média-baixa** | O evento é possível, mas depende de uma vulnerabilidade ou condição específica. |
| **3** | **Média-alta** | O evento é plausível e pode ocorrer em situações comuns de uso ou ataque. |
| **4** | **Alta** | O evento pode ocorrer com facilidade, frequência ou durante condições previsíveis do sistema. |

### 2.2 Critérios de impacto

O impacto avalia os prejuízos e consequências que o evento de risco trará ao aplicativo, aos usuários (clientes, parceiros, entregadores) e ao modelo de negócios. Consideramos perdas financeiras, exposição de PII (LGPD), danos à reputação e interrupção do serviço. Utilizamos a seguinte escala:

| Valor | Classificação | Critério |
| :---: | :--- | :--- |
| **1** | **Baixo** | Causa pequeno transtorno e pode ser corrigido rapidamente. |
| **2** | **Moderado** | Causa interrupção ou inconsistência limitada, com possibilidade de recuperação. |
| **3** | **Alto** | Causa prejuízo relevante aos usuários, ao negócio, à administração ou à privacidade. |
| **4** | **Muito alto** | Pode afetar muitos usuários, comprometer operações críticas ou causar prejuízo grave. |

### 2.3 Cálculo e classificação

A pontuação de cada risco será calculada multiplicando a probabilidade pelo impacto (`Pontuação = Probabilidade × Impacto`). O resultado define a prioridade de atenção que devemos dar ao evento:

| Pontuação | Nível do risco |
| :---: | :--- |
| **1 a 3** | **Baixo** |
| **4 a 7** | **Médio** |
| **8 a 11** | **Alto** |
| **12 a 16** | **Crítico** |

### 2.4 Registro de riscos

A partir das ameaças e casos de abuso levantados na Etapa 1, os eventos foram transformados na seguinte matriz de riscos (R01 a R06).

| ID | Origem STRIDE | Evento de risco | Vulnerabilidade ou condição | Probabilidade | Impacto | Pontuação | Nível |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **R01** | Spoofing (CA-01) | Sequestro de Sessão do Entregador, resultando em roubo de pedidos | Token JWT interceptável via rede insegura e ausência de verificação adicional de dispositivo | 3 | 4 | **12** | **Crítico** |
| **R02** | Tampering (CA-02) | Manipulação do Valor do Pedido para forjar compras gratuitas | Aceitação de valores calculados no front-end sem recálculo/validação rígida no servidor | 3 | 3 | **9** | **Alto** |
| **R03** | Repudiation (CA-03) | Golpe do Estorno (falsa alegação de não entrega) | Falta de evidências irrefutáveis de recebimento (ex: OTP, GPS log e assinatura fotográfica) | 4 | 2 | **8** | **Alto** |
| **R04** | Info. Disclosure (CA-04) | Extração em Massa de Dados (IDOR) e vazamento de PII da base inteira | Uso de IDs sequenciais nas APIs sem validação forte de autorização sobre os objetos | 3 | 4 | **12** | **Crítico** |
| **R05** | DoS (CA-05) | DDoS por Botnet derrubando a plataforma em horário de pico (ex: sexta à noite) | Endpoints de catálogo e busca abertos sem *Rate Limiting* ou proteção de Web Application Firewall | 3 | 4 | **12** | **Crítico** |
| **R06** | Elevation of Privilege (CA-06)| Broken Access Control permitindo a parceiros acessar endpoints de Admin e zerar comissões | Endpoints verificam apenas autenticação (estar logado) e não o papel (role-based access control) | 2 | 4 | **8** | **Alto** |
## 2.5 Justificativa das Avaliações

Esta seção explica os valores de probabilidade e impacto atribuídos a cada risco na seção 2.4, detalhando os critérios considerados para cada avaliação com base nas características do sistema, no perfil dos atacantes e nas condições de exploração identificadas.

---

### R01 — Sequestro de Sessão do Entregador (Spoofing / CA-01)

**Probabilidade: 3 — Média-alta**
O ataque depende de o adversário obter o token JWT do entregador, o que pode ser feito por phishing direcionado, sniffing em redes Wi-Fi abertas ou malware em dispositivos móveis. Essas três técnicas são amplamente disponíveis, não exigem conhecimento técnico avançado e são rotineiramente utilizadas contra trabalhadores de plataformas digitais. O fato de entregadores frequentemente utilizarem redes públicas durante o expediente — em restaurantes, postos de gasolina e áreas de espera — aumenta consideravelmente a exposição ao sniffing. A probabilidade não foi classificada como 4 (Alta) porque o ataque ainda exige uma etapa prévia de comprometimento do dispositivo ou da rede, representando uma barreira mínima mas existente.

**Impacto: 4 — Muito alto**
O comprometimento da sessão de um entregador ativo afeta simultaneamente múltiplas partes do ecossistema: o cliente que não recebe o pedido e sofre prejuízo financeiro; o restaurante que prepara o pedido sem receber a confirmação de entrega e arca com reclamação indevida; o entregador legítimo que é penalizado automaticamente no sistema de reputação; e a plataforma que absorve o prejuízo financeiro e o dano reputacional. Há ainda um componente de risco físico direto — clientes que aguardam entregas em locais isolados ou residências ficam expostos a situações de vulnerabilidade. O impacto foi classificado como Muito alto por comprometer simultaneamente múltiplos usuários, múltiplos componentes financeiros e a segurança física dos envolvidos.

**Nível: Crítico (3 × 4 = 12)**
O nível Crítico é adequado dado que o vetor humano (phishing) é de difícil eliminação completa, as consequências são imediatas, multidimensionais e afetam toda a cadeia operacional da entrega.

---

### R02 — Manipulação do Valor do Pedido (Tampering / CA-02)

**Probabilidade: 3 — Média-alta**
A técnica de interceptação de requisições HTTP com ferramentas como Burp Suite é amplamente documentada e acessível a qualquer usuário com conhecimento técnico básico. Tutoriais específicos sobre manipulação de parâmetros em APIs de e-commerce e delivery são facilmente encontrados em fóruns públicos. A condição habilitadora — ausência de recálculo server-side, confiando nos valores enviados pelo cliente — é um erro de design recorrente em sistemas que não separam adequadamente a camada de apresentação da camada de negócio. A probabilidade não foi classificada como 4 porque o atacante precisa configurar um proxy HTTP e ter familiaridade mínima com a estrutura de requisições da API, representando uma barreira de entrada moderada.

**Impacto: 3 — Alto**
A manipulação do valor do pedido causa prejuízo financeiro direto para a plataforma e para o restaurante parceiro, que prepara e entrega o pedido sem receber o valor correspondente. Os componentes afetados são: a API de checkout, o gateway de pagamento e o fluxo de repasse ao restaurante. O impacto afeta o modelo de negócio de forma recorrente se explorado sistematicamente por múltiplos atacantes. Não foi classificado como Muito alto (4) porque o prejuízo, embora relevante, é limitado ao valor individual de cada pedido fraudado — não expõe dados pessoais de outros usuários nem compromete a disponibilidade do serviço para a base geral de clientes.

**Nível: Alto (3 × 3 = 9)**
O nível Alto é adequado: o ataque é tecnicamente acessível, o impacto financeiro é direto e recorrente, mas o dano por ocorrência é delimitado ao valor unitário do pedido, diferentemente de ataques que comprometem toda a base de usuários ou a disponibilidade da plataforma.

---

### R03 — Golpe do Estorno por Falsa Não-Entrega (Repudiation / CA-03)

**Probabilidade: 4 — Alta**
Este é o risco de maior probabilidade do registro porque não exige nenhum conhecimento técnico: qualquer cliente desonesto pode alegar não ter recebido um pedido e acionar o suporte solicitando estorno. A condição habilitadora — ausência de evidências irrefutáveis de entrega como OTP, registro de geolocalização com timestamp e fotografia — é uma lacuna operacional que persiste em muitas plataformas de delivery. O comportamento pode ser repetido sistematicamente pelo mesmo usuário em pedidos distintos até ser detectado por análise comportamental, processo que frequentemente demora semanas. A probabilidade foi classificada como 4 (Alta) por ser um comportamento de baixíssima barreira de execução, sem necessidade de nenhuma capacidade técnica, e de alta frequência documentada em plataformas similares.

**Impacto: 2 — Moderado**
Cada ocorrência individual causa prejuízo financeiro limitado ao valor do pedido e eventual penalização indevida do entregador no sistema de reputação. Os componentes afetados são: o sistema de disputas e estornos, o histórico do entregador e o repasse financeiro ao restaurante. O impacto não alcança o nível Alto porque o dano por ocorrência é contido e reversível — a plataforma pode identificar padrões de abuso e banir contas reincidentes. Não compromete dados pessoais de terceiros nem a disponibilidade do serviço para outros usuários. O impacto agregado pode ser relevante se praticado em escala, mas individualmente é classificado como Moderado.

**Nível: Alto (4 × 2 = 8)**
Apesar do impacto unitário moderado, a altíssima probabilidade eleva o nível para Alto. O risco merece atenção prioritária pela frequência com que ocorre em plataformas de delivery e pelo impacto acumulado sobre entregadores e restaurantes parceiros ao longo do tempo.

---

### R04 — Extração em Massa de Dados Pessoais por IDOR (Information Disclosure / CA-04)

**Probabilidade: 3 — Média-alta**
Vulnerabilidades IDOR em APIs REST são extremamente comuns e figuram consistentemente no OWASP Top 10 sob a categoria Broken Access Control. A técnica de enumeração de IDs sequenciais é simples e completamente automatizável com scripts básicos em Python ou ferramentas como Burp Suite Intruder. A condição habilitadora — uso de identificadores sequenciais e previsíveis nos endpoints de perfil sem validação de autorização por objeto — é um erro de design frequente em sistemas que cresceram rapidamente sem revisão de segurança. A probabilidade não foi classificada como 4 porque a exploração em massa requer que o atacante primeiro identifique a vulnerabilidade e desenvolva ou adapte um script de automação, o que representa uma barreira técnica mínima mas existente.

**Impacto: 4 — Muito alto**
O vazamento em massa de CPFs, endereços residenciais, histórico de geolocalização de entregas e dados financeiros de potencialmente milhões de usuários é o cenário de maior impacto regulatório e social do sistema. Os componentes afetados incluem: o banco de dados central de PII, os endpoints de perfil da API, o serviço de rastreamento GPS e os dados financeiros dos parceiros. As consequências abrangem: sanções administrativas da ANPD com multas de até 2% do faturamento anual (LGPD, art. 52); ações judiciais coletivas movidas por titulares afetados; risco físico direto aos usuários cujos endereços residenciais foram expostos; e destruição irreversível da confiança na plataforma. O impacto foi classificado como Muito alto por comprometer potencialmente toda a base de usuários em múltiplas dimensões — financeira, regulatória, reputacional e de segurança física.

**Nível: Crítico (3 × 4 = 12)**
O nível Crítico é plenamente justificado: a vulnerabilidade é tecnicamente acessível, completamente automatizável e resulta no pior cenário possível do ponto de vista regulatório, de privacidade e de segurança física dos usuários.

---

### R05 — DDoS por Botnet em Horário de Pico (Denial of Service / CA-05)

**Probabilidade: 3 — Média-alta**
Serviços de DDoS por aluguel (DDoS-as-a-Service) estão disponíveis na internet a preços acessíveis, tornando esse tipo de ataque viável para adversários sem infraestrutura própria. A condição habilitadora — ausência de rate limiting eficaz e WAF nos endpoints públicos de busca e catálogo — é uma lacuna de infraestrutura comum em plataformas em estágio inicial de maturidade de segurança. Plataformas de delivery são alvos particularmente atrativos por operarem com receita concentrada em janelas de tempo previsíveis (horários de almoço e jantar, sextas-feiras à noite, fins de semana e datas comemorativas), o que permite ao atacante maximizar o impacto com precisão temporal. A probabilidade não foi classificada como 4 porque ataques DDoS direcionados a plataformas específicas ainda requerem motivação deliberada e investimento mínimo, sendo menos oportunistas do que os demais vetores analisados.

**Impacto: 4 — Muito alto**
A indisponibilidade da plataforma durante horários de pico causa prejuízo financeiro direto e imediato para todos os participantes do ecossistema: a plataforma perde receita de comissões; os restaurantes deixam de receber pedidos durante seu período de maior faturamento; os entregadores perdem corridas e renda; e os clientes migram para plataformas concorrentes, gerando perda de mercado de difícil reversão. Os componentes afetados incluem: a infraestrutura de backend, as filas de mensagens (RabbitMQ/Kafka), os endpoints de busca e catálogo e o serviço de despacho de entregadores. O impacto foi classificado como Muito alto porque afeta simultaneamente toda a base de usuários, todos os parceiros e a receita operacional no seu momento de maior concentração.

**Nível: Crítico (3 × 4 = 12)**
O nível Crítico é adequado: o ataque é acessível financeiramente, previsível em termos de janela de oportunidade e resulta em indisponibilidade total do serviço no momento de maior valor operacional e financeiro da plataforma.

---

### R06 — Broken Access Control no Painel Administrativo (Elevation of Privilege / CA-06)

**Probabilidade: 2 — Média-baixa**
A exploração requer que um operador de restaurante com conta ativa inspecione as chamadas de rede do portal parceiro usando as ferramentas de desenvolvedor do navegador, identifique endpoints administrativos acessíveis e replique as requisições com seu próprio token JWT. Embora a técnica seja simples para alguém com conhecimento básico de HTTP e inspeção de rede, ela depende de motivação específica, de que o operador perceba a oportunidade e de que os endpoints administrativos não estejam minimamente ofuscados. A probabilidade foi classificada como 2 (Média-baixa) porque, apesar de tecnicamente acessível, o ataque requer que o agente seja um parceiro cadastrado e verificado na plataforma, com intenção deliberada de explorar a falha — o que representa um perfil de atacante mais específico e rastreável do que um usuário anônimo externo.

**Impacto: 4 — Muito alto**
O acesso indevido ao painel administrativo permite manipular comissões de todos os parceiros, acessar dados financeiros consolidados da plataforma, alterar configurações críticas de operação e potencialmente comprometer toda a lógica de negócio do sistema. Os componentes afetados incluem: o painel administrativo web, o sistema de gestão de comissões, os dados financeiros de todos os restaurantes parceiros e as configurações globais da plataforma. O impacto foi classificado como Muito alto porque as consequências têm natureza sistêmica — não se limitam ao atacante individual, mas comprometem a integridade de toda a operação da plataforma e os dados confidenciais de todos os parceiros cadastrados.

**Nível: Alto (2 × 4 = 8)**
Apesar do impacto máximo (4), a probabilidade relativamente menor (2) mantém o nível em Alto. O risco ainda merece atenção prioritária pela natureza sistêmica do dano potencial e pela dificuldade de detecção — a exploração é feita com credenciais legítimas —, mas a barreira de entrada maior em relação aos riscos Críticos justifica sua posição na ordem de prioridade.

---

## 2.6 Priorização dos Riscos

Com base nas pontuações calculadas, na gravidade das consequências, na quantidade de usuários e componentes afetados, nas dependências técnicas entre os riscos e na urgência do tratamento, define-se a seguinte ordem de prioridade:

| Prioridade | ID | Evento de risco | Nível | Pontuação | Justificativa da priorização |
| :---: | :---: | :--- | :---: | :---: | :--- |
| 1º | **R04** | Extração em Massa de Dados por IDOR | Crítico | 12 | Maior impacto regulatório (LGPD/ANPD) com consequências irreversíveis; afeta potencialmente toda a base de usuários; exige refatoração estrutural do modelo de dados (substituição de IDs por UUIDs) que impacta múltiplos serviços — deve ser resolvido primeiro por ser uma dependência arquitetônica de outros controles |
| 2º | **R06** | Broken Access Control no Painel Admin | Alto | 8 | Falha sistêmica que expõe toda a lógica de negócio e os dados financeiros de todos os parceiros; exploração com credenciais legítimas torna a detecção muito mais difícil; a implementação correta de RBAC é pré-requisito técnico para a segurança dos demais endpoints da plataforma |
| 3º | **R01** | Sequestro de Sessão do Entregador | Crítico | 12 | Pontuação igual à de R04 e R05, mas priorizado após R06 por depender de um modelo de autenticação e autorização robusto; o MFA e o JWT binding ao dispositivo apoiam-se na arquitetura de identidade que deve ser corrigida em R06 para garantir consistência |
| 4º | **R02** | Manipulação do Valor do Pedido | Alto | 9 | Prejuízo financeiro direto e recorrente com alto potencial de escala; a mitigação é tecnicamente simples (recálculo server-side com HMAC) e de alto retorno de segurança; não depende de mudanças estruturais, podendo ser implementado rapidamente após os controles de identidade |
| 5º | **R05** | DDoS por Botnet em Horário de Pico | Crítico | 12 | Pontuação Crítica, mas implementado integralmente na camada de infraestrutura (WAF, rate limiting, auto-scaling) de forma independente do desenvolvimento backend; pode e deve ser executado em paralelo aos itens anteriores sem criar dependência técnica |
| 6º | **R03** | Golpe do Estorno por Falsa Não-Entrega | Alto | 8 | Menor prioridade relativa por envolver exclusivamente regra de negócio no app mobile (fluxo de OTP e foto de entrega) sem dependência de mudanças arquitetônicas; impacto unitário moderado permite que seja tratado após o saneamento das vulnerabilidades estruturais |

### Justificativa geral da ordem

A priorização não seguiu exclusivamente a pontuação numérica — três riscos empataram com pontuação 12 (R01, R04 e R05) — mas considerou três fatores adicionais:

**Dependências técnicas:** R04 foi colocado em primeiro lugar porque a substituição de IDs sequenciais por UUIDs é uma mudança no modelo de dados que afeta múltiplos serviços simultaneamente e deve preceder qualquer outra refatoração de segurança. R06 foi colocado em segundo porque a implementação correta de RBAC é pré-requisito para a segurança dos endpoints que serão protegidos nos demais riscos — sem um modelo de autorização por papel funcionando corretamente, os controles dos outros riscos podem ser contornados.

**Natureza e reversibilidade do dano:** Riscos com consequências regulatórias irreversíveis (R04 — LGPD/ANPD) e sistêmicas (R06 — acesso administrativo completo) foram priorizados sobre riscos com impacto operacional importante mas recuperável (R05 — DDoS, cujos efeitos cessam com o fim do ataque e podem ser mitigados com auto-scaling; R03 — estorno, cujo impacto unitário é limitado e reversível).

**Paralelismo possível:** R05 foi posicionado em 5º lugar não por menor importância, mas porque sua implementação — na camada de infraestrutura com WAF e rate limiting — é completamente independente do desenvolvimento de backend e pode ser executada em paralelo às demais tarefas, sem atrasar o cronograma geral de mitigação.

---

## 2.7 Estratégias de Tratamento

Para cada risco, foi definida uma estratégia principal de tratamento com justificativa baseada na natureza da vulnerabilidade, na viabilidade de eliminação da condição de risco e no custo-benefício da implementação.

| ID | Estratégia | Justificativa |
| :---: | :---: | :--- |
| **R01** | **Reduzir** | Não é possível eliminar completamente o risco de phishing ou comprometimento de dispositivos móveis de entregadores — o vetor humano não pode ser suprimido por design de sistema. A estratégia é reduzir o impacto e a janela de exploração por meio de tokens JWT de curta duração (15 min), MFA/TOTP obrigatório no login e vinculação do token ao `device_id`, tornando o token roubado inutilizável sem o segundo fator de autenticação. |
| **R02** | **Reduzir** | A funcionalidade de checkout não pode ser eliminada — é o núcleo da operação da plataforma. O que se elimina é a vulnerabilidade específica no processamento da requisição. A estratégia é reduzir a probabilidade de exploração bem-sucedida implementando recálculo obrigatório do valor total no servidor com base nos preços do banco de dados e assinatura HMAC do payload do carrinho, tornando qualquer valor enviado pelo cliente irrelevante para o processamento do pagamento. |
| **R03** | **Reduzir** | Não é possível evitar que clientes desonestos tentem solicitar estornos indevidos — o comportamento humano malicioso não pode ser eliminado por controle técnico. A estratégia é reduzir drasticamente a probabilidade de sucesso do golpe por meio de evidências irrefutáveis de entrega: código OTP validado no ato, registro de geolocalização com timestamp imutável e foto obrigatória da entrega, tornando o estorno fraudulento contestável com provas concretas e auditáveis. |
| **R04** | **Evitar** | A condição habilitadora — uso de IDs sequenciais e previsíveis sem validação de autorização em nível de objeto — pode ser completamente eliminada substituindo identificadores numéricos por UUIDs não sequenciais e implementando verificação de autorização por objeto (RBAC/ABAC) em todos os endpoints da API. Como é possível eliminar a raiz arquitetônica do problema por design, a estratégia Evitar é a mais adequada e eficaz para este risco. |
| **R05** | **Reduzir + Compartilhar** | Não é possível evitar que ataques DDoS sejam tentados — o vetor é completamente externo e independe de decisões de design da plataforma. A estratégia primária é **Reduzir** o impacto por meio de rate limiting por IP/usuário, WAF com detecção de padrões anômalos e auto-scaling automático na nuvem. Complementarmente, parte da responsabilidade operacional é **Compartilhada** com provedores especializados (Cloudflare, AWS Shield Advanced), que possuem infraestrutura dedicada de absorção de tráfego malicioso em escala que a plataforma não poderia manter internamente com custo razoável. |
| **R06** | **Evitar** | A condição habilitadora — verificação apenas de autenticação (estar logado) sem verificação do papel (*role*) do usuário autenticado — pode ser completamente eliminada implementando RBAC com verificação explícita de escopo em cada endpoint administrativo e emitindo tokens JWT com *audiences* e *scopes* distintos e não intercambiáveis para cada perfil de usuário. Como a raiz do problema é um erro de design de autorização corrigível por implementação, a estratégia Evitar é a mais adequada. |

---

## 2.8 Apresentação das Funções do NIST CSF 2.0

Para organizar os resultados de segurança esperados e as medidas de mitigação no contexto do aplicativo de delivery, adotamos as seis funções do NIST Cybersecurity Framework 2.0. É importante ressaltar que as funções do NIST não são controles específicos, mas categorias lógicas que organizam os resultados esperados de segurança — cada função agrupa um conjunto de práticas e resultados, e os controles concretos são os meios para atingi-los.

| Função | Finalidade | Resultado esperado | Exemplo de controle no delivery |
| :--- | :--- | :--- | :--- |
| **Govern** | Definir políticas, responsabilidades, prioridades e critérios de decisão | Existência de políticas formais de segurança e papéis definidos | Política de banimento de contas com histórico de estornos fraudulentos; critérios documentados de aprovação de restaurantes e entregadores parceiros |
| **Identify** | Conhecer ativos, dependências, vulnerabilidades e riscos | Inventário atualizado de ativos e mapeamento de vulnerabilidades | Mapeamento de todos os endpoints vulneráveis a IDOR; inventário de dados pessoais armazenados (PII) classificados por sensibilidade |
| **Protect** | Implementar salvaguardas para reduzir a probabilidade ou o impacto | Controles técnicos e administrativos que dificultam ou impedem a exploração | Autenticação multifator (MFA); recálculo server-side de valores de pedido; RBAC com verificação de escopo em endpoints administrativos; substituição de IDs por UUIDs |
| **Detect** | Identificar eventos suspeitos, falhas e possíveis incidentes | Capacidade de identificar anomalias em tempo hábil | Rate limiting com alertas automáticos; logs de tentativas de acesso a IDs de outros usuários; monitoramento de picos de requisição nos endpoints públicos |
| **Respond** | Conter, analisar, comunicar e tratar incidentes | Plano de resposta definido e capacidade de contenção rápida | Bloqueio automático de sessão em login anômalo; invalidação imediata de token comprometido; protocolo de comunicação a usuários afetados em caso de vazamento |
| **Recover** | Restaurar serviços e dados e reduzir os prejuízos causados | Capacidade de retomada rápida das operações após incidente | Auto-scaling e circuit breaker após DDoS; restauração de banco de dados a partir de backup verificado após incidente de integridade |

---

## 2.9 Mapeamento dos Riscos para as Funções do NIST CSF

A tabela abaixo cruza os eventos de risco com as funções do NIST CSF 2.0 relevantes para seu tratamento. Cada marcação indica que a função é necessária para endereçar adequadamente o risco — funções foram marcadas apenas quando há relação direta com os controles propostos, evitando marcação indiscriminada.

| Risco | Origem | Govern | Identify | Protect | Detect | Respond | Recover |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **R01** (Sequestro de Sessão) | Spoofing / CA-01 | | | X | X | X | X |
| **R02** (Manipulação de Valor) | Tampering / CA-02 | | | X | X | X | |
| **R03** (Golpe do Estorno) | Repudiation / CA-03 | X | | X | X | X | |
| **R04** (Extração por IDOR) | Info. Disclosure / CA-04 | X | X | X | X | X | X |
| **R05** (DDoS em Horário de Pico) | DoS / CA-05 | | | X | X | X | X |
| **R06** (Broken Access Control) | Priv. Escalation / CA-06 | X | X | X | X | X | |

---

## 2.10 Plano de Tratamento

Nesta subseção detalhamos as medidas concretas que serão aplicadas para tratar cada risco, atribuindo os responsáveis diretos e as evidências que confirmarão que os controles existem e funcionam na prática.

| Risco | Estratégia | Controles Propostos | Funções do NIST | Responsáveis | Evidências e Verificação |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R01** (Sequestro de Sessão) | Reduzir | Vincular token JWT ao `device_id` e IP de origem no momento da emissão; aplicar MFA/TOTP obrigatório no login do entregador; configurar expiração do access token em 15 min com refresh token rotativo. | Protect, Detect, Respond, Recover | Equipe de IAM / Dev Backend | Logs de autenticação com registro de `device_id`; testes unitários de rejeição de token em dispositivo diferente do de emissão; simulação de login anômalo em ambiente de staging. |
| **R02** (Manipulação de Valor) | Reduzir | Backend recalcula obrigatoriamente o valor total do pedido com base nos preços do banco de dados, ignorando o valor enviado pelo cliente; assinar o payload do carrinho com HMAC antes do envio; rejeitar e registrar toda transação cujo valor recebido divirja do valor calculado no servidor. | Protect, Detect | Equipe de Pagamentos / Dev Backend | Testes unitários cobrindo 100% dos cenários de divergência de valor; relatório de transações rejeitadas por divergência; teste de mutação no fluxo de checkout. |
| **R03** (Golpe do Estorno) | Reduzir | Implementar código OTP de confirmação de entrega gerado no servidor e validado no ato; registrar geolocalização do entregador com timestamp no momento da marcação de "entregue"; exigir foto da entrega armazenada em log imutável; implementar análise comportamental para clientes com histórico de estornos recorrentes. | Govern, Protect, Detect, Respond | Logística / Dev Mobile / Suporte | Auditoria periódica dos logs de entrega no banco de dados; validação do fluxo de OTP em testes de integração; relatório mensal de taxa de estornos por cliente. |
| **R04** (Extração por IDOR) | Evitar | Substituir todos os IDs sequenciais por UUIDs v4 não previsíveis em todos os endpoints da API; implementar verificação de autorização em nível de objeto (RBAC/ABAC) validando se o usuário autenticado tem permissão sobre o recurso específico solicitado; configurar rate limiting com alertas automáticos para requisições a múltiplos IDs distintos em curto intervalo. | Identify, Protect, Detect, Respond, Recover | Dev Backend / SecOps | Relatório de pentest (DAST) demonstrando impossibilidade de acesso a recursos de outros usuários; testes de segurança automatizados (SAST) no pipeline de CI/CD; alertas de varredura ativos no sistema de monitoramento. |
| **R05** (DDoS em Pico) | Reduzir + Compartilhar | Configurar rate limiting por IP e por usuário autenticado nos endpoints públicos `/search` e `/catalog`; ativar Web Application Firewall (WAF) com regras de detecção de tráfego anômalo; configurar auto-scaling automático na nuvem com thresholds definidos; contratar serviço especializado de proteção anti-DDoS (Cloudflare ou AWS Shield Advanced) para absorção de tráfego em escala. | Protect, Detect, Respond, Recover | Infraestrutura / Cloud / SecOps | Relatórios mensais do WAF com volume de requisições bloqueadas; logs de ativação de auto-scaling; relatório de stress testing simulando pico de 50.000 req/s; SLA documentado do provedor anti-DDoS. |
| **R06** (Broken Access Control) | Evitar | Implementar RBAC com verificação explícita do papel do usuário em cada endpoint administrativo no servidor (não apenas no frontend); emitir tokens JWT com `scope` e `audience` distintos e não intercambiáveis para perfis de parceiro e administrador; cobrir todos os endpoints `/admin/` com testes automatizados de controle de acesso. | Govern, Identify, Protect, Detect, Respond | Dev Backend / SecOps | Revisão de código (code review) obrigatória para toda alteração em endpoints administrativos; logs de negação de acesso (HTTP 403) monitorados; teste automatizado no pipeline de CI/CD verificando que tokens de parceiro recebem 403 em rotas `/admin/`. |

---

## 2.11 Ordem Inicial de Implementação

A sequência para mitigação foi elaborada priorizando as vulnerabilidades de maior severidade e aquelas que exigem mudanças estruturais na fundação do software, considerando também as dependências técnicas entre os controles.

1. **R04 (Extração por IDOR):** Urgência máxima por impacto regulatório irreversível (LGPD/ANPD). A substituição de IDs sequenciais por UUIDs afeta a modelagem do banco de dados e múltiplos serviços — deve ser implementada primeiro para não exigir refatoração posterior de outros controles que dependem dos identificadores.
2. **R06 (Broken Access Control):** Urgência sistêmica imediata. A implementação de RBAC com verificação de escopo nos tokens é pré-requisito para a segurança de todos os endpoints da plataforma — sem ela, outros controles podem ser contornados por operadores com acesso ao portal parceiro.
3. **R02 (Manipulação de Valor):** Alta prioridade para estancar perdas financeiras diretas e recorrentes. A mitigação é tecnicamente simples e de implementação rápida, não dependendo de mudanças arquitetônicas — pode ser entregue logo após a estabilização dos controles de identidade.
4. **R01 (Sequestro de Sessão):** Requer intervenção coordenada no fluxo de autenticação do app mobile (MFA/TOTP) e no serviço de emissão de tokens (JWT binding ao dispositivo). Depende do modelo de autorização corrigido em R06 para garantir consistência dos escopos.
5. **R05 (DDoS em Pico):** Implementado integralmente na camada de infraestrutura — WAF, rate limiting e auto-scaling. Deve ser executado em paralelo aos itens de desenvolvimento backend (R02, R01) sem criar dependência técnica, aproveitando o mesmo ciclo de sprint.
6. **R03 (Golpe do Estorno):** Implementação de regra de negócio no app mobile (fluxo de OTP e foto de entrega). Menor urgência relativa por impacto unitário moderado; pode ser tratado após o saneamento das vulnerabilidades estruturais e financeiras.

---

## 2.12 Estimativa do Risco Residual

A redução do nível de risco somente será confirmada após a implementação dos controles, execução de testes rigorosos e coleta das evidências definidas no plano de tratamento. Os valores abaixo representam estimativas condicionadas à implementação completa e verificada de todos os controles propostos.

| Risco | Nível Inicial | Nível Residual Esperado | Condição para aceitar o residual |
| :--- | :---: | :---: | :--- |
| **R01** | Crítico | Médio | Token expirando em menos de 15 min, MFA ativo para todos os entregadores e logs confirmando bloqueio de tentativas de login com token em dispositivo diferente do de emissão. |
| **R02** | Alto | Baixo | Pipeline de CI/CD com testes unitários cobrindo 100% dos cenários de divergência de valor; zero transações aprovadas com valor divergente do calculado no servidor em ambiente de produção por 30 dias consecutivos. |
| **R03** | Alto | Baixo | Redução mensurável na taxa de estornos deferidos sem contestação; 100% das entregas com log imutável de OTP, geolocalização e foto disponíveis para auditoria em caso de disputa. |
| **R04** | Crítico | Baixo | Relatório de pentest (DAST) demonstrando falha em 100% das tentativas de enumeração de perfis; zero endpoints retornando dados de usuários sem validação de autorização por objeto em produção. |
| **R05** | Crítico | Médio | WAF ativo com relatório de bloqueio de tráfego anômalo; stress test simulando 50.000 req/s com disponibilidade mantida acima de 99% durante o teste; SLA do provedor anti-DDoS contratado e documentado. |
| **R06** | Alto | Baixo | Impossibilidade técnica comprovada de acesso a qualquer rota `/admin/` por token sem a role explícita de administrador; testes automatizados de controle de acesso integrados ao pipeline de CI/CD e executados a cada deploy. |

---

## 2.13 Considerações Finais da Etapa 2

Nesta segunda etapa, transformamos as ameaças identificadas na modelagem STRIDE em eventos de risco quantificados, priorizados e associados a planos de tratamento concretos, completando o ciclo de análise iniciado na Etapa 1.

**Riscos mais importantes e razões da priorização:** Os riscos classificados como Críticos — R04 (Extração por IDOR), R01 (Sequestro de Sessão) e R05 (DDoS) — compartilham a pontuação máxima de 12, mas foram diferenciados na ordem de tratamento por suas dependências arquitetônicas e pela natureza irreversível das consequências. R04 foi colocado em primeiro lugar por exigir mudança estrutural no modelo de dados com impacto em toda a plataforma e por representar a maior exposição regulatória sob a LGPD. R06, apesar de classificado como Alto, foi priorizado em segundo lugar por ser pré-requisito técnico para a segurança de todos os demais endpoints.

**Estratégias de tratamento predominantes:** A análise revelou que as estratégias de **Evitar** e **Reduzir** dominam o plano de tratamento. Evitar foi aplicada aos riscos de origem arquitetônica (R04 e R06), onde é possível eliminar a condição habilitadora por design. Reduzir foi aplicada aos riscos cujos vetores são externos ou comportamentais e não podem ser suprimidos (R01, R02, R03 e R05). Para R05, foi adicionada a estratégia complementar de **Compartilhar**, reconhecendo que a proteção contra DDoS em larga escala exige capacidade de infraestrutura que justifica a contratação de provedores especializados.

**Funções do NIST mais relevantes para o sistema:** A função **Protect** foi a mais abrangente, presente em todos os seis riscos, refletindo a necessidade de controles preventivos como MFA, RBAC, recálculo server-side e WAF. A função **Detect** foi a segunda mais recorrente, presente em cinco dos seis riscos, destacando a importância de monitoramento ativo, logs estruturados e alertas de anomalia para um sistema com superfície de ataque ampla. A função **Govern** aparece nos três riscos de natureza sistêmica (R03, R04, R06), onde políticas formais e definição de responsabilidades são pré-requisitos para a eficácia dos controles técnicos.

**Controles considerados essenciais:** Quatro controles se destacam por reduzirem múltiplos riscos simultaneamente e por serem pré-requisitos para outros controles: (1) implementação de RBAC com verificação de escopo em todos os endpoints — endereça R06 e fortalece R01 e R04; (2) substituição de IDs sequenciais por UUIDs — elimina a condição habilitadora de R04; (3) recálculo obrigatório de valores no servidor — elimina a exploração de R02; e (4) logs estruturados e imutáveis de todas as operações críticas — suporta a detecção e resposta em R01, R03, R04 e R06.

**Principais dificuldades encontradas:** A principal dificuldade foi diferenciar com precisão os conceitos de ameaça, vulnerabilidade, evento de risco e controle, garantindo que cada camada do documento tratasse do nível correto de abstração. A segunda dificuldade foi justificar a priorização de riscos com pontuação idêntica (R01, R04 e R05 com pontuação 12), o que exigiu análise qualitativa de dependências técnicas e natureza do dano além da pontuação numérica.

**Limitações da avaliação:** Como o sistema analisado é hipotético e não está em produção, os valores de probabilidade foram estimados com base em referências do setor e analogias com incidentes documentados em plataformas similares, sem acesso a dados históricos reais de ocorrências. Os níveis residuais estimados na seção 2.12 são projeções condicionadas à implementação completa e correta de todos os controles propostos — desvios de implementação (RBAC parcialmente aplicado, rate limiting com thresholds inadequados, MFA opcional em vez de obrigatório) podem resultar em níveis residuais superiores aos estimados.

**Pontos a detalhar nas próximas etapas:** Os controles propostos precisarão ser detalhados em especificações técnicas de implementação, incluindo: definição dos escopos exatos de cada papel no modelo RBAC; thresholds de rate limiting por endpoint; política de rotação e revogação de tokens JWT; requisitos de retenção e integridade dos logs de auditoria; e critérios de aceite para os testes de segurança (SAST/DAST) integrados ao pipeline de CI/CD.


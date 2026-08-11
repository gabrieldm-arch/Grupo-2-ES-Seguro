# Etapa 5 — Verificação de Vulnerabilidades

Nesta etapa, utilizamos a ferramenta de teste de segurança dinâmica (DAST) **OWASP ZAP** para varrer uma aplicação vulnerável padronizada (*OWASP Juice Shop*). O objetivo é observar o tráfego, identificar configurações inseguras e propor correções para os alertas gerados, simulando um ambiente de homologação antes de colocar um aplicativo web/API em produção.

## 5.1 Configuração da Verificação

* **Sistema testado:** OWASP Juice Shop (Aplicação web deliberadamente vulnerável, autorizada para fins educacionais).
* **Ferramenta utilizada:** OWASP ZAP (Zed Attack Proxy).
* **Configuração básica do teste:** Realizamos uma Varredura Automatizada (*Automated Scan*) padrão da ferramenta, iniciando com o *Spider* (aranha) para mapear e descobrir todas as rotas e arquivos públicos da aplicação, seguido imediatamente por um *Active Scan* focado em testar vetores de ataque comuns, injeções e vazamentos de cabeçalho HTTP. O escaneamento foi realizado sem credenciais prévias (análise em caixa preta).

## 5.2 Evidência da Execução

Abaixo consta a captura de tela evidenciando a execução do OWASP ZAP contra o alvo. O quadrante inferior exibe a aba de **Alertas**, detalhando as descobertas categorizadas por nível de criticidade.

![Evidência ZAP](../evidencias/etapa-5/capturas-de-tela/captura_zap.png)

## 5.3 Análise de Alertas e Correções

A partir da execução do ZAP, selecionamos três alertas relevantes que impactam a postura de segurança do *front-end* e da comunicação com as APIs. Abaixo, descrevemos o impacto potencial de cada um e propomos medidas corretivas baseadas em melhores práticas.

| ID | Alerta ou achado | Evidência                                                                                                                     | Possível impacto | Relação com OWASP ou CWE | Correção proposta |
| :---: | :--- |:------------------------------------------------------------------------------------------------------------------------------| :--- | :--- | :--- |
| **A01** | **Content Security Policy (CSP) Header Not Set** | O cabeçalho `Content-Security-Policy` não está presente nas respostas HTTP da aplicação.                                      | A ausência do CSP permite que o navegador do usuário confie e execute scripts de qualquer origem. Isso reduz drasticamente a defesa em profundidade e facilita ataques de *Cross-Site Scripting* (XSS) caso um atacante consiga injetar código na página. | OWASP A05:2021-Security Misconfiguration<br>CWE-693 (Protection Mechanism Failure) | Configurar o servidor web ou API Gateway para retornar o cabeçalho `Content-Security-Policy`. Exemplo de medida inicial: `default-src 'self'`, que restringe o carregamento de recursos apenas ao domínio de origem. |
| **A02** | **Missing Anti-clickjacking Header** | O cabeçalho de resposta `X-Frame-Options` (ou a diretiva `frame-ancestors` do CSP) não foi incluído pela aplicação.           | Um atacante pode embutir a aplicação inteira (ex: a tela de checkout do nosso delivery) dentro de um *iframe* invisível em um site malicioso controlado por ele. O usuário legítimo clicaria em botões sem saber que está executando ações na nossa plataforma (Clickjacking). | OWASP A05:2021-Security Misconfiguration<br>CWE-1021 (Improper Restriction of Rendered UI Layers or Frames) | Adicionar o cabeçalho HTTP `X-Frame-Options: DENY` (para impedir qualquer iframe) ou `SAMEORIGIN` (para permitir apenas no próprio domínio) em todas as páginas e rotas de estado que exigem interação. |
| **A03** | **Sub Resource Integrity Attribute Missing** | Arquivos carregados externamente (via tags `<script>` ou `<link>` apontando para CDNs) não possuem o atributo de integridade. | Se o CDN de terceiros que hospeda uma biblioteca (ex: jQuery, Bootstrap) for hackeado e o arquivo modificado com código malicioso, a nossa aplicação carregará e executará esse código indiscriminadamente para todos os usuários. | OWASP A06:2021-Vulnerable and Outdated Components<br>CWE-345 (Insufficient Verification of Data Authenticity) | Adicionar o atributo `integrity` contendo o hash criptográfico do arquivo (ex: `integrity="sha384-..."`) nas tags `<script>` e `<link>` externas, garantindo que o navegador bloqueie o carregamento caso o arquivo original seja alterado remotamente. |

### Considerações Finais — Etapa 5

A Etapa 5 complementou a análise estática e os testes unitários das etapas anteriores com uma verificação dinâmica em ambiente de execução real, utilizando o OWASP ZAP sobre o OWASP Juice Shop como alvo representativo de uma aplicação web vulnerável em estágio de homologação.

Os três alertas selecionados para análise — ausência de Content Security Policy (A01), ausência de proteção contra Clickjacking (A02) e ausência de Sub Resource Integrity em recursos externos (A03) — pertencem a uma categoria de vulnerabilidades frequentemente subestimada em projetos que focam apenas nas camadas de backend e autenticação. Nenhum dos três exige exploração sofisticada: a ausência de um cabeçalho HTTP é uma configuração de uma linha que, quando omitida, abre vetores de ataque relevantes como XSS facilitado, Clickjacking no fluxo de checkout e comprometimento de bibliotecas externas via CDN. No contexto do delivery, esses vetores são especialmente críticos porque a tela de checkout e o fluxo de pagamento são os alvos mais atrativos para ataques client-side.

É importante destacar que os alertas identificados pelo ZAP no Juice Shop são representativos de lacunas que também poderiam existir no sistema de delivery analisado, caso os cabeçalhos de segurança HTTP não fossem configurados explicitamente no API Gateway ou no servidor web. As correções propostas — configuração de CSP, X-Frame-Options e atributo integrity — são controles preventivos que complementam diretamente os controles de backend implementados na Etapa 4.

A principal limitação desta etapa é que a varredura foi realizada em modo caixa-preta e sem autenticação, o que significa que vulnerabilidades presentes em fluxos autenticados — como os endpoints de perfil vulneráveis a IDOR (R04) ou os endpoints administrativos sem RBAC (R06) — não foram alcançadas pelo scanner automatizado. Uma varredura autenticada com sessões de diferentes perfis (cliente, restaurante, administrador) seria necessária para validar completamente os controles implementados nas etapas anteriores e está indicada como próximo passo em um ciclo de segurança mais maduro.


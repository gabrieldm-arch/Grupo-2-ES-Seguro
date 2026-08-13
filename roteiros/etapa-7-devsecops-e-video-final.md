# Etapa 7 — DevSecOps e Vídeo Final

## 7.1 Fluxo DevSecOps da Equipe

Para garantir que as decisões de segurança acompanhem a evolução do App de Delivery e não se tornem gargalos no fim do processo, desenhamos um fluxo contínuo de DevSecOps dividido nas seguintes fases:

1. **Planejamento:** Antes de escrever o código, a equipe modela as ameaças da nova *feature* (usando STRIDE) e quantifica os riscos (NIST CSF) para definir os requisitos de segurança arquiteturais (ex: adotar UUIDs para evitar IDOR).
2. **Código Seguro:** O desenvolvedor aplica as diretrizes da OWASP (*Cheat Sheets*) e cria testes TDD de segurança antes da lógica de negócio (ex: forçar erro 403 para controle de acesso).
3. **Testes Automatizados (CI):** A cada *commit*, o GitHub Actions roda os testes unitários (SAST e TDD). Se um teste de segurança falhar, o *build* quebra.
4. **Verificação Dinâmica (DAST):** O código aprovado sobe para um ambiente de homologação (*Staging*), onde uma ferramenta automatizada (como o OWASP ZAP) escaneia a API em busca de falhas em tempo de execução (ex: falta de cabeçalhos CSP ou anti-clickjacking).
5. **Implantação Segura (CD):** Após a aprovação do DAST e revisão de código manual, a versão é liberada para produção.
6. **Monitoramento Operacional:** O sistema em produção envia logs estruturados e a infraestrutura aplica regras automáticas de detecção (ex: WAF limitando acessos abusivos e bloqueio por força bruta).

---

## 7.2 Tabela de Continuidade do Pipeline

Esta tabela resume os *gates* (portões de qualidade) do nosso fluxo automatizado. O *deploy* para produção só ocorre se todas as condições de continuidade forem satisfeitas.

| Momento | Atividade de segurança | Evidência produzida | Condição para continuar |
| :--- | :--- | :--- | :--- |
| **Planejamento** | Modelagem de Ameaças (STRIDE) e Análise de Riscos. | Tabela de ameaças, matriz de riscos e Requisitos de Segurança definidos. | Riscos inaceitáveis/críticos devem possuir um plano de tratamento formalizado. |
| **Código** | Implementação de código seguro baseado na OWASP e criação de testes (TDD). | Códigos fonte com validação *server-side* e *scripts* de testes de unidade. | Os testes devem cobrir obrigatoriamente cenários de ataques (inválidos) e cenários de sucesso (válidos). |
| **Testes (CI)** | Execução automatizada da suíte de testes de unidade e segurança no repositório. | Logs do *runner* (ex: GitHub Actions) exibindo `Pass` ou `Fail`. | 100% dos testes devem ser aprovados. |
| **Verificação (DAST)** | Escaneamento automatizado em ambiente de *Staging* usando OWASP ZAP. | Relatório de alertas e vulnerabilidades (HTML/PDF). | Nenhuma vulnerabilidade de criticidade Alta (*High*) ou Crítica (*Critical*) pode ser ignorada. |
| **Operação** | Coleta de logs, rate limiting e disparo de alertas de segurança. | Alertas gerados no painel de monitoramento e bloqueios no WAF. | Incidentes críticos devem ser contidos; ausência de falsos positivos excessivos travando usuários legítimos. |

---

## 7.3 Condições de Bloqueio

No conceito de DevSecOps, o botão "*Stop-the-line*" significa interromper imediatamente a esteira de implantação se algo grave for detectado, impedindo que o código vulnerável chegue à produção. Abaixo estão três gatilhos críticos no nosso sistema de delivery que fariam o *pipeline* travar sumariamente:

1. **Reprovação em Teste de Lógica de Negócio (Tampering):** Se a suíte automatizada rodar o teste de "Manipulação do Valor do Pedido" e o backend retornar sucesso (`HTTP 200 OK`) aceitando um carrinho com valor `R$ 0,00` adulterado pelo cliente. Isso indica falha no recálculo *server-side* e o código não pode subir.
2. **Vulnerabilidade de Controle de Acesso (Broken Access Control):** Se o DAST (OWASP ZAP) detectar ou os testes unitários falharem em impedir que um *token* com `role="restaurant"` acesse uma URL estrita de administração (ex: `/api/admin/commissions`). Isso indica exposição sistêmica.
3. **Vazamento de Segredos no Repositório:** Se o scanner de dependências ou de segredos do GitHub (ex: *TruffleHog* ou *Gitleaks*) identificar *commits* recentes contendo chaves privadas da API de Pagamento (Gateway), senhas de banco de dados ou a chave mestre (SECRET_KEY) de assinatura dos tokens JWT em texto claro.

## 7.4 Vídeo

**Link do Vídeo:** https://youtu.be/R76SqL1aWxw?si=zFQ1756ygJJIeqUD

### Considerações Finais — Etapa 7

A Etapa 7 encerrou o ciclo de análise do trabalho integrando todas as decisões e controles produzidos nas etapas anteriores em um fluxo contínuo de DevSecOps, demonstrando que segurança não é uma fase isolada do desenvolvimento mas uma responsabilidade distribuída ao longo de todo o ciclo de vida do software.

O fluxo definido — Planejamento com STRIDE, código seguro baseado em OWASP, testes automatizados no CI, verificação dinâmica com DAST em staging e monitoramento operacional em produção — reflete diretamente a progressão do próprio trabalho: cada etapa do documento corresponde a uma fase do pipeline. A modelagem de ameaças da Etapa 1 alimentou a análise de riscos da Etapa 2; os riscos priorizados determinaram os requisitos de arquitetura da Etapa 3; os requisitos guiaram as práticas de código e testes da Etapa 4; os testes dinâmicos da Etapa 5 validaram os controles em execução; e as regras de detecção da Etapa 6 garantem visibilidade operacional após o deploy. O pipeline DevSecOps não foi desenhado de forma independente — ele emergiu naturalmente da coerência entre as etapas anteriores.

As três condições de bloqueio definidas (falha no recálculo server-side, Broken Access Control detectado pelo DAST e vazamento de segredos no repositório) representam os cenários em que o custo de ir para produção supera qualquer pressão de prazo ou negócio. A definição explícita dessas condições é um resultado importante desta etapa: equipes que não documentam o que impede um deploy tendem a negociar segurança sob pressão, acumulando dívida técnica de segurança de difícil reversão.

A principal limitação do trabalho como um todo é que o sistema analisado é hipotético — os controles foram propostos, implementados em pseudocódigo e verificados em aplicações de referência, mas nunca testados no sistema de delivery real em produção com tráfego e dados reais. Em um contexto profissional, o próximo passo natural seria a execução de um pentest formal por equipe externa, a calibração dos thresholds de monitoramento com dados reais e a revisão periódica da modelagem de ameaças à medida que novas funcionalidades fossem adicionadas à plataforma.

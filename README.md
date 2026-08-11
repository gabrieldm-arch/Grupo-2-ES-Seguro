# Engenharia de Software Seguro — Grupo 2

> Repositório destinado ao Trabalho Final da disciplina de **Engenharia de Software Seguro (ESS)**, plataforma **Codefólio**.

---

## Identificação do Sistema

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

## Organização do Repositório

O repositório será estruturado para documentar a evolução contínua da análise e das decisões de segurança ao longo de todas as etapas da disciplina:

```text
Grupo-2-ES-Seguro/
├── README.md
│
├── docs/
│   ├── etapa-1-ameacas-stride.md
│   ├── etapa-2-riscos-nist.md
│   ├── etapa-3-arquitetura-segura.md
│   ├── etapa-4-codigo-seguro.md
│   └── etapa-5-verificacao-vulnerabilidades.md
│
├── diagramas/
│   ├── etapa-1/
│   │   └── visao-geral-do-sistema.png
│   └── etapa-3/
│       ├── arquitetura-segura.png
│       └── arquitetura-segura.drawio
│
├── codigo/
│   └── etapa-4/
│       ├── implementacao-ou-pseudocodigo
│       └── testes
│
├── evidencias/
│   └── etapa-5/
│       ├── capturas-de-tela/
│       └── relatorio-da-verificacao.md
│
└── roteiros/
    ├── etapa-6-deteccao-de-intrusoes.md
    └── etapa-7-devsecops-e-video-final.md
```

---

## Etapas do Trabalho

O projeto será desenvolvido em **7 etapas** ao longo da disciplina. O progresso de cada fase será acompanhado abaixo:

- [x] **Etapa 1:** Casos de Abuso e Modelagem de Ameaças com STRIDE 
- [x] **Etapa 2:** Análise, Priorização e Tratamento de Riscos com o NIST CSF 
- [x] **Etapa 3:** Projeto de uma Arquitetura Segura 
- [x] **Etapa 4:** Código Seguro e Testes de Segurança
- [x] **Etapa 5:** Verificação de Vulnerabilidades
- [x] **Etapa 6:** Monitoramento e Detecção de Intrusões 
- [ ] **Etapa 7:** DevSecOps e Vídeo Final *(Em andamento)*
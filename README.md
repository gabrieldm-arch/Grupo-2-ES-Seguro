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
├── README.md                           Apresentação do grupo e identificação do sistema
├── docs/                               Documentos principais em Markdown
│   └── modelagem-de-ameacas.md         Documento unificado de análise
├── diagramas/                          Diagramas de arquitetura, contexto, DFD e casos de uso
└── imagens/                            Imagens e figuras auxiliares utilizadas na documentação
```

---

## Etapas do Trabalho

O projeto será desenvolvido em **7 etapas** ao longo da disciplina. O progresso de cada fase será acompanhado abaixo:

- [ ] **Etapa 1:** Casos de Abuso e Modelagem de Ameaças com STRIDE *(Em andamento)*
- [ ] **Etapa 2:** Análise, Priorização e Tratamento de Riscos com o NIST CSF *(Em andamento)*
- [ ] **Etapa 3:** *Em breve*
- [ ] **Etapa 4:** *Em breve*
- [ ] **Etapa 5:** *Em breve*
- [ ] **Etapa 6:** *Em breve*
- [ ] **Etapa 7:** *Em breve*
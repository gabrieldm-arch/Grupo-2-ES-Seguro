# Implementação da Etapa 4

Neste projeto, optamos por entregar código executável em Python real (Test-Driven Development) no lugar de apenas pseudocódigo.

A lógica de implementação de cada prática segura (o *decorator* RBAC e a função *process_checkout*) está definida e testada nativamente dentro dos arquivos localizados na pasta `codigo/etapa-4/testes/`.

* `etapa4_rbac_test.py`: Contém a lógica de verificação de escopo de autorização no backend.
* `etapa4_checkout_test.py`: Contém a lógica de recálculo transacional no lado do servidor para mitigar fraudes de Mass Assignment.

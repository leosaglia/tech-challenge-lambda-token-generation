# tech-challenge-lambda-token-generation
## Descrição
Este repositório contém uma função Lambda responsável pela geração de tokens JWT, tokens que posteriormente serão utilizado para autenticação na geração de pedidos para os clientes.

Esta função é invocada via integração Lambda Proxy no Api Gateway [**fast-food-tech-challenge**](https://github.com/leosaglia/tech-challenge-infra-api-gateway).

Pode gerar tokens tanto para clientes identificados (que informam o CPF), quanto para clientes não identificados. Quando o cliente se identifica a lambda se integra com um serviço no EKS responsável por realizar a identifica do cliente.

Clientes identificados retornam informações complemetares (nome e cpf) no payload do token.

**Tecnologia:** Python

## Pré requisitos
Deve existir um cluster EKS, com a aplicação [fast-food-api](https://github.com/leosaglia/tech-challenge-fast-food-api) publicada e exposta via um NLB interno.

## Integrações e Dependências
- Integrações com AWS (Lambda, Secrets Manager) via **boto3**.
- **PyJWT** para manipulação de tokens JWT.
- **Requests** para se comunicar com o serviço presente no EKS, através do NLB.

## Workflow
Todo o deploy CI/CD é automatizado utilizado o github actions.

Utiliza o ***Github flow***. Possui a branch main protegida, com as alterações sendo realizadas em outras branchs, e quando concluídas, realizado o PR para main.

O workflow é definido em *.github/workflows/deploy-lambda.yml*.

1. Instalação das dependências do projeto Python.
2. Configuração de credenciais AWS para acessar serviços e fazer deploy.
3. Passos do Terraform (init, validate, plan) como ações de CI para gerenciar a infraestrutura da função Lambda.
4. Terraform apply após passar nos steps anterior o o merge for efetivado para main.

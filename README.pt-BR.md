# GitHub Project Publisher — Resumo em Português

> A documentação técnica completa está em inglês no [README principal](README.md).

## O que é

Uma ferramenta local para auditar e validar repositórios antes de publicá-los no GitHub.

## Qual problema resolve

Evita publicar projetos com documentação fraca, arquivos obrigatórios ausentes, alterações Git
pendentes, segredos acidentais ou estrutura difícil de entender.

## O que entrega

- relatório claro no terminal;
- relatório JSON para automação;
- nota de prontidão para publicação;
- checklist de Git, documentação, segurança, qualidade e apresentação.

## Como usar

```powershell
project-publisher audit C:\caminho\do\projeto
project-publisher check C:\caminho\do\projeto
```

## Segurança

Nesta primeira versão, os comandos são somente leitura: eles não reorganizam código nem alteram
o projeto analisado.

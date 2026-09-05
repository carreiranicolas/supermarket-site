# Lógica do Carrinho — Visitante, Login e Sessão

## Decisão de arquitetura

O carrinho de usuário não logado é implementado via **sessão do Django** (sem persistir no banco enquanto o usuário está anônimo). Ele só vira um registro real (`Carrinho` / `ItemCarrinho`) no momento do login ou cadastro.

Isso é uma decisão de **implementação**, não de **modelagem**: o DER continua o mesmo, com `Carrinho` 1:1 obrigatório com `Usuário`.

## Estrutura do carrinho na sessão

```python
request.session['carrinho'] = {
    produto_id: quantidade,
    ...
}
```

Atenção: o Django serializa a sessão como JSON, então as **chaves do dicionário viram string**. Ao comparar com `Produto.id` (inteiro), é necessário converter (`int(produto_id)`), senão a comparação falha silenciosamente.

## Fluxo de merge no login

Usar o signal `user_logged_in` do Django, para desacoplar da view de login (funciona independente do método de autenticação usado, ex: login social no futuro).

Passos:
1. Ler o dicionário `carrinho` da sessão.
2. Para cada `produto_id` (convertido para `int`) e `quantidade`:
   - Buscar o `Produto` no banco. Se não existir mais (removido/indisponível), ignorar esse item.
   - Verificar se já existe `ItemCarrinho` para esse produto no carrinho do usuário.
     - Se existir: somar as quantidades.
     - Se não existir: criar novo `ItemCarrinho`.
3. Limpar o carrinho da sessão (`del request.session['carrinho']`) — se não fizer isso, um login futuro soma o mesmo carrinho de novo.

## Preço: Carrinho vs. Pedido

- **Carrinho**: não guarda preço. Reflete sempre o `Produto.preco` atual — se o preço mudar enquanto o item está no carrinho, o carrinho deve refletir o novo valor.
- **Pedido**: o preço é "congelado" no momento da compra, em `ItemPedido.preco_unitario`. Um pedido finalizado não pode mudar de valor se o produto mudar de preço depois.

## Checkout (resumo do fluxo)

1. Ler os itens de `ItemCarrinho` do usuário.
2. Criar um `Pedido` novo, com status inicial (ex: "pendente").
3. Para cada item: criar um `ItemPedido`, copiando produto, quantidade e o preço atual do produto (que a partir daí fica fixo).
4. Esvaziar o `ItemCarrinho` do usuário — o `Carrinho` em si não é apagado, só fica vazio, pronto para o próximo ciclo.

## Configurações de sessão (settings.py)

```python
# COOKIES

SESSION_COOKIE_AGE = 60 * 60 * 24 * 2    # 2 dias, em segundos (padrão do Django: 2 semanas)
SESSION_SAVE_EVERY_REQUEST = True         # prazo é renovado a cada requisição (padrão: False)

# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Deixado comentado de propósito: se ativado, o carrinho de visitante seria perdido
# sempre que a aba fosse fechada, mesmo dentro do prazo de SESSION_COOKIE_AGE.
```

- `SESSION_COOKIE_AGE`: prazo de expiração da sessão, sempre em segundos.
- `SESSION_SAVE_EVERY_REQUEST`: se `True`, o prazo é recalculado a cada requisição (sliding), em vez de fixo desde a criação.
- `SESSION_EXPIRE_AT_BROWSER_CLOSE`: mexe no cookie do navegador, não no prazo do servidor — faz a sessão morrer ao fechar a aba, independente do `SESSION_COOKIE_AGE`. Os dois não são opostos entre si: agem em pontos diferentes do ciclo de vida da sessão e podem ser combinados sem contradição.

## Decisões já tomadas (contexto do modelo)

- Endereço de entrega = mesmo do cadastro do usuário (atributo do `Usuário`, não uma entidade separada).
- `Pagamento` = registro da transação específica de cada pedido (não um catálogo reaproveitável de formas de pagamento).
- `Status` = catálogo reaproveitável (tabela de consulta com os estados possíveis do pedido), por isso a cardinalidade (1,n) em relação a Pedido — diferente de `Pagamento`, que é exclusivo de cada pedido.

## Pendências / próximos passos

- [ ] Prototipar leitura/escrita do carrinho em sessão (adicionar, remover, atualizar quantidade).
- [ ] Implementar o merge no login via signal `user_logged_in`.
- [ ] Tratar o caso de borda: produto removido/indisponível durante navegação anônima.
- [ ] Implementar validação de estoque ao adicionar/finalizar (fora do escopo do DER, mas necessário na lógica).
- [ ] Fluxo de checkout completo (Carrinho → Pedido → ItemPedido → Pagamento).

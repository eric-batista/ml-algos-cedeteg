# Decision Tree Regression

## Sobre.
A árvore de decissão cria modelos de classificação, devide um conjunto de dados em  subconjuntos cada vez menores enquanto ao mesmo tempo, cada nó de decisão tem mais dois ramos cada um representando valores para o atributo testado.

## Tipos de árvores de decisão.
* ID3 (Dicotimizador interativo 3).
* C4.5 (Sucessor de ID3).
* Detecção automática de interações qui-quadrado(CHAID) - Executa divisões de vários  níveis ao calcular árvore ao calcular árvore de classificação.
* MARS - Estende as árvores de decisão para lidar melhor com os dados numéricos.
* Árvore de inferência condicional.

---

### Como funciona o algoritmo.
O algoritmo usa pontos de dados que precorre toda a árvore fazendo perguntas verdadeiro ou falso. começando do nó raiz, perguntas são feitas e ramificações separadas são criadas para cada resposta, e isso continua até que o nó folha seja alcançado.

![img](https://datascience.foundation/img/pdf_images/understanding_decision_trees_with_python_decision_tree.png)

* Nós Raiz
* Nós de decissões ou Interno
* Folhas

### Nos Raiz.
  Geralmente é o nó superior também chamado nó de decisão superior, ele representa toda a população ou amostra e ainda é dividida em dois ou mais conjuntos homogêneos.
    
### Nó de decisão ou Interno.
  Quando um subnós se divide em outros subnós, ai acabam se tornando nós internos, que geralmente e chamamo-os de "troco" da nossa árvore, 
  no caso são as informações ainda não prédefinida.

### Nós Folhas.
  Chamados de nós filhos também, no caso esses nós não possuem ramificações e assim geralmente ficam no final da árvore, e geralmente definem nossa tomada de decisão.

---

## Pros. 
* Otimo para pradrões não lineares.
* Simples de intender e implementar.
* Capas de lidar com dados categoricos.
* Requer pouca preparação de dados.
* Possivel validar um modelo por meio estatistico.
* Apresenta bom desempenho com grandes conjuntos de dados.
* Espelha tomada de decisão humana mais de perto que outras abordagens.
## Contras.
* A profundidade média da árvore que é definida pelo números de nós e o teste de classificação não garantida como minima ou pequena sob vários critérios de divisão.
* Para dados incluem variáveis categóricas com diferentes números de niveis, o ganho da árvore de decisão é tendencioso em favor de atributos com mais níveis.
* Os nós da árvore podem criar ramos entremamentes complexos que não generalizam bem a partir dos dados de treinamento.
---

## Tecnologias Utilizadas:
    Python
    C++
    MetaTrader5

---

# Autor: 
    Renan Lemes Leepkaln

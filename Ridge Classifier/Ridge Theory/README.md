# Ridge Classifier

#### Primeiramente precisamos explicar alguns conceitos antes de definir o modelo Ridge Classifier:

* **Regressão:** é caracterizada pela regularização dos dados, ou seja, é feito uma tentativa de ajuste na função de acordo com os dados, porém se isso for feito em excesso, 
pode ocorrer o overfitting, pois o nivel de variância está alto. Para evitar que isso ocorra, é inserido mais viés (bias) dentro do modelo para que a sua variância diminua. 
* **Modelo de regressão Ridge:** é caracterizado pela adição de penalidades dentro da função. A regressão linear usa a soma residual dos quadrados (RSS) a fim de fazer este ajuste,
já o Ridge utiliza a mesma soma, porém adiciona a penalidade L2, que consiste em elevar as variáveis ao quadrado. Deste modo os coeficientes das features que estão interligadas, 
poderão ter resultados parecidos, ou até mesmo um coeficiente alto, enquanto o outro coeficiente seria 0. Abaixo está ilustrado a soma residual dos quadrados utilizando a 
penalidade L2:

<img src="https://miro.medium.com/max/1060/1*_2_bFm9NkDrOmfOYs5lNFA.png" width="500px">

#### Agora após estas definições, podemos entender como funciona o modelo Ridge Classifier:
* **Modelo Ridge Classifier:** Este modelo é derivado do seu modelo de regressão, porém ele possui um passo anterior, que é caracterizado pela conversão dos valores alvo (target) 
em valores {-1, 1}, desta forma estamos tratando a coluna alvo como sendo true e false (trata-se de um modelo classifier). Após ser feita esta conversão, podemos tratar o 
problema como uma regressão Ridge.

---

### Vantagens do modelo: 
A principal vantagem deste modelo é que ele traz melhores previsões a longo prazo e também quando as variáveis são utéis para o modelo, pois se a variável de inclinação (α) for 
um valor alto, os coeficientes vão encolher bastante e chegar em um valor bem próximo de 0, porém nunca vai ser 0.

---

### Desvantagens do modelo:
Podemos classificar como a sua principal desvantagem, uma precisão não tão boa quando temos muitos paramêtros e a maioria deles não são muito úteis para a análise, desta forma 
ele não é capaz de excluir as variáveis inúteis. Isso ocorre porque quando aumentamos o valor de α, a reta se aproxima do eixo X, ou seja, a inclinação se aproxima de 0, e o 
valor dos coeficientes vai ser reduzido chegando em um valor bem próximo de 0. Neste quesito, a regressão em Lasso é melhor, pois ela consegue eliminar as variáveis inúteis e 
torna a equação mais simples de se interpretar. 

---

### Diferença entre os modelos lineares:
Como já foi mencionado anteriormente, a regressão em Lasso é mais útil quando temos mais coeficientes, pois ela consegue eliminar as variáveis inúteis do conjunto de dados. 
Já a regressão em Ridge, é melhor quando a maioria das variáveis são úteis, pois quando existir dados desnecessários, ao invés de eliminar as variáveis anulando o seu valor, 
ela define valores bem próximos de 0, porém nunca serão 0. Ambos podem ser aplicados em modelos mais complexos. Agora comparando com o modelo Elastic Net, podemos perceber que 
ele é a união dos dois modelos, conseguindo extrair o melhor dos dois. O Elastic, é mais usado quando temos milhares ou até milhões de dados, pois ele tem um melhor desempenho 
com dados correlatos.

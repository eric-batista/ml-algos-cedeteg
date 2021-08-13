# Regressão Linear, Lasso Aplicando o método de Larry Willians

# Sobre o projeto:
  A  ideia principal foi fazer um robo para mercado financeiro que utilizava da linguagem python e o aplicativo MetaTrader5.
  No projeto foi ultilizado combinação linear dos recursos preditores de X, para prever nosso recurso a resposta depois fizemos restrições de norma L2,     que vem da regressão linear que e dado por:
  
  
  ![equation](https://miro.medium.com/max/327/1*UFsN2JHfP5t_E1a9icTbwQ.png)
  
  
  Desta forma surge o método LASSO Acrony for Least Absolute Sheinkage and Selection Operator, que faz com que a regressão tenha uma contração absoluta 
  ou seja uma aproximação de forma fechada direta, ou seja seus coeficientes tendem para zero.
  
  ![equation](https://miro.medium.com/max/535/1*dynW6DLJxX2iaMrnfgxk_A.png)
  
  Desta forma quando temos bastantes features extremamentes correlacionados neste caso o Lasso pega uma e zera as demais.
  
  ![img](https://miro.medium.com/max/600/1*iz4AZmNJGWNzOX5P-SmW4A.png)

---
### Larry Williams

Foi desenvolvido pelo trader Larry Williams é uma estratégia simples conhecida como setup de reversão, ou seja quando a média móvel muda de direção fazemos  a compra ou a venda.


#### Setup 9.1
      
   ![img](https://economia.culturamix.com/blog/wp-content/gallery/setup-larry-williams-3/Setup-Larry-Williams-4.png)
   
 ### Compra
 Procuramos por ativos em que a MME9 esteja apontando para baixo. No momento em que ela vira para cima, marcamos o candle que fez a linha mudar de   direção.   A entrada da operação se dá no rompimento (superação) da máxima desse candle. 
  
  ### Venda
  É o oposto do setup de compra, onde procuramos por ativos em que a MME9 esteja apontando para cima. No momento em que ela vira para baixo, marcamos o candle que fez a linha mudar de direção. A entrada da operação se dá na perda da mínima desse candle.

---
## Tecnologias Utilizadas:
    Python
    C++
    MetaTrader5
---
# Autor: 
    Renan Lemes Leepkaln

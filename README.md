# Dashboard de Análise de Tráfego de Servidor em Tempo Real

Este trabalho consiste em desenvolver um dashboard web.
Utilizando uma porta espelhada no switch para capturar todo o tráfego de e para um servidor-alvo,
nosso sistema irá processar esses dados e exibi-los em um gráfico de barras dinâmico.
O dashboard mostrará, em janelas de 5 segundos, o volume de tráfego de entrada e saída,
agrupado por cada cliente (IP) que se comunica com o servidor.

Além disso, a interface permitirá uma análise mais profunda (drill down),
revelando a quebra de tráfego por protocolo para cada cliente.

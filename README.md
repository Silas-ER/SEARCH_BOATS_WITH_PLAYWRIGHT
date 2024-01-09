# Localização atual de barcos

<h2>Objetivo</h2> 
<p>
    O script foi criado com objetivo de suprir uma demanda de localização da frota de barcos da empresa onde trabalho,
    para tal realizei o estudo do metódo que eles utilizavam anteriormente que consistia em abrir um site asiático e digitar manualmente cada 
    um dos dados dos barcos para assim encontrar sua localização, não tendo como ter um método de comparação de distancia, já que o site só exibia em sua 
    versão gratuita, um barco por vez. 
</p>
<h2>Execução</h2>
<p>
    Portanto explorei a exibição de duas maneiras distintas mas que permitissem ao usuario tanto armazenamento de dados quanto a exibição visual. 
    <br>
    Para isso inicialmente planejei que o script leria os dados do site, os armazenando em uma lista e assim eu poderia manipula-los, tanto para a criação do mapa
    quanto o armazenamento que seria numa planilha no google sheets.
    <br>
    Com isso os dados necessários para o web scraping, para tal seriam: 
        <ul>
            <li>Dados de login do site (credentials.txt)</li>
            <li>Lista dos dados dos barcos (data_query.txt)</li>
            <li>Dados de login do email (data_smtp.txt)</li>
            <li>E-mails de usuários aos quais os arquivos serão encaminhados (adressees.txt)</li>
            <li>Credencial para o (client_secret.json ou token.json)</li>
        </ul> 
</p>
Web Scraping

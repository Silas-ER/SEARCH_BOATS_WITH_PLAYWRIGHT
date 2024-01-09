# Localização atual de barcos

<h2>Objetivo</h2> 
<p>
    O script foi criado com objetivo de suprir uma demanda de localização da frota de barcos da empresa onde trabalho,
    para tal realizei o estudo do metódo que eles utilizavam anteriormente que consistia em abrir um site asiático e digitar manualmente cada 
    um dos dados dos barcos para assim encontrar sua localização, não tendo como ter um método de comparação de distancia, já que o site só exibia em sua 
    versão gratuita, um barco por vez. 
</p>
<h2>Planejamento</h2>
<p>
    Portanto explorei a exibição de duas maneiras distintas mas que permitissem ao usuario tanto armazenamento de dados quanto a exibição visual. 
    <br>
    Para isso inicialmente planejei que o script leria os dados do site, os armazenando em uma lista e assim eu poderia manipula-los, tanto para a criação do mapa
    quanto o armazenamento que seria numa planilha no google sheets.
    <br>
    Com isso os dados necessários para o web scraping, para tal seriam: 
        <ul>
            <li>
                <h3>Dados de login do site (credentials.txt)</h3>
                <p>São os dados necessários para o login no site em que se capturam os dados de localização, no caso o https://www.shipdt.com/#/ </p>
            </li>
            <li>
                <h3>Lista dos dados dos barcos (data_query.txt)</h3>
                <p>
                    Lista com os dados de cada barco que queremos saber as localizações
                </p>
            </li>
            <li>
                <h3>Dados de login do email (data_smtp.txt)</h3>
                <p>
                    Dados de login do email que vai realizar os envios
                </p>
            </li>
            <li>
                <h3>E-mails de usuários aos quais os arquivos serão encaminhados (adressees.txt)</h3>
                <p>
                    Lista com os emails dos usuarios que irão receber os mapas e planilhas
                </p>
            </li>
            <li>
                <h3>Credencial para o (client_secret.json ou token.json)</h3>
                <p>
                    Credencial necessária para API do google realizar a conexão com o google drive e atualizar a planilha online
                </p>
            </li>
        </ul> 
</p>
<h2>Execução</h2>
<p>
    
</p>

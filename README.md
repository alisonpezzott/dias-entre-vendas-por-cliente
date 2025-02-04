# Dias entre vendas por clientes

> [!NOTE]
> Repositório criando por Alison Pezzott em resposta ao questionamento em https://discord.com/channels/1279778182941245503/1332361733645537440  


## Download da base

Faça o download do arquivo [vendas.csv](https://overdax-my.sharepoint.com/:f:/g/personal/alison_pezzott_fluentebi_com/EisVch9F1V1KiIW5tbKSznUBILjXuPz02JRCEqVa-wRtGA?e=wWkvGP)  
Extraia e coloque o arquivo dentro da pasta `C:/Temp/`.   


## SQL

Adicionamos os dados em uma tabela no banco de dados com 

```sql
IF NOT EXISTS ( SELECT * FROM sys.databases WHERE name = 'sandbox' )
BEGIN
    CREATE DATABASE sandbox;
END
GO

USE sandbox;
GO

DROP TABLE IF EXISTS vendas;
GO

CREATE TABLE vendas (       
	Venda_ID INT, 
	Data DATE, 
	Cliente_ID INT, 
	Valor MONEY 
); 

GO 

BULK INSERT vendas 
FROM 'C:/Temp/vendas.csv' 
WITH (     
	CODEPAGE = '65001',     
	FIELDTERMINATOR = ';',      
	FIRSTROW = 2  
); 

SELECT TOP (100) * FROM vendas;

SELECT COUNT (*) FROM vendas; 

```

Vamos rodar agora o código para encontrar a média de tempo entre vendas por cliente.  

```sql
WITH CTE_DataVendaAnterior AS (
    SELECT 
        Cliente_ID,
        Venda_ID,
        Data,
        COALESCE (
            LAG ( Data ) OVER ( PARTITION BY Cliente_ID ORDER BY Data ASC ),
            Data
        ) AS Ultima_Data_Venda
    FROM vendas
),
CTE_DifDias AS (
    SELECT 
        Cliente_ID,
        Venda_ID,
        Data,
        Ultima_Data_Venda,
        DATEDIFF ( DAY, Ultima_Data_Venda, Data ) AS Dif_Dias
    FROM CTE_DataVendaAnterior
)
SELECT 
    Cliente_ID,
    AVG ( Dif_Dias * 1.0 ) AS Media_Dias_Entre_Vendas
FROM CTE_DifDias
GROUP BY Cliente_ID 
ORDER BY Cliente_ID; 

```

## Power BI

Crie um novo arquivo do Power BI Desktop e ingira os dados do SQL Server com o Power Query, feche e aplique.  

Crie a coluna calcula na tabela `vendas`  

```dax
VendaAnteriorDoCliente = 

    COALESCE(
        SELECTCOLUMNS(
            OFFSET(
                -1,
                ALL(vendas[Cliente_ID], vendas[Venda_ID], vendas[Data]),
                ORDERBY([Data]),
                PARTITIONBY(vendas[Cliente_ID])
            ),
            [Data]
        ),
        [Data]
    )

```  


Crie a medida `Média dias entre vendas por cliente`   

```dax
Média dias entre vendas por cliente =
			
    AVERAGEX(
        vendas,
        DATEDIFF(vendas[VendaAnteriorDoCliente], vendas[Data], DAY)
    ) 

```

Acrescente na tela uma tabela com a coluna `Cliente_ID` e a medida recém-criada `Média dias entre vendas por cliente`.  
Ordene por `Cliente_ID` e verifique a medida criada.  

## Conclusão

Com este repositório você aprendeu como calcular a média de dias entre as vendas por clientes de forma congelada com a linguagem SQL e de forma dinâmica com a linguagem DAX no Microsoft Power BI.  

A partir de agora você pode aplicar outras análises com esta métrica seja para filtrar clientes ou analisar correlação com outras variáveis como valor de vendas, ticket médio, churn entre outros.

> [!TIP]  
> Siga meus canais:  
> YouTube: [youtube.com/@alisonpezzott](youtube.com/@alisonpezzott)  
> Linkedin: [linkedin.com/in/alisonpezzott](linkedin.com/in/alisonpezzott)  
> Instagram: [instagram.com/alisonpezzott](instagram.com/alisonpezzott)  
> GitHub: [github.com/alisonpezzott](github.com/alisonpezzott)  
> Discord: [discord.gg/sJTDvWz9sM](discord.gg/sJTDvWz9sM)  
> Telegram: [t.me/alisonpezzott](t.me/alisonpezzott)

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

Vamos rodar agora o código para encontrar a média de dias entre vendas por cliente.  

```sql
WITH CTE_DataVendaAnterior AS (
    SELECT 
        Venda_ID,
        Data,
        Cliente_ID,
        LAG(Data) 
            OVER ( 
                PARTITION BY Cliente_ID 
                ORDER BY Data ASC, Venda_ID ASC 
            ) AS UltimaDataVenda
    FROM vendas
),
CTE_DifDias AS (
    SELECT 
        Venda_ID,
        Data,
        Cliente_ID,
        UltimaDataVenda,
        DATEDIFF ( DAY, UltimaDataVenda, Data ) AS DifDias
    FROM CTE_DataVendaAnterior
    WHERE UltimaDataVenda IS NOT NULL
)
SELECT 
    AVG ( DifDias * 1.0 ) AS DiasEntreVendas
FROM CTE_DifDias; 

```

## Power BI

Crie um novo arquivo do Power BI Desktop e ingira os dados do SQL Server com o Power Query, feche e aplique.  

Crie a coluna calcula na tabela `fact_vendas`  

```dax
DataVendaAnterior = 

VAR __UltimaDataVenda = 
    OFFSET (
        -1,
        ALLSELECTED ( 
            fVendas[Data],
            fVendas[Venda_ID],
            fVendas[Cliente_ID]
        ),
        ORDERBY ( [Data], ASC, [Venda_ID], ASC ), 
        PARTITIONBY (  fVendas[Cliente_ID] )
    )

VAR __Resultado =  
    SELECTCOLUMNS ( __UltimaDataVenda, [Data] )

RETURN 
    __Resultado
    

```  


Crie a medida `Dias entre vendas`   

```dax
Dias entre vendas = 
    AVERAGEX (
        FILTER (
            fVendas,
            [DataVendaAnterior]
        ), 
        DATEDIFF ( [DataVendaAnterior], [Data],  DAY )
    )

```

Acrescente na tela uma tabela com a coluna `Cliente_ID` e a medida recém-criada `Dias entre vendas`.  
Ordene por `Cliente_ID` e verifique a medida criada.  

## Faixas de dias  

Este exemplo permite que você crie faixas de dias para os clientes.  

Crie uma tabela calculada em DAX chamada de `faixas`  

```dax
faixas = 

-- Parâmetros
VAR __Inicio = 0
VAR __Final = 365
VAR __Passo = 30

-- Criação da tabela
VAR __padrao = 
    SELECTCOLUMNS (
        GENERATESERIES ( __Inicio, __Final, __Passo ),
        "Min", [Value],
        "Max", [Value] + __Passo
    )

VAR __ultimaFaixa = {( __Final + __Passo, 999999 )}

VAR __estrutura = UNION ( __padrao, __ultimaFaixa )

RETURN

-- Adiciona a coluna faixa
    ADDCOLUMNS (
        __estrutura,
        "Faixa", 
        SWITCH ( 
            TRUE(), 
            [Min] = 0, "<" & [Max],
            [Max] = 999999, [Min] & "+",
            [Min] & "~" & [Max]
        )
    )

```  

> [!IMPORTANT] 
> Ordene a coluna `Faixa` pela coluna `Min`.  

Como esta é uma tabela auxiliar e desconectada do modelo crie a medida que fará conexão com ela através da função FILTER.  

```dax
Clientes por faixas = 

VAR __fonte =
    ADDCOLUMNS (
	    VALUES ( vendas[Cliente_ID] ),
        "@Media", [Dias entre vendas]
    )

VAR __faixas = 
    ADDCOLUMNS (
        faixas,
        "@Clientes",
        COUNTROWS (
            FILTER ( 
                __fonte,
                [@Media] >= faixas[Min] &&
                [@Media] <  faixas[Max]
            )
        )
    )

VAR __Resultado = SUMX ( __faixas, [@Clientes] )

RETURN
    __Resultado
```  

Coloque na tela um visual de colunas cluesterizadas, coloque no eixo x a coluna `'faixas'[Faixa]`  e no eixo Y a medida recém-criada `Clientes por faixas`.  

A partir de então esta medida se torna coringa para que as faixas filtrem qualquer medida basta usá-la na sintaxe das medidas assim como no exemplo abaixo onde estamos segregando o valor total por faixas.  

```dax
Valor total por faixas = 
    CALCULATE (
        SUM ( vendas[Valor] ),
        FILTER (
            VALUES ( vendas[Cliente_ID] ),
            [Clientes por faixas]
        )
    ) 
```  


## Conclusão

A partir de agora você pode aplicar outras análises com esta métrica seja para filtrar clientes ou analisar correlação com outras variáveis como valor de vendas, ticket médio, churn entre outros.

> [!TIP]  
> Siga meus canais:  
> YouTube: [youtube.com/@alisonpezzott](youtube.com/@alisonpezzott)  
> Linkedin: [linkedin.com/in/alisonpezzott](linkedin.com/in/alisonpezzott)  
> Instagram: [instagram.com/alisonpezzott](instagram.com/alisonpezzott)  
> GitHub: [github.com/alisonpezzott](github.com/alisonpezzott)  
> Discord: [discord.gg/sJTDvWz9sM](discord.gg/sJTDvWz9sM)  
> Telegram: [t.me/alisonpezzott](t.me/alisonpezzott)

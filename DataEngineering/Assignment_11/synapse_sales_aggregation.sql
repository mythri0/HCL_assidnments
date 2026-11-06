-- Azure Synapse Serverless SQL Query for Data Validation
-- Executed by: Poornima (NorthStar Retail)

-- Query processed Parquet output directly from Azure Data Lake Storage Gen2
SELECT 
    region,
    ROUND(SUM(total_sales), 2) AS total_sales,
    COUNT(transaction_id) AS transaction_count
FROM 
    OPENROWSET(
        BULK 'https://adlspoornimasales.dfs.core.windows.net/raw-data/*.parquet',
        FORMAT = 'PARQUET'
    ) AS [result]
WHERE 
    total_sales > 100
GROUP BY 
    region
ORDER BY 
    total_sales DESC;

# daxgenie
AI-powered DAX formula assistant for Power BI 
# DAX Cheatsheet

A collection of common DAX patterns I use as a Power BI analyst.

## Time Intelligence

### Year-over-Year Growth

    YoY Growth =
    VAR Current = [Total Sales]
    VAR Previous = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Calendar[Date]))
    RETURN DIVIDE(Current - Previous, Previous)

### Running Total

    Running Total =
    CALCULATE(
        [Total Sales],
        FILTER(
            ALLSELECTED(Calendar[Date]),
            Calendar[Date] <= MAX(Calendar[Date])
        )
    )

### Sales Last 30 Days

    Sales Last 30 Days =
    CALCULATE(
        [Total Sales],
        DATESINPERIOD(Calendar[Date], MAX(Calendar[Date]), -30, DAY)
    )

## Aggregations

### Safe Division

    Profit Margin = DIVIDE([Profit], [Revenue], 0)

### Filtered Sum

    Sales Active Customers =
    CALCULATE(
        [Total Sales],
        Customer[Status] = "Active"
    )

## Ranking

### Top 5 Products

    Top 5 Sales =
    CALCULATE(
        [Total Sales],
        TOPN(5, ALL(Products), [Total Sales])
    )

## Notes

These are DAX patterns I have worked with while studying for my Microsoft Power BI Data Analyst certification. I share them here as a personal reference and for other analysts learning DAX.

## License

MIT
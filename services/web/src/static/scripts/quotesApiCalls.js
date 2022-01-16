const axios = window.axios;

export const updatePrices = (tickers, portfolioRows) => {

    let api_url='https://stockportfoliotracker.net/quotes?';

    for (const ticker of tickers) {
        api_url = api_url.concat(`t=${ticker}&`);
    }

    axios.get(api_url)
    .then((response) => {
        const data = response.data;
        for (const row of portfolioRows) {
            // Last Price
            const price = data[row.id]['price'];
            // Open price
            const open = data[row.id]['open'];
            // Calculate daily profit/loss
            const dayPl = (price - open).toFixed(2);
            // Set daily p/l column
            row.cells.item(2).innerHTML = (dayPl * row.cells.item(1).innerHTML).toFixed(2);
            // Set daily % change
            row.cells.item(3).innerHTML = `${(dayPl / price * 100).toFixed(2)}%`
            // Set last price
            row.cells.item(4).innerHTML = price.toFixed(2);
            // Update Total Value
            const value = price * row.cells.item(1).innerHTML;
            row.cells.item(7).innerHTML = value.toFixed(2);
            // Update Unrealized p/l
            const unrel = value - row.cells.item(6).innerHTML;
            // Color cells green or red if up or down
            const unrelRow = row.cells.item(8);
            unrelRow.innerHTML = unrel.toFixed(2);
            if (unrel == 0) {
                unrelRow.style.color = "#000000";            
            }
            else if (unrel < 0) {
                unrelRow.style.color ="#AA0000";
            }
            else {
                unrelRow.style.color="#00AA00";
            }
            const dayRow = row.cells.item(2);
            if (dayPl > 0) {
                dayRow.style.color = "#00AA00";
            }
            else if (dayPl < 0) {
                dayRow.style.color = "#AA0000";
            }
            else {
                dayRow.style.color = "#000000";
            }
            const dayPercRow = row.cells.item(3);
            if (dayPl > 0) {
                dayPercRow.style.color = "#00AA00";
            }
            else if (dayPl < 0) {
                dayPercRow.style.color = "#AA0000";
            }
            else {
                dayPercRow.style.color = "#000000";
            }
        }
    }, (error) => {
        console.log(error);
    });

}


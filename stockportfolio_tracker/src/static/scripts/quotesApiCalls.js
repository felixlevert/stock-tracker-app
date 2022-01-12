const axios = window.axios;

export const updatePrices = (tickers, portfolioRows) => {

    let api_url='http://localhost:5001/quotes?';

    for (const ticker of tickers) {
        api_url = api_url.concat(`t=${ticker}&`);
    }

    axios.get(api_url)
    .then((response) => {
        const data = response.data;
        for (const row of portfolioRows) {
            // Update Last Price
            const price = data[row.id]['price'];
            const open = data[row.id]['open'];
            const dayPl = (price - open).toFixed(2);
            row.cells.item(2).innerHTML = (dayPl * row.cells.item(1).innerHTML).toFixed(2);
            row.cells.item(3).innerHTML = `${(dayPl / price * 100).toFixed(2)}%`
            row.cells.item(4).innerHTML = price.toFixed(2);
            // Update Total Value
            const value = price * row.cells.item(1).innerHTML;
            row.cells.item(7).innerHTML = value.toFixed(2);
            // Update Unrealized p/l
            const unrel = value - row.cells.item(6).innerHTML;
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
        }
    }, (error) => {
        console.log(error);
    });

}

export const getQuote = (ticker) => {
    const api_url = `http://localhost:5002/quotes?${ticker}`;

    axios.get(api_url)
    .then((response) => {
        const data = response.data;
        return data[ticker];
    }, (error) => {
        console.log(error);
    });
}

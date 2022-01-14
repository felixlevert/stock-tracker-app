import { ModalHandler } from './ModalHandlers.js'
import { updatePrices, getQuote } from './quotesApiCalls.js';


class App {
    static init() {
        new ModalHandler('new-position-button', 'add-position-modal', 'add');
        new ModalHandler('sell-position-button', 'sell-position-modal', 'sell');
        let tickers = [];
        const portfolioRows = document.getElementById('portfolio-table-body').querySelectorAll('tr');;
        for (const row of portfolioRows) {
            tickers.push(row.id);
        }
        setInterval(function() {
            updatePrices(tickers, portfolioRows);
        }, 1000);
                 
    }
}

App.init();
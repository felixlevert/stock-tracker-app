import { ModalHandler } from './ModalHandlers.js'
import { updatePrices} from './quotesApiCalls.js';


class Portfolio {
    static init() {
        new ModalHandler('new-position-button', 'add-position-modal', 'add');
        new ModalHandler('sell-position-button', 'sell-position-modal', 'sell');
        new ModalHandler('new-position-button-mobile', 'add-position-modal', 'add');
        new ModalHandler('sell-position-button-mobile', 'sell-position-modal', 'sell');
        let tickers = [];
        const portfolioRows = document.getElementById('portfolio-table-body').querySelectorAll('tr');;
        for (const row of portfolioRows) {
            tickers.push(row.id);
        }
        // Update stock prices every second.
        setInterval(function() {
            /* 
            Only call updatePrices if there are stocks in portfolio
            Avoids unnessecary API calls.
            */
            if (tickers[0] != '') {
                updatePrices(tickers, portfolioRows);
            }            
        }, 1000);
    }
}

Portfolio.init();

class Login {
    static init() {
        // Demo button fills in demo account info and submits login form.
        const demoButton = document.getElementById('demo-account-btn');
        demoButton.addEventListener('click', () => {
            const inputs = document.querySelectorAll('.input');
            inputs[0].value = 'test@test.com';
            inputs[1].value = 'test';
            const form = document.querySelector('form');
            form.submit();
        })
    }
}

Login.init();
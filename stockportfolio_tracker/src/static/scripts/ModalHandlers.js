

export class ModalHandler {
    constructor(id, modalId, action) {
        this.modal = document.getElementById(modalId);
        this.background = document.getElementById(`${action}-modal-bg`);
        this.form = this.modal.querySelector('form');
        this.thisModalVisible = false;
        this.action = action;
        this.connectAddButton(id);
        this.connectCancelButton();
    }

    connectAddButton(id) {
        const button = document.getElementById(id);
        button.addEventListener('click', this.addButtonHandler);
    }


    connectCancelButton() {
        document.getElementById(`cancel-${this.action}-btn`).addEventListener('click', this.closeModalHandler);
        document.getElementById(`close-${this.action}-btn`).addEventListener('click', this.closeModalHandler);
        this.background.addEventListener('click', this.closeModalHandler);
    }



    addButtonHandler = () => {
        this.thisModalVisible = true;
        this.modal.classList.toggle('is-active');
    }


    closeModalHandler = () => {
        if (this.thisModalVisible) {
            this.modal.classList.toggle('is-active');
            this.thisModalVisible = false;
        }
    }

}
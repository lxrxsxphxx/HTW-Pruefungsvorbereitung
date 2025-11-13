<template>
    <div id="index-cards-entry-body">
        <div id="index-cards-entry-header">
            Karteikarten-Lernset erstellen
        </div>

        <div id="index-cards-entry-main">
            <div id="input">
                <div id="input-container">
                    <div>
                        <label for="card_set_name">Name des Lernsets:</label>
                        <input type="text" id="card_set_name" name="card_set_name" class="input-field" ref="card_set_name_input"><br>
                    </div>
                    <hr style="border: 0;">
                    <div id="error-message"></div>
                    <div>
                        <label for="front">Vorderseite:</label>
                        <input type="text" id="front" name="front" class="input-field" ref="front_input"><br>
                    </div>
                    <br>

                    <div id="back-container" class="answer-container">
                        <label for="back">Rückseite:</label>
                        <input type="text" id="back" name="back" class="input-field" ref="back_input"><br>
                    </div>
                    <br>
                </div>

                <div id="control-button-container">
                    <button class="control-button" id="add_card">Karte hinzufügen</button>
                    <button class="control-button" id="save_card_set">Lernset speichern</button>
                    <button class="control-button" id="cancel">Abbrechen</button>
                </div>

                <div id="cancel-popup" ref="cancel_popup">
                    <div id="cancel-popup-text">
                        <div style="margin-bottom: 1em;">Achtung, alle Fragen werden gelöscht.</div><div>Wirklich Abbrechen?</div>
                    </div>
                    <div id="cancel_button_container">
                        <button id="commit_cancel" class="cancel_option" ref="commit_cancel">Ja</button>
                        <button id="cancel_cancel" class="cancel_option" ref="cancel_cancel">Nein</button>
                    </div>
                </div>
            </div>

            <aside id="aside">
                <!--Hier werden die eingegebenen Fragen stehen-->
                <h3>Eingegebene Fragen:<br/></h3>
                <!--div class="entered_card" v-for="(card, index) in entered_cards" :key="index">
                    <div class="card_text" v-text="(index+1) + ': ' + card"></div>
                    <button class="delete_card" @click="v.deletecard(index)">löschen</button>
                    <button class="edit_card" @click="v.editcard(index)">bearbeiten</button>
                </div-->
            </aside>
        </div>
    </div>
</template>


<style scoped>
/* @import '@assets/karteikarten-erstellen.css'; */

:root {
    --dark-background: #444444;
    --dark-popup: #8d4000;
    --dark-menu: #cd5c00;
    --dark-menu-hover: #e58435;
    --dark-menu-active: #e3761d;
    --dark-button: #666666;
    --dark-button-hover: #585858;
    --dark-button-active: #555555;
    --dark-aside: #555555;
    --dark-input: var(--dark-aside);
    --dark-text-color: white;
    --dark-red: #ad0a0a;
    --dark-green: #269200;

    --light-background: rgba(249, 155, 32, 0.308);
    --light-popup: orange;
    --light-menu: orange;
    --light-menu-hover: #ffbb61;
    --light-menu-active: #fda633;
    --light-button: white;
    --light-button-hover: #fffbf4;
    --light-button-active: #fdc781;
    --light-aside: #ffaa00cc;
    --light-input: white;
    --light-text-color: black;
    --light-h-text-color: orange;
    --light-red: rgb(255, 42, 0);
    --light-green: rgb(124, 232, 0);
}

#index-cards-entry-body {
    color: var(--light-text-color);
}

button {
    font-size: 1em;
    color: var(--light-text-color);
    background-color: var(--light-button);

    border: none;
    border-radius: 0.25em;
}
button:hover {background-color: var(--light-button-hover);}
button:active {background-color: var(--light-button-active);}

label {
    padding-right: 1em;
}

#index-cards-entry-main {
    display: flex;
    flex-direction: row;
}

#input {
    order: 1;
    padding: 0.5em;
    padding-top: 1em;
    padding-bottom: 1em;
    display: flex;
    flex-direction: column;
    flex: 2 2 0%;
}

#aside {
    background-color: var(--light-aside);
    order: 2;
    flex: 1 1 0%;
    max-width: calc(33.33% - 0.5em - 8px);
}


#cancel-popup {
    display: none;
}

</style>
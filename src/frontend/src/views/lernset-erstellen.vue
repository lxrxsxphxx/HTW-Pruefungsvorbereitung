<template>
    <div id="learning-set-choice-body">
        <div id="learning-set-choice-header">
            <h1>Lernmodus zum erstellen auswählen</h1>
            
        </div>

        <div id="learning-set-choice-choice">
            <div>
                <RouterLink v-slot="{navigate, isActive}" to="/erstellen/karteikarten" custom>
                    <button id="choice-karteikarten" @click="navigate" :class="{active: isActive}">
                        Karteikarten
                    </button>
                </RouterLink>
            </div>
            <div>
                <RouterLink v-slot="{navigate, isActive}" to="/erstellen/multiplechoice" custom>
                    <button id="choice-multiplechoice" @click="navigate" :class="{active: isActive}">
                        Multiple Choice Quiz
                    </button>
                </RouterLink>
            </div>
        </div>
        
    </div>
</template>

<style scoped>
/* @import '@assets/lernset-erstellen.css'; */

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

#learning-set-choice-body {
    font-family: Arial, Helvetica, sans-serif;
    margin: 0 auto;
    padding: 0 20px;
}


button {
    font-size: 1em;
    background-color: var(--light-button);
    color: var(--light-text-color);
    overflow: hidden;
    text-overflow: ellipsis;

    padding: 0.5em;
    border: 0;
    border-radius: 0.5em;
}

#learning-set-choice-header {
    background-color: var(--light-background);
    border-radius: 10px;
    padding: 30px 40px;
    text-align: center;
    margin-bottom: 20px;
}

#learning-set-choice-header > h1{
    margin-top: -5px;
    color: #ec852c;
    font-size: 48px;
    font-weight: bold;
    /* margin-bottom: 30px; */
    text-align: center;
}

#learning-set-choice-choice {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 20px;
    background: transparent;
}

#learning-set-choice-choice > div {
    flex: 1;
    background: transparent;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    min-height: 280px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

#learning-set-choice-choice button {
    font-size: 32px;
    font-weight: bold;
    color: var(--light-h-text-color);
    border: none;
    padding: 0;
    margin: 0;
    cursor: pointer;
    width: 100%;
    height: 100%;
    max-width: 250px;
    margin-bottom: 10px;
    border-radius: 10px;

    transition: transform 0.2s ease;
}
    
#learning-set-choice-choice button:hover {
    transform: scale(1.20);
}


</style>
const HTMLTAG = {
    DIV: 'div',
    BUTTON: 'button',
    DIALOG: 'dialog',
    INPUT: 'input',
    LABEL: 'label',
    SELECT: 'select',
    OPTION: 'option',
    BR: 'br',
    IMG: 'img',
    SPAN: 'span',
    H3: 'h3',
}

const EVENT = {
    CLICK: 'click',
    ONCLICK: 'onclick',
}

const ATTRI = {
    ID: 'id',
    CLASS: 'class',
    MAXLEN: 'maxlength',
    FOR: 'for',
    NAME: 'name',
    SRC: 'src',
    TYPE: 'type',
    MAX: 'max',
    MIN: 'min',
    PLACEHOLDER: 'placeholder',
    STYLE: 'style',
    VALUE: 'value'
}

const FCSCLASS = {
    PLAYER: 'player',
    HORIZONTALPROFILE: 'horizontal-profile',
    PLAYERHEADPICTUREHORI: 'player-head-picture-horizontal',
    PLAYERHORIZONTALHOLDER: 'player-horizontal-holder',
    PLAYERNAMEHORI: 'player-name-horizontal',
    PLAYERBALANCEHORI: 'player-balance-horizontal',
    VERTICALPROFILE:'vertical-profile',
    PLAYERHEADPICTUREVER: 'player-head-picture-vertical',
    PLAYERNAMEVER: 'player-name-vertical',
    PLAYERBALANCEVER: 'player-balance-vertical',
    PLAYERHEADPICTURE: 'player-head-picture',
    CARDCONTAINER: 'card-container',
    CONTROLBUTTON: 'control-button',
    CONTROLBUTTONCONTAINER: 'control-button-container',
    MAINCONTAINER: 'main-container',
    ADDPLAYERDIALOG: 'add-player-dialog',
    ADDPLAYERBUTTON: 'add-player-button',
    DIALOGYESBUTTON: 'dialog-yes-button',
    DIALOGNOBUTTON: 'dialog-no-button',
    DIALOGDELETEBUTTON: 'dialog-delete-button',
    ROOTCONTAINER: 'root-container',
    CARDPILE: 'card-pile',
    DUPLICATECARDPILE: 'duplicate-card-pile',
    BEGINBUTTON: 'begin-button',
    ADDPLAYERDIALOGNAMEINPUT: 'add-player-dialog-name-input',
    ADDPLAYERDIALOGAGENTSELECTION: 'add-player-dialog-agent-selection',
    ADDPLAYERDIALOGAGENTNUMITERATION: 'add-player-dialog-num-iteration',
    ADDCHIPINPUT: 'add-chip-input',
    INFORMATIONPANEL: 'information-panel',
    MAXCHIPBOX: 'max-chip-box',
    TOTALCHIPBOX: 'total-chip-box',
    CURRENTCHIPBOX: 'current-chip-box',
    TURN: 'turn',
    FINALRESULTDIALOG: 'final-result-dialog',
    FINALRESULTTITLE: 'final-result-title',
    FINALRESULTCONTAINER: 'final-result-container',
    FINALRESULTPANEL: 'final-result-panel',
    FINALRESULTPLAYERINFO: 'final-result-player-information',
    FINALRESULTPLAYERPIC: 'final-result-player-pic',
    FINALRESULTPLAYERNAME: 'final-result-player-name',
    FINALRESULTPLAYERCARDTYPE: 'final-result-card-type',
    FINALRESULTCARDHOLDER: 'final-result-card-holder',
    FINALRESULTCARDHOLDER1: 'final-result-card-holder-1',
    FINALRESULTCARDHOLDER2: 'final-result-card-holder-2',
    FINALRESULTCARDHOLDER3: 'final-result-card-holder-3',
    FINALRESULTCARDHOLDER4: 'final-result-card-holder-4',
    FINALRESULTCARDHOLDER5: 'final-result-card-holder-5',
    FINALRESULTBUTTONCONTAINER: 'final-result-dialog-button-container',
    FINALRESULTBUTTON: 'final-result-dialog-button',
    FINALRESULTCARDTYPERESULT: 'final-result-card-type-result',
}

const FCSMSG = {
    INIT: 'init',
    LOADPLAYER: 'load-player',
    ADDPLAYER: 'add-player',
    DELETEPLAYER: 'delete-player',
    BEGIN: "begin",
    PLAYERNEXT: 'player-next',
    PLAYERGIVEUP: 'player-give-up',
    PLAYERFOLLOW: 'player-follow',
    PLAYERADD: 'player-add',
    PROCESSPLAYEROPTION: 'process-player-option',
    REPEATROUND: 'repeat-round',
    NEXTROUND: 'next-round',
    GETWINNER: 'get-winner'
}

const FCSCALLBACK = {
    HANDLEADDPLAYER: 'handleAddPlayer',
    HANDLEDELETEPLAYER: 'handleDeletePlayer',
    HANDLEDELETEHUMANPLAYER: 'handleDeleteHumanPlayer',
    HANDLEPLAYEROPTION: 'handlePlayerOption',
    HANDLERESETGAME: 'handleResetGame'
}

const FCSAGENTTYPE = ["MCTS Agent", "Uniform Agent", "Random Agent"]
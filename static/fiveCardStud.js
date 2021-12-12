
players = [0, 0, 0, 0, 0, 0]
player = null // the game state
removeHumanPlayer = false

$(document).ready(function () {
    init()
    // setup(players)
    // addButton()
    // showDialog()
})

function init() {
    send_message(FCSMSG.INIT, [], function (result) {
        console.log(result)
        player = result.game
        players = player.players
        setup(players)
    })
}

function loadPlayer() {
    send_message(FCSMSG.LOADPLAYER, [], function (result) {
        console.log(result)
        player = result
        players = player.showhand.players
        setup(players)
    })
}

function setup(players) {
    let con = document.getElementById(FCSCLASS.MAINCONTAINER)
    removeAllChildren(con)
    addPlayer(players)
    addPlayerButton(players)
    setupAddPlayerEventHandler()
    setupRemoveHumanPlayerHandler()
    // addCard(players)
    addCardPile()
    addInformationPanel(false, player)
    addBeginButton()
}

function firstStart(newPlayer) {
    let con = document.getElementById(FCSCLASS.MAINCONTAINER)
    removeAllChildren(con)
    payEnterTicket(newPlayer)
    addPlayer(players)
    addCard(newPlayer.showhand.players)
    addCardPile()
    addInformationPanel(true, newPlayer)
    let newPlayers = newPlayer.showhand.players
    let alivePlayer = getAlivePlayer(false, newPlayer)
    let j = 0
    let interval2 = setInterval(function () {
        if(j > 0)
            restoreHighlightPlayer(newPlayers[alivePlayer[j-1]], alivePlayer[j-1])
        highlightPlayer(newPlayers[alivePlayer[j]], alivePlayer[j])
        updateInformationPanel(newPlayers[alivePlayer[j]], players[alivePlayer[j]])
        updatePlayerInformation(newPlayers[alivePlayer[j]], alivePlayer[j])
        updatePlayerDecision(newPlayers[alivePlayer[j]], alivePlayer[j])
        if(alivePlayer[j] === 4){
            player = newPlayer
            players = player.showhand.players
            addButton()
            clearInterval(interval2)
        }
        j++
    }, 900)

}

function payEnterTicket(newPlayer){
    for(let i = 0; i < players.length; i++){
        if(players[i] !== 0){
            players[i].chip = newPlayer.showhand.players[4].chip
        }
    }
}

function gameInProgress(beforePlayer, newPlayer, callback, afterPlayer) {
    let con = document.getElementById(FCSCLASS.MAINCONTAINER)
    // removeAllChildren(con)
    // addPlayer(players)
    // addCard(players)
    // addCardPile()
    // if(beforePlayer)
    //     addButton()
    simulateBotMove(beforePlayer, newPlayer, callback, afterPlayer)
}

function simulateBotMove(beforePlayer, newPlayer, callback, afterPlayer) {
    let newPlayers = newPlayer.showhand.players
    let alivePlayer = getAlivePlayer(afterPlayer, newPlayer)
    if(alivePlayer.length === 0){
        player = newPlayer
        players = player.showhand.players
        if(callback)
            callback()
    }
    else{
        let i = 0
        let interval = setInterval(function () {
            if(!addCardDynamically(newPlayers[alivePlayer[i]], alivePlayer[i])){
                i = alivePlayer.length-1
            }
            i++
            if(i === alivePlayer.length){
                clearInterval(interval)
            }
        }, 300)
        let j = 0
        let interval2 = setInterval(function () {
            if(i === alivePlayer.length && j < alivePlayer.length){
                if(j > 0)
                    restoreHighlightPlayer(newPlayers[alivePlayer[j-1]], alivePlayer[j-1])
                highlightPlayer(newPlayers[alivePlayer[j]], alivePlayer[j])
                updateInformationPanel(newPlayers[alivePlayer[j]], players[alivePlayer[j]])
                updatePlayerInformation(newPlayers[alivePlayer[j]], alivePlayer[j])
                updatePlayerDecision(newPlayers[alivePlayer[j]], alivePlayer[j])
                if(beforePlayer && alivePlayer[j] === 4){
                    player = newPlayer
                    players = player.showhand.players
                    addButton()
                    clearInterval(interval2)
                    if(callback)
                        callback()
                }
                else if(j === alivePlayer.length - 1){

                }
                j++
            }else if(j >= alivePlayer.length){
                if(j === alivePlayer.length + 1){
                    restoreHighlightPlayer(newPlayers[alivePlayer[alivePlayer.length - 1]], alivePlayer[alivePlayer.length - 1])
                    player = newPlayer
                    players = player.showhand.players
                    clearInterval(interval2)
                    if(callback)
                        callback()
                }
                j++
            }

        }, 900)

        console.log('hi')
    }
}

function getAlivePlayer(afterPlayer, player) {
    let alivePlayer = []
    let index = Number(player.showhand.firstPlayer)
    if(afterPlayer)
        index = 4
    for(let i = 0; i < players.length; i++){
        if(players[index] !== 0 && players[index].alive) {
            alivePlayer.push(index)
        }
        index = index === players.length-1 ? 0 : index + 1
        if(afterPlayer && index === Number(player.showhand.firstPlayer)) break
    }
    if(afterPlayer && alivePlayer[0] === 4){
        alivePlayer.reverse().pop()
        alivePlayer.reverse()
    }
    return alivePlayer
}

function addCardDynamically(newPlayer, index) {
    let cardHolder = document.getElementById("player-" + (index + 1) + "-card")
    let cardIndex = players[index].cards.length
    if(players[index].cards.length < newPlayer.cards.length){
        document.getElementById(FCSCLASS.DUPLICATECARDPILE).removeAttribute(ATTRI.CLASS)
        document.getElementById(FCSCLASS.DUPLICATECARDPILE).classList.add('distribute-card-'+(index+1))
        let card = cardHolder.childNodes[cardIndex]
        let cardImg = document.createElement(HTMLTAG.IMG)
        cardImg.setAttribute(ATTRI.SRC, "./static/card/" + newPlayer.cards[cardIndex] + ".png")
        card.appendChild(cardImg)
        return true
    }else{
        return false
    }
}

function updateInformationPanel(newPlayer, oldPlayer) {
    let current = document.getElementById(FCSCLASS.CURRENTCHIPBOX)
    let total = document.getElementById((FCSCLASS.TOTALCHIPBOX))
    if(Number(current.innerHTML) < newPlayer.chip){
        current.innerHTML = "" +newPlayer.chip
    }
    total.innerHTML = ""+ (Number(total.innerHTML) + (newPlayer.chip - oldPlayer.chip))
}

function updatePlayerInformation(newPlayer, index) {
    if(index !== 2){
        let balance = document.getElementById(FCSCLASS.PLAYERBALANCEHORI+'-'+(index+1))
        balance.innerHTML = "" + newPlayer.balance
    }else{
        let balance = document.getElementById(FCSCLASS.PLAYERBALANCEVER+'-'+(index+1))
        balance.innerHTML = "" + newPlayer.balance
    }
}

function updatePlayerDecision(newPlayer, index) {
    if(!newPlayer.alive){
        let cardHolder = document.getElementById("player-" + (index + 1) + "-card")
        for(let i = 0; i< newPlayer.cards.length; i++){
            cardHolder.childNodes[i].firstChild.setAttribute(ATTRI.SRC, "./static/card/100.png")
        }
    }
}

function highlightPlayer(newPlayer, index) {
    let p = document.getElementById(FCSCLASS.PLAYER + "-" + (index+1))
    p.classList.add(FCSCLASS.TURN)
}

function restoreHighlightPlayer(newPlayer, index) {
    let p = document.getElementById(FCSCLASS.PLAYER + "-" + (index+1))
    p.classList.remove(FCSCLASS.TURN)
}

function checkPlayerChip() {
    let chip = []
    for(let i = 0; i < players.length; i++){
        if(players[i] !== 0 && players[i].alive){
            chip.push(players[i].chip)
        }
    }
    return chip
}

function determineGameStatus() {
    let chip = checkPlayerChip()
    // only one player alive
    if(chip.length === 1){
        getWinner()
        return
    }
    let c = chip[0]
    let repeat = false
    for(let i = 1; i < chip.length; i++){
        if(chip[i] !== c){
            repeat = true;
        }
    }
    if(repeat){
        repeatRound()
    }else{
        nextRound()
    }
}

function getWinner() {
    send_message(FCSMSG.GETWINNER, [], function (result) {
        console.log(result)
        player = result
        players = result.showhand.players
        let chip = checkPlayerChip()
        if(chip.length === 1){
            loadPlayer()
        }else{
            showFinalResultDialog(players)
        }
    })
}

function repeatRound() {
    send_message(FCSMSG.REPEATROUND, [], function (result) {
        console.log(result)
        // player = result
        // players = player.showhand.players
        let chip = checkPlayerChip()
        if(chip.length === 1){
            getWinner()
        }else{
            if(players[4].alive && Math.max(...chip) === players[4].chip){
                gameInProgress(false, result, nextRound)
            }else if(players[4].alive){
                gameInProgress(true, result)
            }else{ // human player gives up
                gameInProgress(false, result, nextRound)
            }
        }
    })
}

function nextRound() {
    let max_card = 0
    for(let i = 0; i < players.length; i++){
        if(players[i] !== 0 && players[i].alive && players[i].cards.length > max_card){
            max_card = players[i].cards.length
        }
    }
    if(max_card === 5){
        getWinner()
    }else{
        send_message(FCSMSG.NEXTROUND, [], function (result) {
            console.log(result)
            // player = result
            // players = result.showhand.players
            let chip = checkPlayerChip()
            if(chip.length === 1){
                getWinner()
            }else{
                if(players[4].alive){
                    gameInProgress(true, result)
                }else{ // human player gives up
                    gameInProgress(false, result, determineGameStatus)
                }
            }
        })
    }
}

function send_message(command, args, successCallback) {
    $.ajax({
        type: 'POST',
        url: '/fcsmsg',
        data: JSON.stringify({"command":command, "args": args}),
        dataType: "json",
        success: successCallback,
        error:function () {

        }
    })
}

function addPlayer(players) {
    let container = document.getElementById(FCSCLASS.MAINCONTAINER)
    for(let i = 0; i < players.length; i++){
        if(players[i] !== 0 && i !== 3){
            // i !== 3 is meaningless beyond eliminating player 4, delete it if needed in the future
            container.appendChild(buildPlayer(i+1))
        }
    }
}

function addCard(players) {
    let container = document.getElementById(FCSCLASS.MAINCONTAINER)
    let i = 0
    let interval = setInterval(function () {
        console.log(i)
        if(players[i] !== 0 && i !== 3){
            document.getElementById(FCSCLASS.DUPLICATECARDPILE).removeAttribute(ATTRI.CLASS)
            document.getElementById(FCSCLASS.DUPLICATECARDPILE).classList.add('distribute-card-'+(i+1))
            // i !== 3 is meaningless beyond eliminating player 4, delete it if needed in the future
            container.appendChild(buildCard(i+1, players))
        }
        i++
        if(i === players.length)
            clearInterval(interval)
    }, 100)

}

function addButton(){
    let container = document.getElementById(FCSCLASS.MAINCONTAINER)
    container.appendChild(buildControlButton())
}

function addCardPile() {
    let container = document.getElementById(FCSCLASS.MAINCONTAINER)
    container.appendChild(buildCardPile())
    container.appendChild(buildDuplicateCardPile())
}

function addBeginButton() {
    let count = 0
    for(let i = 0; i < 6; i++){
        if(players[i] !== 0) count++
    }
    if(count > 1){
        let container = document.getElementById(FCSCLASS.MAINCONTAINER)
        container.appendChild(buildBeginButton())
    }
}

function addInformationPanel(begin, player) {
    let con = document.getElementById(FCSCLASS.MAINCONTAINER)
    con.appendChild(buildInformationPanel(begin, player))
}

function buildPlayer(player) {
    if(player === 3 || player === 4){
        return buildVerticalProfile(player)
    }else{
        return buildHorizontalProfile(player)
    }
}

function buildHorizontalProfile(player) {
    let p = document.createElement(HTMLTAG.DIV)
    p.setAttribute(ATTRI.ID, 'player-'+player)
    p.setAttribute(ATTRI.CLASS, FCSCLASS.HORIZONTALPROFILE +" " + FCSCLASS.PLAYER)
    let pic = document.createElement(HTMLTAG.DIV)
    pic.setAttribute(ATTRI.ID, FCSCLASS.PLAYERHEADPICTUREHORI+'-'+player)
    pic.setAttribute(ATTRI.CLASS, FCSCLASS.PLAYERHEADPICTUREHORI)
    let img = document.createElement(HTMLTAG.IMG)
    img.setAttribute(ATTRI.SRC, players[player-1].pic)
    img.setAttribute(ATTRI.CLASS, FCSCLASS.PLAYERHEADPICTURE)
    img.setAttribute(ATTRI.ID, FCSCLASS.PLAYERHEADPICTURE + '-' + player)
    pic.appendChild(img)

    let holder = document.createElement(HTMLTAG.DIV)
    holder.setAttribute(ATTRI.CLASS, FCSCLASS.PLAYERHORIZONTALHOLDER)
    let name = document.createElement(HTMLTAG.DIV)
    name.setAttribute(ATTRI.ID, FCSCLASS.PLAYERNAMEHORI+'-'+player)
    name.setAttribute(ATTRI.CLASS, FCSCLASS.PLAYERNAMEHORI)
    name.innerHTML = players[player-1].name
    let balance = document.createElement(HTMLTAG.DIV)
    balance.setAttribute(ATTRI.ID, FCSCLASS.PLAYERBALANCEHORI+'-'+player)
    balance.setAttribute(ATTRI.CLASS, FCSCLASS.PLAYERBALANCEHORI)
    balance.innerHTML = players[player-1].balance
    holder.appendChild(name)
    holder.appendChild(balance)

    p.appendChild(pic)
    p.appendChild(holder)
    return p
}

function buildVerticalProfile(player) {
    let p = document.createElement(HTMLTAG.DIV)
    p.setAttribute(ATTRI.ID, 'player-'+player)
    p.setAttribute(ATTRI.CLASS, FCSCLASS.VERTICALPROFILE +" " + FCSCLASS.PLAYER)
    let pic = document.createElement(HTMLTAG.DIV)
    pic.setAttribute(ATTRI.ID, FCSCLASS.PLAYERHEADPICTUREVER+'-'+player)
    pic.setAttribute(ATTRI.CLASS, FCSCLASS.PLAYERHEADPICTUREVER)
    let img = document.createElement(HTMLTAG.IMG)
    img.setAttribute(ATTRI.SRC, players[player-1].pic)
    img.setAttribute(ATTRI.CLASS, FCSCLASS.PLAYERHEADPICTURE)
    img.setAttribute(ATTRI.ID, FCSCLASS.PLAYERHEADPICTURE + '-' + player)
    pic.appendChild(img)

    let name = document.createElement(HTMLTAG.DIV)
    name.setAttribute(ATTRI.ID, FCSCLASS.PLAYERNAMEVER+'-'+player)
    name.setAttribute(ATTRI.CLASS, FCSCLASS.PLAYERNAMEVER)
    name.innerHTML = players[player-1].name
    let balance = document.createElement(HTMLTAG.DIV)
    balance.setAttribute(ATTRI.ID, FCSCLASS.PLAYERBALANCEVER+'-'+player)
    balance.setAttribute(ATTRI.CLASS, FCSCLASS.PLAYERBALANCEVER)
    balance.innerHTML = players[player-1].balance

    p.appendChild(pic)
    p.appendChild(name)
    p.appendChild(balance)
    return p
}

function addPlayerButton(players) {
    let container = document.getElementById(FCSCLASS.MAINCONTAINER)
    for(let i = 0; i < players.length; i++){
        if(players[i] === 0 && i !== 3){
            container.appendChild(buildAddPlayerButton(i+1))
        }
    }
}

function buildAddPlayerButton(player) {
    let p = document.createElement(HTMLTAG.DIV)
    p.setAttribute(ATTRI.ID, 'player-'+player)
    if(player === 3 || player === 4){
        p.setAttribute(ATTRI.CLASS, FCSCLASS.VERTICALPROFILE +" " + FCSCLASS.PLAYER)
    }else{
        p.setAttribute(ATTRI.CLASS, FCSCLASS.HORIZONTALPROFILE +" " + FCSCLASS.PLAYER)
    }
    let but = document.createElement(HTMLTAG.BUTTON)
    but.setAttribute(ATTRI.ID, FCSCLASS.ADDPLAYERBUTTON + '-' + player)
    but.setAttribute(ATTRI.CLASS, FCSCLASS.ADDPLAYERBUTTON)
    but.innerHTML = '+'
    p.appendChild(but)
    return p
}

function buildCard(player, players) {
    let con = document.createElement(HTMLTAG.DIV)
    con.setAttribute(ATTRI.ID, 'player-' + player + '-card')
    con.setAttribute(ATTRI.CLASS, FCSCLASS.CARDCONTAINER)
    for(let i = 1; i <= 5; i++){
        let card = document.createElement(HTMLTAG.DIV)
        card.setAttribute(ATTRI.CLASS, 'card-holder-' + i)
        if(i <= players[player-1].cards.length){
            let cardImg = document.createElement(HTMLTAG.IMG)
            cardImg.setAttribute(ATTRI.SRC, "./static/card/" + players[player-1].cards[i-1] + ".png")
            card.appendChild(cardImg)
        }
        con.appendChild(card)
    }
    return con
}

function buildControlButton() {
    let con = document.createElement(HTMLTAG.DIV)
    con.setAttribute(ATTRI.ID, FCSCLASS.CONTROLBUTTONCONTAINER)

    let repeat = player.showhand.repeat
    let balance = []
    let chip = []
    for(let i = 0; i < players.length; i++){
        if(players[i] !== 0) {
            balance.push(players[i].balance)
            chip.push(players[i].chip)
        }
    }
    let chipCap = Number(player.showhand.chipCap)
    let highestCap = Math.max(...chip)

    let tempa = ['弃牌', '过牌', '跟注', '加注']
    let bu = document.createElement(HTMLTAG.BUTTON)
    bu.setAttribute(ATTRI.CLASS, FCSCLASS.CONTROLBUTTON)
    setupCallback(bu, EVENT.ONCLICK, FCSCALLBACK.HANDLEPLAYEROPTION, [FCSMSG.PLAYERGIVEUP, 0] )
    bu.innerHTML = tempa[0]
    con.appendChild(bu)

    if(highestCap === players[4].chip){
        bu = document.createElement(HTMLTAG.BUTTON)
        bu.setAttribute(ATTRI.CLASS, FCSCLASS.CONTROLBUTTON)
        setupCallback(bu, EVENT.ONCLICK, FCSCALLBACK.HANDLEPLAYEROPTION, [FCSMSG.PLAYERNEXT, 0] )
        bu.innerHTML = tempa[1]
        if(!repeat)
            con.appendChild(bu)
    }else{
        bu = document.createElement(HTMLTAG.BUTTON)
        bu.setAttribute(ATTRI.CLASS, FCSCLASS.CONTROLBUTTON)
        setupCallback(bu, EVENT.ONCLICK, FCSCALLBACK.HANDLEPLAYEROPTION, [FCSMSG.PLAYERFOLLOW, 0] )
        bu.innerHTML = tempa[2]
        con.appendChild(bu)
    }

    con.appendChild(document.createElement(HTMLTAG.BR))
    bu = document.createElement(HTMLTAG.BUTTON)
    bu.setAttribute(ATTRI.CLASS, FCSCLASS.CONTROLBUTTON)
    bu.innerHTML = tempa[3]
    let input = document.createElement(HTMLTAG.INPUT)
    input.setAttribute(ATTRI.ID, FCSCLASS.ADDCHIPINPUT)
    input.setAttribute(ATTRI.TYPE, 'number')

    if(chipCap - highestCap >= 0 && !repeat){
        input.setAttribute(ATTRI.MAX, ''+ (chipCap - highestCap))
        input.setAttribute(ATTRI.MIN, '10')
        let placeholder = '10-' + (chipCap - highestCap)
        input.setAttribute(ATTRI.PLACEHOLDER, placeholder)
        setupCallback(bu, EVENT.ONCLICK, FCSCALLBACK.HANDLEPLAYEROPTION, [FCSMSG.PLAYERADD, 1, 10, chipCap - highestCap] )
        con.appendChild(bu)
        con.appendChild(input)
    }

    return con
}

function buildCardPile() {
    let con = document.createElement(HTMLTAG.DIV)
    con.setAttribute(ATTRI.ID, FCSCLASS.CARDPILE)
    let img = document.createElement(HTMLTAG.IMG)
    img.setAttribute(ATTRI.SRC, './static/card/100.png')
    con.appendChild(img)
    return con
}

function buildDuplicateCardPile() {
    let con = document.createElement(HTMLTAG.DIV)
    con.setAttribute(ATTRI.ID, FCSCLASS.DUPLICATECARDPILE)
    let img = document.createElement(HTMLTAG.IMG)
    img.setAttribute(ATTRI.SRC, './static/card/100.png')
    con.appendChild(img)
    return con
}

function buildBeginButton() {
    let bu = document.createElement(HTMLTAG.BUTTON)
    bu.setAttribute(ATTRI.ID, FCSCLASS.BEGINBUTTON)
    setupEventHandler(bu, EVENT.CLICK, handleBegin)
    bu.innerHTML = 'begin'
    return bu
}

function buildInformationPanel(begin, game) {
    let info = document.createElement(HTMLTAG.DIV)
    info.setAttribute(ATTRI.ID, FCSCLASS.INFORMATIONPANEL)
    let maxL = document.createElement(HTMLTAG.LABEL)
    let maxS = document.createElement(HTMLTAG.SPAN)
    maxL.innerHTML = "Max:"
    maxS.setAttribute(ATTRI.ID, FCSCLASS.MAXCHIPBOX)
    maxS.innerHTML = "" + game.maxChip
    info.appendChild(maxL)
    info.appendChild(maxS)
    if(begin){
        let totalL = document.createElement(HTMLTAG.LABEL)
        let totalS = document.createElement(HTMLTAG.SPAN)
        let chip = 0
        for(let i = 0; i < players.length; i++){
            if(players[i] !== 0){
                chip += game.players[4].chip
            }
        }
        totalL.innerHTML = "total:"
        totalS.setAttribute(ATTRI.ID, FCSCLASS.TOTALCHIPBOX)
        totalS.innerHTML = "" + chip
        let currentL = document.createElement(HTMLTAG.LABEL)
        let currentS = document.createElement(HTMLTAG.SPAN)
        currentL.innerHTML = "current:"
        currentS.setAttribute(ATTRI.ID, FCSCLASS.CURRENTCHIPBOX)
        currentS.innerHTML = "0"
        info.appendChild(document.createElement(HTMLTAG.BR))
        info.appendChild(totalL)
        info.appendChild(totalS)
        info.appendChild(document.createElement(HTMLTAG.BR))
        info.appendChild(currentL)
        info.appendChild(currentS)
    }
    return info
}

function showDialog(num) {
    let d = document.createElement(HTMLTAG.DIALOG)
    let nameL = document.createElement(HTMLTAG.LABEL)
    nameL.innerHTML = 'Name: '
    nameL.setAttribute(ATTRI.FOR, 'name')
    let nameI = document.createElement(HTMLTAG.INPUT)
    let numMap = [1, 2, 3, 0, 4, 5]
    nameI.value = "Player" + numMap[num-1]
    nameI.setAttribute(ATTRI.MAXLEN, 16)
    nameI.setAttribute(ATTRI.NAME, 'name')
    nameI.setAttribute(ATTRI.ID, FCSCLASS.ADDPLAYERDIALOGNAMEINPUT)

    let agentL = document.createElement(HTMLTAG.LABEL)
    agentL.innerHTML = 'Agent: '
    agentL.setAttribute(ATTRI.FOR, 'agent')
    let agentI = document.createElement(HTMLTAG.SELECT)
    agentI.setAttribute(ATTRI.NAME, 'agent')
    agentI.setAttribute(ATTRI.ID, FCSCLASS.ADDPLAYERDIALOGAGENTSELECTION)
    for (let i = 0; i < 3; i++){
        let agentV = document.createElement(HTMLTAG.OPTION);
        agentV.setAttribute(ATTRI.VALUE, "" + (i+1))
        agentV.innerHTML = FCSAGENTTYPE[i]
        agentI.appendChild(agentV)
    }

    let numIterationL = document.createElement(HTMLTAG.LABEL)
    numIterationL.innerHTML = 'MCTS Iteration: '
    numIterationL.setAttribute(ATTRI.FOR, 'iteration')
    let numIterationI = document.createElement(HTMLTAG.INPUT)
    numIterationI.value = "100"
    numIterationI.setAttribute(ATTRI.TYPE, 'number')
    numIterationI.setAttribute(ATTRI.MAX, '10000')
    numIterationI.setAttribute(ATTRI.MIN, '100')
    numIterationI.setAttribute(ATTRI.PLACEHOLDER, '100-10000')
    numIterationI.setAttribute(ATTRI.NAME, 'name')
    numIterationI.setAttribute(ATTRI.ID, FCSCLASS.ADDPLAYERDIALOGAGENTNUMITERATION)


    let br = () => {return document.createElement(HTMLTAG.BR)}
    // let selectL = document.createElement(HTMLTAG.LABEL)
    // selectL.innerHTML = 'IQ: '
    // let select = document.createElement(HTMLTAG.SELECT)
    // let tempa = ['low', 'medium', 'high']
    // for (let i = 0; i < 3; i++){
    //     let o = document.createElement(HTMLTAG.OPTION)
    //     o.innerHTML = tempa[i]
    //     select.appendChild(o)
    // }
    let yes = document.createElement(HTMLTAG.BUTTON)
    let no = document.createElement(HTMLTAG.BUTTON)
    let del = document.createElement(HTMLTAG.BUTTON)
    yes.setAttribute(ATTRI.ID, FCSCLASS.DIALOGYESBUTTON)
    yes.innerHTML = 'yes'
    setupCallback(yes, EVENT.ONCLICK, FCSCALLBACK.HANDLEADDPLAYER, [num])
    no.setAttribute(ATTRI.ID, FCSCLASS.DIALOGNOBUTTON)
    no.innerHTML = 'no'
    setupEventHandler(no, EVENT.CLICK, handleCloseDialog)
    del.setAttribute(ATTRI.CLASS, FCSCLASS.DIALOGDELETEBUTTON)
    del.innerHTML = 'delete'
    setupCallback(del, EVENT.ONCLICK, FCSCALLBACK.HANDLEDELETEPLAYER, [num])
    d.appendChild(nameL)
    d.appendChild(nameI)
    d.appendChild(br())
    d.appendChild(br())
    d.appendChild(agentL)
    d.appendChild(agentI)
    d.appendChild(br())
    d.appendChild(br())
    d.appendChild(numIterationL)
    d.appendChild(numIterationI)
    // d.appendChild(br())
    // d.appendChild(br())
    // d.appendChild(selectL)
    // d.appendChild(select)
    d.appendChild(br())
    d.appendChild(br())
    d.appendChild(yes)
    d.appendChild(no)
    if(players[num-1] !== 0) {
        d.appendChild(del)
    }
    d.setAttribute(ATTRI.ID, FCSCLASS.ADDPLAYERDIALOG)

    let root = document.getElementById(FCSCLASS.MAINCONTAINER)
    root.appendChild(d)
}

function showFinalResultDialog(players) {
    let d = document.createElement(HTMLTAG.DIALOG)
    d.setAttribute(ATTRI.ID, FCSCLASS.FINALRESULTDIALOG)
    let title = document.createElement(HTMLTAG.H3)
    title.innerHTML = "hi"
    title.setAttribute(ATTRI.ID, FCSCLASS.FINALRESULTTITLE)

    let resultContainer = document.createElement(HTMLTAG.DIV)
    resultContainer.setAttribute(ATTRI.ID, FCSCLASS.FINALRESULTCONTAINER)
    for(let i = 0; i <= players.length; i++){
        if(i === 3) continue
        let panel = document.createElement(HTMLTAG.DIV)
        panel.setAttribute(ATTRI.CLASS, FCSCLASS.FINALRESULTPANEL)

        let playerInfo = document.createElement(HTMLTAG.DIV)
        playerInfo.setAttribute(ATTRI.CLASS, FCSCLASS.FINALRESULTPLAYERINFO)
        let pic = document.createElement(HTMLTAG.DIV)
        pic.setAttribute(ATTRI.CLASS, FCSCLASS.FINALRESULTPLAYERPIC)
        let picimg = document.createElement(HTMLTAG.IMG)
        picimg.setAttribute(ATTRI.STYLE, "height: inherit")
        pic.appendChild(picimg)
        let name = document.createElement(HTMLTAG.DIV)
        name.setAttribute(ATTRI.CLASS, FCSCLASS.FINALRESULTPLAYERNAME)
        if(i !== players.length && players[i] !== 0){
            picimg.setAttribute(ATTRI.SRC, players[i].pic)
            name.innerHTML = players[i].name
        }
        playerInfo.appendChild(pic)
        playerInfo.appendChild(name)

        let cardPanel = document.createElement(HTMLTAG.DIV)
        cardPanel.setAttribute(ATTRI.CLASS, FCSCLASS.FINALRESULTPLAYERCARDTYPE)
        let cardHoldersList = [FCSCLASS.FINALRESULTCARDHOLDER1, FCSCLASS.FINALRESULTCARDHOLDER2,
        FCSCLASS.FINALRESULTCARDHOLDER3,FCSCLASS.FINALRESULTCARDHOLDER4,FCSCLASS.FINALRESULTCARDHOLDER5]
        for(let j = 1; j <= 5; j++){
            let cardHolder = document.createElement(HTMLTAG.DIV)
            cardHolder.classList.add(FCSCLASS.FINALRESULTCARDHOLDER, cardHoldersList[j-1] )
            if(i !== players.length && players[i] !== 0 && players[i].alive){
                let cardImg = document.createElement(HTMLTAG.IMG)
                cardImg.setAttribute(ATTRI.SRC, "./static/card/" + players[i].cards[j-1] + ".png")
                cardHolder.appendChild(cardImg)
            }else if(i !== players.length && players[i] !== 0 && !players[i].alive){
                let cardImg = document.createElement(HTMLTAG.IMG)
                cardImg.setAttribute(ATTRI.SRC, "./static/card/100.png")
                cardHolder.appendChild(cardImg)
                if(players[i].cards.length === j-1) break
            }
            cardPanel.appendChild(cardHolder)
        }
        panel.appendChild(playerInfo)
        panel.appendChild(cardPanel)
        if(i !== players.length && players[i] !== 0  && players[i].endType !== 0){
            let cardTypeResult = document.createElement(HTMLTAG.DIV)
            cardTypeResult.setAttribute(ATTRI.CLASS, FCSCLASS.FINALRESULTCARDTYPERESULT)
            cardTypeResult.innerHTML = players[i].endType
            if(i !== players.length && player.showhand.firstPlayer === i){
                cardTypeResult.classList.add("winner")
                panel.classList.add("turn")
            }
            panel.appendChild(cardTypeResult)
        }

        resultContainer.appendChild(panel)
    }
    let buttonContainer = document.createElement(HTMLTAG.DIV)
    buttonContainer.setAttribute(ATTRI.ID, FCSCLASS.FINALRESULTBUTTONCONTAINER)
    let but = document.createElement(HTMLTAG.BUTTON)
    but.setAttribute(ATTRI.ID, FCSCLASS.FINALRESULTBUTTON)
    but.innerHTML = "close"
    setupEventHandler(but, EVENT.CLICK, handleFinalResultDialogClose)
    buttonContainer.appendChild(but)

    d.appendChild(title)
    d.appendChild(resultContainer)
    d.appendChild(buttonContainer)

    let main = document.getElementById(FCSCLASS.MAINCONTAINER)
    main.appendChild(d)
}


function removeAllChildren(node) {
    if (!node)
        console.log("WHAT?");
    let child = node.firstElementChild;
    while (child) {
        child.remove();
        child = node.firstElementChild;
    }
}

function removeButton() {
    let but = document.getElementById(FCSCLASS.CONTROLBUTTONCONTAINER)
    if(but)
        but.remove()
}

function setupEventHandler(node, event, handler) {
    if(node)
        node.addEventListener(event, handler)
}

function removeEventHandler(node, event, handler) {
    if(node)
        node.removeEventListener(event, handler)
}

function setupCallback(element, elementCallbackName, callbackFunctionName, args) {
    let functionCallText = callbackFunctionName + "(";
    for (let i = 0; i < args.length; i++) {
        functionCallText += "'" + args[i] + "'";
        if (i < (args.length - 1)) {
            functionCallText += ", ";
        }
    }
    functionCallText += ")";
    element.setAttribute(elementCallbackName, functionCallText);
    return functionCallText;
}

function setupAddPlayerEventHandler() {
    for(let i = 1; i <= 6; i++){
        if(i !== 5 || removeHumanPlayer === true){ // or human agent is removed
            let p = document.getElementById(FCSCLASS.PLAYER + '-' + i)
            setupEventHandler(p, EVENT.CLICK, popUpDialog)
        }

    }
}

function setupRemoveHumanPlayerHandler() {
    let d = document.getElementById('remove-human-player');
    setupCallback(d, EVENT.ONCLICK, FCSCALLBACK.HANDLEDELETEHUMANPLAYER, []) // delete human player
}


function removeAddPlayerEventHandler() {
    for(let i = 1; i <= 6; i++){
        if(i !== 5){
            let p = document.getElementById(FCSCLASS.PLAYER + '-' + i)
            removeEventHandler(p, EVENT.CLICK, popUpDialog)
        }
    }
}

function popUpDialog(e) {
    let id = e.target.id
    let num = id.substring(id.length - 1)
    num = Number.parseInt(num)
    if(!Number.isNaN(num)){
        handleCloseDialog()
        showDialog(num)
    }
}

function handleCloseDialog() {
    let dia = document.getElementById(FCSCLASS.ADDPLAYERDIALOG)
    if(dia)
        dia.remove()
}

function handleAddPlayer(num) {
    let name = document.getElementById(FCSCLASS.ADDPLAYERDIALOGNAMEINPUT).value
    let agent = document.getElementById(FCSCLASS.ADDPLAYERDIALOGAGENTSELECTION).value
    let numIteration = document.getElementById(FCSCLASS.ADDPLAYERDIALOGAGENTNUMITERATION).value
    send_message(FCSMSG.ADDPLAYER,[num, name, agent, numIteration],function (result) {
        console.log(result)
        player = result.game
        players = player.players
        setup(players)
    })
    handleCloseDialog()
}

function handleDeletePlayer(num) {
    send_message(FCSMSG.DELETEPLAYER,[num],function (result) {
        console.log(result)
        player = result.game
        players = player.players
        setup(players)
    })
    handleCloseDialog()
}

function handleDeleteHumanPlayer() {
    if(removeHumanPlayer === false){
        send_message(FCSMSG.DELETEPLAYER,[5],function (result) {
            console.log(result)
            player = result.game
            players = player.players
            removeHumanPlayer = true
            setup(players)
        })
    }

}

function handleBegin() {
    send_message(FCSMSG.BEGIN, [], function (result) {
        console.log(result)
        firstStart(result)
    })
}

function handlePlayerOption(callbackName, arg, min, max) {
    let amount = 0
    if(arg === "1"){
        let input = document.getElementById(FCSCLASS.ADDCHIPINPUT)
        amount = Number(input.value)
        console.log(amount)
        if (!Number.isInteger(amount) || amount < Number(min) || amount > Number(max)){
            input.setAttribute(ATTRI.STYLE, "background:red;")
            return
        }
        input.setAttribute(ATTRI.STYLE, "")
    }
    removeButton()
    send_message(FCSMSG.PROCESSPLAYEROPTION, [callbackName, amount], function (result) {
        console.log(result)
        let newPlayers = result.showhand.players
        updateInformationPanel(newPlayers[4], players[4])
        updatePlayerInformation(newPlayers[4], 4)
        updatePlayerDecision(newPlayers[4], 4)
        restoreHighlightPlayer(newPlayers[4], 4)
        gameInProgress(false, result, determineGameStatus, true)
    })
}

function handleFinalResultDialogClose() {
    let d = document.getElementById(FCSCLASS.FINALRESULTDIALOG)
    if(d)
        d.remove()
    loadPlayer()
}
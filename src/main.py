from src.modules import *
from src.helpers import *
from src.functions import *
from . import GS_REPORT

count = 0

# this is where the table looping happens
def play(driver, gsreport, bet, betArea, allin=False, name=""):
    global count
    print('\n')
    waitElement(driver, 'lobby', 'main')
    waitElement(driver, 'in-game', 'botnav')
    createNew_sheet(driver)
    wait_If_Clickable(driver, 'category', bet)
    bet_areas = list(data(bet))
    elements = findElements(driver, 'lobby', 'table panel')

    for i in range(len(elements)):
        gameName = elements[i]
        
        if bet == 'dragontiger' and name not in gameName.text:
            continue 

        elif bet == 'baccarat' and i < 2:
            continue
        
        elif bet == 'three-cards' and name not in gameName.text:
            continue
        
        elif bet == 'sedie' and name not in gameName.text:
            continue
            
        elif bet == 'sicbo' and name not in gameName.text:
            continue

        elif bet == 'roulette' and name not in gameName.text:
            continue

        elif bet == 'bull bull' and name not in gameName.text:
            continue
        
        if allin:
            elements = reset_coins(driver, bet, 2191.78)
        else:
            elements = reset_coins(driver, bet, 10000)

        table = elements[i]

        customJS(driver, 'noFullScreen();')
        customJS(driver, 'scrollToTop();')
        driver.execute_script("arguments[0].scrollIntoView();", table)
        getPlayerBalance = findElement(driver, 'lobby', 'balance')
        userBalance = getPlayerBalance.text.strip()

        table.click()

        waitElement(driver, 'in-game', 'game')
        if betArea == 'All':
            for x in range(len(bet_areas)):
                betOn(driver, gsreport, bet, bet_areas[x])
        else:
            betOn(driver, gsreport, bet, betArea, allin, lobBalance=userBalance)

        wait_If_Clickable(driver, 'in-game', 'back')
        waitElement(driver, 'lobby', 'main')
        elements = findElements(driver, 'lobby', 'table panel')
        print('=' * 100)
    
# Main Test Case function for validation and assertions
def betOn(driver, gsreport, bet, betArea, allin=False, lobBalance=""):
    global count
    balance = []
    tableDealer = table_dealer(driver)
    waitElement(driver, 'in-game', 'timer')
    checkPlayerBalance(driver, bet, value=lobBalance, allin=allin, lobbyBal=True)
    currHistoryRow = openBetHistory(driver, bet, tableDealer)
    editChips(driver, 20)

    while True:
        money = findElement(driver, 'in-game', 'balance')
        balance.append(money.text)
        timer = findElement(driver, 'in-game', 'timer')

        if timer.text == 'CLOSED':
            waitPresence(driver, 'in-game', 'toast', text='Please Place Your Bet!')
            screenshot(driver, 'Please Place Your Bet', tableDealer[0], allin)
        else:
            try:
                timerInt = int(timer.text.strip())
            except ValueError:
                waitPresence(driver, 'in-game', 'toast', text='Please Place Your Bet!')

            if timerInt <= 5:
                waitPresence(driver, 'in-game', 'toast', text='Please Place Your Bet!')
            else:
                if timerInt >= 10:
                    if allin:
                        coins_allin(driver, bet, allin)
                    else:
                        wait_If_Clickable(driver, bet, betArea)
                        waitElementInvis(driver, 'in-game', 'toast')
                        wait_If_Clickable(driver, 'action', 'confirm')

                    waitPresence(driver, 'in-game','toast', text='No More Bets!', setTimeout=40)
                    remainingMoney = findElement(driver, 'in-game', 'balance')
                    preBalance = float(remainingMoney.text.replace(',',''))

                    screenshot(driver, 'No More Bets', tableDealer[0], allin)
                    waitElementInvis(driver, 'in-game', 'toast')
                    waitElement(driver, 'in-game', 'toast')
                    winner = findElement(driver, 'in-game', 'toast')
                    screenshot(driver, winner.text, tableDealer[0], allin)
                                            
                    # =================================================
                    # get game result text from digital message
                    board = findElements(driver, 'in-game', 'board-result')
                    lucky_odds = dict(data('lucky'))
                    lucky_result = 0.00
                    odds = []
                    for i in board:
                        board_result = i.text.split(' – ')[0]

                        if board_result in lucky_odds:
                            value = lucky_odds[board_result]
                            odds.append(value)
                            if len(odds) == 2:
                                if odds[0] > odds[1]:
                                    lucky_result = float(odds[0])
                                else:
                                    lucky_result = float(odds[1])
                            else:
                                lucky_result = float(value)

                    # =================================================
                    bets = findElement(driver, 'in-game', 'bets')
                    getBets = float(bets.text.replace(',',''))

                    # get balance after bet
                    wl = LoseOrWin(driver)
                    balance = float(remainingMoney.text.replace(',',''))
                    total = 0

                    # =================================================
                    # calculates the expected lose and win
                    if 'Lose: ' in wl:
                        loseAmount = float(wl.replace('Lose: ',''))
                        calcAmount = max(0, float(preBalance) + float(getBets) - float(loseAmount))

                        if allin:
                            screenshot(driver, 'Lose Balance', tableDealer[0], allin)
                        
                        message = debuggerMsg(tableDealer, f'Balance after losing {round(calcAmount, 2)} '\
                        f'Latest Balance {round(balance, 2)} - Expected: EQUAL')
                        assertion(message, f'{round(calcAmount, 2):.2f}', '==', f'{round(balance, 2):.2f}')
                        
                        if not allin:
                            driver.save_screenshot(f'screenshots/{"Lose Total"} {tableDealer[0]} {count}.png')

                        checkPlayerBalance(driver, bet)
                    else:
                        resultBal = float(wl.replace('Win: ',''))
                        total = preBalance + resultBal + getBets
                        placeBets = findElement(driver, 'in-game', 'bets')
                        cFloat = float(placeBets.text.replace(',',''))

                        # ====================================================
                        # calculate the odds player will receive after winning 
                        getOdds = findElement(driver, bet, betArea)
                        match = re.search(r'\b(\d+:\d+(\.\d+)?)\b', getOdds.text)

                        # special case for Three-cards odds
                        if not allin:
                            if bet != 'sicbo' and bet != 'roulette':
                                if bet == 'three-cards' and betArea == 'Lucky':
                                    count += 1
                                    calc_odds = lucky_result * cFloat
                                    message = debuggerMsg(tableDealer, f'Odds won: {calc_odds} & '\
                                    f'Balance Result: {resultBal} - Expected: EQUAL')
                                    assertion(message, calc_odds, '==', resultBal)
                                else:
                                    if match:
                                        val = match.group(1)
                                        odds = float(val.split(':', 1)[1])
                                        winOdds = cFloat * odds
                                        if resultBal != 0.00:
                                            count += 1
                                            message = debuggerMsg(tableDealer, f'Odds won: {winOdds} & '\
                                            f'Balance Result: {resultBal} - Expected: EQUAL')
                                            assertion(message, winOdds, '==', resultBal)
                                    else:
                                        print("Odds not found")
                                
                        if allin:
                            screenshot(driver, 'Win Balance', tableDealer[0], allin)
                    
                        driver.save_screenshot(f'screenshots/{"Win Total"} {tableDealer[0]} {count}.png')
                        # checks if the total winnings + the current balance is
                        # equal to the latest balance
                        message = debuggerMsg(tableDealer, f'Win balance {round(total, 2)} & '\
                        f'Latest balance {balance} - Expected: EQUAL')
                        assertion(message, f'{round(total, 2)}', '==', f'{round(balance, 2)}')
                        checkPlayerBalance(driver, bet)

                    if allin:
                        waitPresence(driver, 'in-game','toast', text='Please Place Your Bet!', setTimeout=5)
                        waitElementInvis(driver, 'in-game','toast')
                        verifiy_newRound(driver, bet, tableDealer)
                        
                        if bet == 'roulette':
                            check_raceTracker(driver, tableDealer)
                            
                        # Place a bet when the timer is CLOSED verification
                        summary(driver, bet, tableDealer)
                        waitPresence(driver, 'in-game','toast', text='No More Bets!', setTimeout=40)
                        if timer.text == 'CLOSED':
                            bet_areas = list(data(bet))
                            setRange = 10 if bet in ['sicbo', 'roulette'] else len(bet_areas)
                            ExceptionMessage = []
                            for i in range(setRange):
                                try:
                                    wait_If_Clickable(driver, bet, bet_areas[i])
                                except Exception as e:
                                    ExceptionMessage.append(str(e))

                            screenshot(driver, 'Bet on CLOSED', tableDealer[0], allin)
                            message = debuggerMsg(tableDealer, f'Failed Clicks {len(ExceptionMessage)} '\
                            f'Bet area length {setRange} - Expected: EQUAL')
                            assertion(message, len(ExceptionMessage), '==', setRange)
                            
                        payrates_odds(driver, bet, tableDealer, allin) # check if bet limit payrate are equal
                        openBetHistory(driver, bet, tableDealer, currHistoryRow, updates=True)
                        if gsreport:
                            sendReport(GS_REPORT, bet, tableDealer)
                    break

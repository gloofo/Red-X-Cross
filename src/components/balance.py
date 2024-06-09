import random

from src.api.services import Services
from src.helpers.helpers import Helpers
from src.utils.utils import Utilities

class Balance(Helpers):

    def __init__(self) -> None:
        super().__init__()
        self.service = Services()
        self.utils = Utilities()

    def update_player_balance(self, driver, game):
        """
        Update the user's balance, perform necessary balance adjustments, and navigate to the specified game lobby.

        params:
        `driver` (WebDriver): The Selenium WebDriver instance.
        `game` (str): The name or category of the game lobby to navigate to.

        : This function generates a random amount between $2000.00 and $10000.00 and converts it to a string
        : with two decimal places. It then adds this amount to the user's balance using the addBalance function
        : with the appropriate environment configurations for adding and deducting balance.
        : After updating the balance, the function navigates the WebDriver instance to the URL obtained from
        : getURL() and waits for the 'lobby' and 'main' elements to be available before proceeding.
        : It then waits for the specified game category to become clickable and retrieves a list of WebElement
        : objects representing the game tables available in the lobby.
        """

        amount = round(random.uniform(2000.00, 10000.00), 2)
        amount_str = f'{amount:.2f}'
        getBalance = self.service.POST_ADD_BALANCE(self.utils.env('add'), amount_str)
        self.service.POST_ADD_BALANCE(self.utils.env('deduc'), amount=getBalance)
        self.service.POST_ADD_BALANCE(self.utils.env('add'), amount)
        driver.get(self.service.GET_URL())
        self.wait_element(driver, 'lobby', 'main')
        self.wait_clickable(driver, 'category', game)
        elements = self.search_elements(driver, 'lobby', 'table panel')
        return elements
    
    def player_balance_assertion(self, driver, game, value="", lobbyBalance=False):
        """
        check the player's balance in the specified game lobby or during gameplay.

        params:
        `driver` (webdriver): the selenium webdriver instance.
        `game` (str): the name of the game or game category.
        `value` (str, optional): the expected balance value. default is an empty string.
        `lobbybal` (bool, optional): whether to check the balance in the lobby. default is false.

        : if the game is not 'roulette', it extracts the table and dealer information using the `table_dealer` function,
        : and locates the player's balance and game balance elements using the `findelement` function.
        : if `lobbybal` is true, it compares the lobby balance (`coins.text`) with the expected value.
        : otherwise, it compares the top balance (`coins.text`) with the bottom balance (`playerbalance.text`).
        """

        if game != 'roulette':
            tableDealer = self.table_dealer(driver)
            coins = self.search_element(driver, 'in-game', 'balance')
            playerBalance = self.search_element(driver, 'in-game', 'playerBalance')

            if lobbyBalance:
                message = self.utils.debuggerMsg(tableDealer, f'Lobby {value} & '\
                f'In-game Balance {coins.text} - Expected: EQUAL')
                self.utils.assertion(message, value, '==', coins.text.strip())

            message = self.utils.debuggerMsg(tableDealer, f'Top {coins.text} & '\
            f'Bottom balance {playerBalance.text} - Expected: EQUAL')
            self.utils.assertion(message, coins.text, '==', playerBalance.text)
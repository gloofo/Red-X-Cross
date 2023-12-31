from src.modules import *
from src.api import *
from src.helper import *

def pytest_addoption(parser):
    parser.addoption("--device", action="store", default=None)

@pytest.fixture(scope='session')
def device(request):
    return request.config.getoption("device")

@pytest.fixture(scope='session')
def driver(device):
    #setup
    deleteScreenshots()
    URL = play()
    option = Options()
    option.add_argument("--hide-scrollbars")
    devices = phone()['deviceName']
    getRandom = random.choice(devices)

    if device:
        option.add_experimental_option("mobileEmulation", {"deviceName": device})
    else:
        option.add_experimental_option("mobileEmulation", {"deviceName": getRandom})

    driver = webdriver.Chrome(options=option)
    driver.get(URL)
    #closeBanner(driver)
    yield driver
    #teardown
    driver.close()
    driver.quit()

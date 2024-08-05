import logging

import pytest


@pytest.fixture(autouse=True, scope='session')
def configure_logging():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler()])

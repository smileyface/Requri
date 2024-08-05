from UI.main_app import MainApplication
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])


def main():
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    main()

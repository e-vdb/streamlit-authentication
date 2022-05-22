from dotenv import load_dotenv
import os
from authentication import StreamlitAuthenticator
import streamlit as st
from streamlit import cli as stcli
import sys

load_dotenv()


class App:
    def __init__(self):
        self.user = None
        self.authenticator = StreamlitAuthenticator(username=os.getenv('USERNAME'), password=os.getenv('PASSWORD'),
                                                    host=os.getenv('HOST'), port=os.getenv('PORT'),
                                                    database=os.getenv('DATABASE'))

    def authentication(self):
        self.authenticator.authentication(main_app_fct_to_show=self.show, app_name='demo')

    def show(self):
        st.markdown("Successful connection to the streamlit web app.")
        self.user = st.session_state['name']
        st.write(self.user)


def main():
    front = App()
    front.authentication()


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())

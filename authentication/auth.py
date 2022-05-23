from authentication import UsernameDatabase
from passlib.hash import pbkdf2_sha256
import streamlit as st


class StreamlitAuthenticator:
    def __init__(self, username, password, host, port, database):
        self.user_db = UsernameDatabase(username=username, password=password, host=host, port=port, database=database)
        self.df_users = self.read_db()
        self.allowed_users = self.df_users['username'].tolist()
        self.authenticated = False
        self.form_container = st.empty()

    def read_db(self):
        return self.user_db.return_table_as_df()

    def authentication(self, main_app_fct_to_show, app_name: str):
        if not self.authenticated:
            with st.sidebar.form("Connection", clear_on_submit=True):
                username = st.text_input(label="Enter your name")
                password = st.text_input(label="Enter your password", type="password")

                if st.form_submit_button("Log in"):
                    if username in self.allowed_users:
                        app_access = self.df_users.loc[self.df_users['username'] == username, 'app_access'].values[0]
                        app_access = app_access.split(' ')
                        if app_name in app_access or 'all' in app_access:
                            hashed_password = self.df_users.loc[self.df_users['username'] == username]["password"].values[0]
                            if pbkdf2_sha256.verify(password, hashed_password):
                                st.success("You are correctly logged in.")
                                if 'name' not in st.session_state:
                                    st.session_state['name'] = username
                                    self.authenticated = True
                            else:
                                st.error("Wrong password.")
                        else:
                            st.error("This user is not allowed to access to this app.")
                    else:
                        st.error("This user is not allowed to access to this app.")
        if 'name' in st.session_state:
            main_app_fct_to_show()

        else:
            st.info("Log in to access to the app.")

    def log_out(self):
        if 'name' in st.session_state:
            del st.session_state['name']
            self.authenticated = False


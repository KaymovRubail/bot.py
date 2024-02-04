import sqlite3
from database import query

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('db.sqlite3')
        self.cursor = self.connection.cursor()
    def create_table(self):
        if self.connection:
            print("Db  connected successfully")
        self.connection.execute(query.CREATE_USER_TABLE)
        self.connection.execute(query.CREATE_ANSWER_TABLE)
        self.connection.execute(query.CREATE_BAN_TABLE)
        self.connection.execute(query.CREATE_REGISTER_TABLE)
        self.connection.execute(query.CREATE_LIKE_DISLIKE_TABLE)
        self.connection.execute(query.CREATE_USER_COMLAIN_TABLE)
        self.connection.execute(query.CREATE_FEEDBACK_PROBLEM_TABLE)
        self.connection.execute(query.CREATE_CHECK_TABLE)
        try:
            self.connection.execute(query.ALTER_R_USER_TABLE)
            self.connection.execute(query.ALTER_B_USER_TABLE)
        except sqlite3.OperationalError:
            pass
        self.connection.execute(query.CREATE_REFERRAL_TABLE)
        self.connection.execute(query.CREAT_TRANSACTIONS_TABLE)
        self.connection.execute(query.CREATE_ENGLISH_LEVEL_LEARN_TABLE)
        self.connection.execute(query.CREATE_FAVOURITE_ENGLISH_LEVEL_LEARN_TABLE)
        self.connection.execute(query.CREATE_ENGLISH_LEVEL_LEARN_TABLE_B2)
        self.connection.execute(query.CREATE_ENGLISH_LEVEL_LEARN_TABLE_B1)
        self.connection.execute(query.CREATE_ENGLISH_LEVEL_LEARN_TABLE_A2)
        self.connection.execute(query.CREATE_ENGLISH_LEVEL_LEARN_TABLE_A1)
        self.connection.execute(query.CREATE_ADMIN_RATING_TABLE)
        self.connection.commit()
    def insert_user(self,telegram_id,username,first_name,last_name):
        self.cursor.execute(query.INSERT_USER_TABLE, (None,telegram_id,username,first_name,last_name,None,None))
        self.connection.commit()
    def insert_answer(self,telegram_id,name,type,model,exp):
        self.cursor.execute(query.INSERT_ANSWER_TABLE, (None,telegram_id,name,type,model,exp))
        self.connection.commit()
    def inseert_ban(self,tg_id,first_name):
        self.cursor.execute(query.INSERT_BAN_TABLE, (None,tg_id,first_name,0))
        self.connection.commit()
    def select_count_bun_table(self,tg_id):
        self.cursor.execute(query.SELECT_BAN_TABLE_COUNT, (tg_id,))
        return self.cursor.fetchone()
    def update_count_bun_table(self,tg_id):
        self.cursor.execute(query.UPDATE_BAN_TABLE_COUNT,(tg_id,))
        self.connection.commit()
    def delete_user(self,tg_id):
        self.cursor.execute(query.DELETE_USER,(tg_id,))
        self.connection.commit()
    def select_user(self):
        self.cursor.execute(query.SELECT_FROM_USER_TABLE)
        rows = self.cursor.fetchall()
        return rows
    def seletc_from_ban(self):
        self.cursor.execute(query.SELECT_USER_FROM_BAN)
        rows = self.cursor.fetchall()
        return rows
    def select_user_answer(self,tg_id):
        self.cursor.execute(query.SELECT_USER_FROM_ANSWER,(tg_id,))
        row = self.cursor.fetchone()
        return row
    def select_all_user_answer(self):
        self.cursor.execute(query.SELECT_ANSWER_TABLE)
        rows = self.cursor.fetchall()
        return rows
    def update_user_answer(self,transport_type,model,experience,telegram_user_id):
        self.cursor.execute(query.UPDATE_ANSWER_TABLE,(transport_type,model,experience,telegram_user_id))
        self.connection.commit()
    def select_all_id_answer(self):
        self.cursor.execute(query.SELECT_ALL_ID_ANSWER)
        rows = self.cursor.fetchall()
        return rows
    def insert_info(self,tg,name,bio,age,zodiac,gender,color,photo):
        self.cursor.execute(query.INSERT_REGISTER_TABLE,(None,tg,name,bio,age,zodiac,gender,color,photo))
        self.connection.commit()
    def select_id_info(self,tg):
        self.cursor.execute(query.SELECT_REGISTER_TABLE,(tg,))
        rows = self.cursor.fetchone()
        return rows

    def select_info_registr_table(self,tg_id):
        self.cursor.execute(query.SELECT_INFO_REGISTER_TABLE,(tg_id,))
        row = self.cursor.fetchone()
        return row
    def select_all_registr(self,tg_id):
        self.cursor.execute(query.FILTER_LEFT_JOIN,(tg_id,tg_id))
        rows = self.cursor.fetchall()
        return rows
    def delete_info_registr_table(self,tg_id):
        self.cursor.execute(query.DELETE_REGISTER_TABLE,(tg_id,))
        self.connection.commit()
    def insert_like_dislike_table(self,user,liker,what):
        self.cursor.execute(query.INSERT_LIKE_DISLIKE_TABLE,(None,user,liker,what))
        self.connection.commit()
    def insert_complain_table(self,complainer_id,user_name,first_name,badman_id,reason):
        self.cursor.execute(query.INSERT_USER_COMLAIN_TABLE,(None,complainer_id,user_name,first_name,badman_id,reason,1))
        self.connection.commit()
    def update_complain_table(self,reason,badman_id):
        self.cursor.execute(query.UPDATE_USER_COMLAIN_TABLE,(reason,badman_id))
        self.connection.commit()

    def update_count_complain_table(self,badman_id):
        self.cursor.execute(query.UPDATE_COUNT_USER_COMPLAIN_TABLE,(badman_id,))
        self.connection.commit()
    def select_count_complain_table(self,bad_id):
        self.cursor.execute(query.SELECT_COUNT_COMLAIN_TABLE,(bad_id,))
        row=self.cursor.fetchone()
        return row
    def select_username_complain_table(self):
        self.cursor.execute(query.SELECT_USERNAME_FIRST_NAME_COMLAIN_TABLE)
        row=self.cursor.fetchall()
        return row
    def insert_feedback_problem_table(self,tg_id,idea,problem):
        self.cursor.execute(query.INSERT_FEEDBACK_PROBLEM_TABLE,(None,tg_id,idea,problem))
        self.connection.commit()
    def select_id_feedback_problem_table(self):
        self.cursor.execute(query.SELECT_ID_FEEDBACK_PROBLEM_TABLE)
        row=self.cursor.fetchall()
        return row
    def select_idea_problem_feedback_problem_table(self,tg_id):
        self.cursor.execute(query.SELECT_IDEA_PROBLEM_FEEDBACK_PROBLEM_TABLE,(tg_id,))
        row=self.cursor.fetchone()
        return row
    def select_balance_totalreferral_table(self,tg_id):
        self.cursor.execute(query.DOUBLE_SELECT_REFERRAL_USER_QUERY,(tg_id,))
        row=self.cursor.fetchone()
        return row
    def select_all_from_tl_users(self,tg_id):
        self.cursor.execute(query.SELECT_ALL_USER_TL_USERS,(tg_id,))
        row=self.cursor.fetchone()
        return row
    def update_tg_user_link(self,link,tg_id):
        self.cursor.execute(query.UPDATE_USER_TL_USERS_LINK,(link,tg_id))
        self.connection.commit()
    def select_all_from_tl_users_by_link(self,link):
        self.cursor.execute(query.SELECT_BY_LINK_TG_USERS,(link,))
        row=self.cursor.fetchone()
        return row
    def insert_referral_table(self,owner,referral):
        self.cursor.execute(query.INSERT_REFERRAL_TABLE,(None,owner,referral))
        self.connection.commit()
    def update_tg_user_balance(self,tg_id):
        self.cursor.execute(query.UPDATE_USER_TL_USERS_BALANCE,(tg_id,))
        self.connection.commit()
    def select_tg_id_user_table(self,tg_id):
        self.cursor.execute(query.SELECT_TG_ID_USER_TABLE,(tg_id,))
        row=self.cursor.fetchone()
        return row
    def select_referrals_referral_table(self,tg_id):
        self.cursor.execute(query.SELECT_REFERRALS_REFERRAL_TABLE,(tg_id,))
        row=self.cursor.fetchall()
        return row
    def insert_transactions(self,sender,taker,amount):
        self.cursor.execute(query.INSERT_TRANSACTIONS_TABLE,(None,sender,taker,amount))
        self.connection.commit()
    def update_tl_user_balance_minus(self,amount,tg_id):
        self.cursor.execute(query.UPDATE_USER_TL_USERS_BALANCE_MINUS,(amount,tg_id))
        self.connection.commit()
    def select_balance(self,tg):
        self.cursor.execute(query.SELECT_BALANCE_TL_USERS,(tg,))
        row=self.cursor.fetchone()
        return row
    def insert_check_table(self,sender,reason,amount,link):
        self.cursor.execute(query.INSERT_CHECK_TABLE,(None,sender,None,reason,amount,link,None))
        self.connection.commit()
    def select_check_table(self,link):
        self.cursor.execute(query.SELECT_CHECK_TABLE,(link,))
        row=self.cursor.fetchone()
        return row
    def update_check_table(self,taker,status,link):
        self.cursor.execute(query.UPDATE_CHECK_TABLE,(taker,status,link))
        self.connection.commit()
    def insert_eng_table(self,link):
        self.cursor.execute(query.INSERT_ENGLISH_LEVEL_LEARN_TABLE,(None,link))
        self.connection.commit()
    def insert_eng_table_b2(self,link):
        self.cursor.execute(query.INSERT_ENGLISH_LEVEL_LEARN_TABLE_B2,(None,link))
        self.connection.commit()
    def insert_eng_table_b1(self,link):
        self.cursor.execute(query.INSERT_ENGLISH_LEVEL_LEARN_TABLE_B1,(None,link))
        self.connection.commit()
    def insert_eng_table_a2(self,link):
        self.cursor.execute(query.INSERT_ENGLISH_LEVEL_LEARN_TABLE_A2,(None,link))
        self.connection.commit()
    def insert_eng_table_a1(self,link):
        self.cursor.execute(query.INSERT_ENGLISH_LEVEL_LEARN_TABLE_A1,(None,link))
        self.connection.commit()
    def insert_favo_eng_table(self,tg_id,link):
        self.cursor.execute(query.INSERT_FAVOURITE_ENGLISH_LEVEL_LEARN_TABLE,(None,tg_id,link))
        self.connection.commit()
    def select_id_fav_table(self,tg_id,link):
        self.cursor.execute(query.SELECT_FAV_ENG_LEVEL_TABLE,(tg_id,link))
        row=self.cursor.fetchone()
        return row
    def select_link_fav_table(self,tg_id):
        self.cursor.execute(query.SELECT_LINK_FAV_TABLE,(tg_id,))
        rows=self.cursor.fetchall()
        return rows
    def delete_fav_eng_table(self,link):
        self.cursor.execute(query.DELETE_FAV_ENG_LEVEL_TABLE,(link,))
        self.connection.commit()
    def select_tg_user_id_fav_table(self,link):
        self.cursor.execute(query.SELECT_USER_ID_FAV_TABLE,(link,))
        rows=self.cursor.fetchall()
        return rows
    def insert_admin_rating(self,admin,tg_id,rating):
        self.cursor.execute(query.INSERT_ADMIN_RATING_TABLE,(tg_id,admin,rating))
        self.connection.commit()
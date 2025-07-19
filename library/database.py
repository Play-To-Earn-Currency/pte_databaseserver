from datetime import datetime
from decimal import Decimal, getcontext
import mysql.connector

from library.config import Config

class Database:
    __connection = None
    __cursor = None

    @staticmethod
    def connect():
        if Database.__connection is None or not Database.__connection.is_connected():
            try:
                Database.__connection = mysql.connector.connect(
                    host=Config.get("host"),
                    user=Config.get("user"),
                    password=Config.get("password"),
                    database=Config.get("database")
                )
                Database.__cursor = Database.__connection.cursor()
                print("\033[32mConnection with database successfully\033[0m")
            except mysql.connector.Error as err:
                print(f"\033[31mCannot connect to database: {err}\033[0m")

    @staticmethod
    def get_connection():
        Database.connect()
        return Database.__connection

    @staticmethod
    def get_cursor():
        Database.connect()
        return Database.__connection.cursor()

    @staticmethod
    def close():
        if Database.__cursor is not None:
            Database.__cursor.close()
            Database.__cursor = None
        if Database.__connection is not None:
            Database.__connection.close()
            Database.__connection = None
            print("\033[33mDatabase connection closed\033[0m")

    #
    # Custom Methods ----------------------
    #
    
    @staticmethod
    def Increment(table: str, value: int, uniqueid: str):
        Database.connect()
        cursor = Database.get_cursor()

        query = f"UPDATE {table} SET value = value + %s WHERE uniqueid = %s"
        params = (value, uniqueid)

        try:
            cursor.execute(query, params)
            Database.__connection.commit()

            if cursor.rowcount == 0:
                print(f"\033[33m[{datetime.now().strftime('%S/%M/%H/%d/%m/%Y')}-DATABASE] No rows updated for uniqueid: {uniqueid}\033[0m")
                return False

            return True
        except mysql.connector.Error as err:
            print(f"\033[31m[{datetime.now().strftime('%S/%M/%H/%d/%m/%Y')}-DATABASE] Failed to increment: {err}\033[0m")
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def Register(table: str, uniqueid: str):
        Database.connect()
        cursor = Database.get_cursor()

        query = f"INSERT INTO {table} (uniqueid) VALUES (%s)"
        params = (uniqueid,)

        try:
            cursor.execute(query, params)
            Database.__connection.commit()
            return True
        except mysql.connector.IntegrityError as err:
            # Unecessary
            # print(f"\033[33m[{datetime.now().strftime('%S/%M/%H/%d/%m/%Y')}-DATABASE] Duplicate record (uniqueid: {uniqueid})\033[0m")
            return False
        except mysql.connector.Error as err:
            print(f"\033[31m[{datetime.now().strftime('%S/%M/%H/%d/%m/%Y')}-DATABASE] Error inserting new record: {err}\033[0m")
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def UpdateWalletAddress(table: str, wallet: str, uniqueid: str) -> bool:
        Database.connect()
        cursor = Database.get_cursor()

        query = f"UPDATE {table} SET walletaddress = %s WHERE uniqueid = %s"
        params = (wallet, uniqueid)

        try:
            cursor.execute(query, params)
            Database.__connection.commit()

            if cursor.rowcount == 0:
                print(f"\033[33m[{datetime.now().strftime('%S/%M/%H/%d/%m/%Y')}-DATABASE] No lines updated for uniqueid: {uniqueid}\033[0m")
                return False
            return True

        except mysql.connector.Error as err:
            print(f"\033[31m[{datetime.now().strftime('%S/%M/%H/%d/%m/%Y')}-DATABASE] Error updating wallet: {err}\033[0m")
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def GetWalletAddress(table: str, uniqueid: str) -> str | None:
        Database.connect()
        cursor = Database.get_cursor()

        query = f"SELECT walletaddress FROM {table} WHERE uniqueid = %s"
        params = (uniqueid,)

        try:
            cursor.execute(query, params)
            result = cursor.fetchone()

            if result:
                wallet = result[0]
                return wallet
            else:
                print(f"\033[33m[{datetime.now().strftime('%S/%M/%H/%d/%m/%Y')}-DATABASE] No wallet found for uniqueid: {uniqueid}\033[0m")
                return None
        except mysql.connector.Error as err:
            print(f"\033[31m[{datetime.now().strftime('%S/%M/%H/%d/%m/%Y')}-DATABASE] Error fetching wallet: {err}\033[0m")
            return None
        finally:
            cursor.close()
            
    @staticmethod
    def GetBalance(table: str, uniqueid: str) -> str | None:
        Database.connect()
        cursor = Database.get_cursor()

        query = f"SELECT value FROM {table} WHERE uniqueid = %s"
        params = (uniqueid,)

        try:
            cursor.execute(query, params)
            result = cursor.fetchone()

            if result:
                brute = Decimal(result[0])
                converted = brute / Decimal("1000000000000000000")
                return str(converted.quantize(Decimal("0.01")))
            else:
                print(f"\033[33m[{datetime.now().strftime('%S/%M/%H/%d/%m/%Y')}-DATABASE] No value found for uniqueid: {uniqueid}\033[0m")
                return None
        except mysql.connector.Error as err:
            print(f"\033[31m[{datetime.now().strftime('%S/%M/%H/%d/%m/%Y')}-DATABASE] Error fetching value: {err}\033[0m")
            return None
        finally:
            cursor.close()
            
    @staticmethod
    def GetBalanceRaw(table: str, uniqueid: str) -> str | None:
        Database.connect()
        cursor = Database.get_cursor()

        query = f"SELECT value FROM {table} WHERE uniqueid = %s"
        params = (uniqueid,)

        try:
            cursor.execute(query, params)
            result = cursor.fetchone()

            if result:
                balance = result[0]
                return balance
            else:
                print(f"\033[33m[{datetime.now().strftime('%S/%M/%H/%d/%m/%Y')}-DATABASE] No value found for uniqueid: {uniqueid}\033[0m")
                return None
        except mysql.connector.Error as err:
            print(f"\033[31m[{datetime.now().strftime('%S/%M/%H/%d/%m/%Y')}-DATABASE] Error fetching value: {err}\033[0m")
            return None
        finally:
            cursor.close()
    
    #
    # Custom Methods ----------------------
    #
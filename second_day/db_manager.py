class DBConnection:
    def __enter__(self):
        print("[DB] соединение открыто")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("[DB] соединение закрыто")
        return False
    
    def query(self, sql):
        if sql == "DROP":
            raise RuntimeError("Попытка выполнить опасный запрос DROP")
        print(f"Выполняется запрос {sql}")


print("--- Успешный запрос ---")
try:
    with DBConnection() as db:
        db.query("SELECT * FROM orders")
except Exception as e:
    print(f"Поймали ошибку: {e}")

print("\n--- Запрос с ошибкой ---")
try:
    with DBConnection() as db:
        db.query("DROP")
except RuntimeError as e:
    print(f"Поймали ошибку на уровне программы: {e}")
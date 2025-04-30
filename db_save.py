import json, sys
from pathlib import Path
from pymongo import MongoClient

MONGO_URI = "mongodb://192.168.10.205:27017"   # 인증이 필요하면 URI에 id:pw 포함
DB_NAME   = "iris_db"
COL_NAME  = "announcements"

def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_to_mongo(data):
    if not data:
        print("⚠️ 저장할 데이터가 없습니다.")
        return
    client = MongoClient(MONGO_URI)
    col    = client[DB_NAME][COL_NAME]
    r      = col.insert_many(data)
    print(f"✅ MongoDB 저장 완료: {len(r.inserted_ids):,} 건")

def main():
    if len(sys.argv) != 2:
        print("Usage: python db_save.py <json_file>")
        sys.exit(1)
    json_path = Path(sys.argv[1])
    save_to_mongo(load_json(json_path))

if __name__ == "__main__":
    main()
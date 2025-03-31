import os

def delete_migration_files():
    migration_files_to_delete = ['0001_initial.py', '0002_initial.py']
    current_dir = os.getcwd()
    
    for root, dirs, files in os.walk(current_dir):
        if 'migrations' in dirs:
            migration_path = os.path.join(root, 'migrations')
            for file_name in os.listdir(migration_path):
                if file_name in migration_files_to_delete:
                    file_path = os.path.join(migration_path, file_name)
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {str(e)}")

if __name__ == "__main__":
    delete_migration_files()

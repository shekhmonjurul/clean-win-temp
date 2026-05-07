import os
import shutil
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """যদি অ্যাডমিন না হয়, তবে অ্যাডমিন পারমিশন চেয়ে আবার রান করবে"""
    if is_admin():
        clean_folders()
    else:
        # উইন্ডোজকে বলবে অ্যাডমিন হিসেবে নতুন উইন্ডো খুলতে
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def clean_folders():
    # ফোল্ডার লিস্ট
    folders_to_clean = [
        os.environ.get('TEMP'),             # User Temp
        r'C:\Windows\Temp',                # System Temp
        r'C:\Windows\Prefetch'             # Prefetch Folder
    ]

    for folder_path in folders_to_clean:
        if not folder_path or not os.path.exists(folder_path):
            print(f"Skipping: {folder_path} (Not found)")
            continue

        print(f"\nCleaning: {folder_path}")
        print("-" * 40)

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"Deleted: {filename}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Deleted Folder: {filename}")
            except Exception:
                print(f"Skipped: {filename} (In use)")

    print("\n" + "=" * 40)
    print("Cleanup Process Finished!")
    input("Press Enter to exit...") # উইন্ডো যাতে সাথে সাথে বন্ধ না হয়ে যায়

if __name__ == "__main__":
    run_as_admin()
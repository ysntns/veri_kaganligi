import subprocess
import sys


def check_and_install_packages(requirements_file):
    try:
        # Mevcut kurulu paketleri listele
        installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode().split('\n')
        installed_packages = [pkg.split('==')[0] for pkg in installed_packages if '==' in pkg]

        # Gereksinim dosyasını oku
        with open(requirements_file, 'r') as file:
            required_packages = file.readlines()

        # Kurulu olmayan paketleri belirle
        packages_to_install = []
        for package in required_packages:
            package_name = package.split('==')[0].strip()
            if package_name not in installed_packages:
                packages_to_install.append(package.strip())

        # Eksik paketleri kur
        if packages_to_install:
            print(f"Kurulacak paketler: {packages_to_install}")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages_to_install)
        else:
            print("Tüm paketler zaten kurulu.")
    except Exception as e:
        print(f"Hata oluştu: {e}")


if __name__ == "__main__":
    check_and_install_packages('requirements.txt')

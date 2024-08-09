import os

def list_project_structure(root_dir, output_file='project_structure.txt'):
    """
    Proje dizin yapısını keşfeder ve sonuçları bir metin dosyasına yazar.

    Args:
        root_dir (str): Projenin kök dizin yolu.
        output_file (str): Çıktı dosyasının adı.
    """
    with open(output_file, 'w') as f:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Dizin yolu ve adını yazdırma
            f.write(f'Directory: {os.path.relpath(dirpath, root_dir)}\n')
            # Alt dizinleri yazdırma
            if dirnames:
                f.write('  Subdirectories:\n')
                for dirname in dirnames:
                    f.write(f'    - {dirname}\n')
            # Dosyaları yazdırma
            if filenames:
                f.write('  Files:\n')
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    file_size = os.path.getsize(file_path)
                    f.write(f'    - {filename} ({file_size} bytes)\n')
            f.write('\n')

    print(f"Proje yapısı '{output_file}' dosyasına yazıldı.")

# Kök dizin yolunu belirtin
root_directory = '/mnt/sda5/teknofest/turkce_nlp'  # Projenizin kök dizin yolu
list_project_structure(root_directory)

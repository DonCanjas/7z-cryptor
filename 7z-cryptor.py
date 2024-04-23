import os, sys, argparse, py7zr
from py7zr import SevenZipFile
from py7zr.exceptions import PasswordRequired

def decompress_7z(source_path, destination_path, password=None, subfolder=False, delete_original=False):
    if not subfolder:
        print("Subfolder option is disabled. Subfolders will not be processed.")

    # Iterate over files in the source directory
    for filename in os.listdir(source_path):
        file_path = os.path.join(source_path, filename)
        
        if os.path.isfile(file_path) and filename.endswith('.7z'):
            try:
                with SevenZipFile(file_path, mode='r', password=password) as z:
                    z.extractall(path=destination_path)
                    print(f"Extraction of {file_path} completed successfully.")
                
                if delete_original:  # Check if delete_original option is enabled
                    os.remove(file_path)
                    print(f"{filename} deleted successfully.")
            
            except PasswordRequired:
                print(f"Password is required for extracting {file_path}")
            
            except Exception as e:
                print(f"Error extracting {file_path}: {e}")

def compress_7z(source_path, destination_path, password=None, subfolder=False, delete_original=False, header_encryption=True, algorithm='COPY'):
    if not subfolder:
        print("Subfolder option is disabled. Subfolders will not be processed.")

    # Traverse the directory and compress files only
    for root, _, files in os.walk(source_path):
        if subfolder or root == source_path:  # Check if subfolder processing is enabled or if it's the root directory
            
            for file_name in files:
                file_path = os.path.join(root, file_name)
                
                try:
                    archive_name = os.path.splitext(file_path)[0] + ".7z"
                    
                    # Dictionary mapping compression algorithm names to filter IDs
                    filters_map = {
                        'COPY': py7zr.FILTER_COPY,
                        'LZMA2': py7zr.FILTER_LZMA2,
                        'LZMA': py7zr.FILTER_LZMA,
                        'Bzip2': py7zr.FILTER_BZIP2,
                        'Deflate': py7zr.FILTER_DEFLATE,
                        'PPMd': py7zr.FILTER_PPMD,
                        'ZStandard': py7zr.FILTER_ZSTD,
                        'Brotli': py7zr.FILTER_BROTLI
                    }

                    # Set compression filters based on the chosen algorithm
                    filters = [{"id": filters_map.get(algorithm)}, {'id': py7zr.FILTER_CRYPTO_AES256_SHA256}]

                    with SevenZipFile(archive_name, mode='w', password=password, filters=filters, header_encryption=header_encryption) as z:
                        rel_path = os.path.relpath(file_path, source_path)
                        z.write(file_path, arcname=rel_path)
                        print(f"Compression of {file_path} completed successfully.")
                    
                    if delete_original:
                        os.remove(file_path)
                        print(f"{file_name} deleted successfully.")
                    
                except Exception as e:
                    print(f"Error compressing {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog="7z-cryptor",
                    description="Encrypts/Decrypts 7z files within a set path. Repo: https://github.com/DonCanjas/7z-cryptor")

    # Add arguments
    parser.add_argument('-d', '--decompress', metavar='DECOMPRESS_INPUT', nargs='?', const=os.getcwd(), help='Path of 7z archives to decompress (default: current directory)') 
    parser.add_argument('-c', '--compress', metavar='COMPRESS_INPUT', nargs='?', const=os.getcwd(), help='Path of files to compress (default: current directory)')
    parser.add_argument('-o', '--output', metavar='OUTPUT', action='store', help='Path extracted/compressed files (default: same as input)')
    parser.add_argument('-p', '--password', metavar='PASSWORD', action='store', help='Password to encrypt/decrypt 7z files')
    parser.add_argument('-sub', '--subfolder', action='store_true', help='Process subfolders (default: disabled)')
    parser.add_argument('-del', '--delete', dest='delete_original', action='store_true', help='Delete original files after encryption/decryption (default: disabled)')
    parser.add_argument('-no-he', '--no-header-encryption', dest='header_encryption', action='store_false', help='Disable header encryption')
    parser.add_argument('-algo', '--algorithm', metavar='ALGORITHM', choices=['COPY', 'LZMA2', 'LZMA', 'Bzip2', 'Deflate', 'PPMd', 'ZStandard', 'Brotli'], default='COPY', 
    help='Compression algorithm (default: COPY). Available alorithms: COPY, LZMA2, LZMA, Bzip2, Deflate, PPMd (depend on pyppmd), ZStandard (depend on pyzstd), Brotli (depend on brotli, brotliCFFI)')
    args = parser.parse_args()

    if len(sys.argv)==1:
        print("")
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.compress:
        operation = 'compress'
        source_path = args.compress
    
    elif args.decompress:
        operation = 'decompress'
        source_path = args.decompress
    
    else:
        print("No job was defined.")
        sys.exit(1)

    destination_path = args.output if args.output else source_path
    password = args.password
    subfolder = args.subfolder
    delete = args.delete_original

    if operation == 'compress':
        if not password:
            print("Please specify a password for compression with -p or --password")
            sys.exit(1)
        
        compress_7z(source_path, destination_path, password, subfolder, delete, args.header_encryption, args.algorithm)
    
    elif operation == 'decompress':
        decompress_7z(source_path, destination_path, password, subfolder, delete)

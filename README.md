## 7z-cryptor
Encrypts/Decrytps 7z files within a set path.
  
## Dependencies
[py7zr](https://github.com/miurahr/py7zr) - 7z library  
[PyCryptodomex](https://www.pycryptodome.org/en/latest/index.html) - 7zAES encryption  
  
Optional:  
[PyZstd](https://pypi.org/project/pyzstd) - ZStandard compression  
[PyPPMd](https://pypi.org/project/pyppmd) - PPMd compression  
[Brotli](https://pypi.org/project/Brotli) - Brotli compression (CPython)  
[BrotliCFFI](https://pypi.org/project/brotlicffi) - Brotli compression (PyPy)  
  
## Usage
### Encrypt files
``python 7z-cryptor -c C:\Input\Path -o C:\Output\Path -p password``

### Decrypt files
``python 7z-cryptor -d C:\Input\Path -o C:\Output\Path -p password``
  
## Argument Explanation
*-d*, *--decompress*: Path to input files to be decompressed. If no path is set, defaults to current dir.  

*-c*, *--compress*: Path to input files to be compressed. If no path is set, defaults to current dir.  

*-o*, *--output*: Path to output files. If no path is set, defaults to same as --decompress/--compress.  

*-p*, *--password*: Password to encrypt/decrypt files. Required for compression.  

*-sub*, *--subfolder*: Process subfolders. If not set, it doesn't process subfolders.  

*-del*, *--delete*: Delete original files after compression/decompression. If not set, it doesn't delete any files.  

*-no-he*, *--no-header-encryption*: Disables header encryption. If not set, it does encrypt the headers.  

*-algo*, *--algorithm*:  Compression algorithm. Default: COPY. Available algorithms: ``COPY``, ``LZMA2``, ``LZMA``, ``Bzip2``, ``Deflate``, ``PPMd`` (depends on pyppmd), ``ZStandard`` (depends on pyzstd), ``Brotli`` (depends on brotli and brotliCFFI)  

*-f*, *--folder*: Folder mode for decompression. Default: none. ``Single`` creates a single folder to save all the extracted files. ``Multi`` will create a folder for every input files' output. 

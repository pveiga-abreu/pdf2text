# pdf2text

Interface to extracting text from PDFs documents

&nbsp;

## Instructions:

Install tesseract-ocr, only english is installed by default

```sh
sudo apt install tesseract-ocr
```

**Optional**: Install language packs

*Portuguese:*

```sh
sudo apt install tesseract-ocr-por
```

*German:*

```sh
sudo apt install tesseract-ocr-deu
```

And others...

&nbsp;

## Usage Example:

```python
pdf = PDF2Text('/path/to/pdf/file.pdf')
text = pdf.extract_text(lang='eng')

print(text)
```

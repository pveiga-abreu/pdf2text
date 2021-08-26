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

## Usage Examples:

```python
pdf = PDF2Text('/path/to/pdf/file.pdf')

"""
Select an area using coordinates -> (X, Y, W, H)
X, Y = Top Left Corner
W = Width
H = Height
"""
text = pdf.extract_text_from_location((260,2411,1099,79), lang='por')

print(text)
```

```python
pdf = PDF2Text('/path/to/pdf/file.pdf')

"""
Extract the text from the entire document
"""
text = pdf.extract_all_text()

print(text)
```

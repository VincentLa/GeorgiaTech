Assignment Details: http://cse6242.gatech.edu/fall-2017/hw1/

# Troubleshooting

If you get an error such as 
```
pandoc: pdflatex not found. pdflatex is needed for pdf output.
Error: pandoc document conversion failed with error 41
```

Need to do a couple things:
```
sudo apt-get install texlive-latex-base
```

and

install miktex (maybe actually only need to do this one)

```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D6BC243565B2087BC3F897C9277A7293F59E4889

echo "deb http://miktex.org/download/ubuntu xenial universe" | sudo tee /etc/apt/sources.list.d/miktex.list

sudo apt-get update

sudo apt-get install miktex
```
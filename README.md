# MDA-simulator-Django
A python simulator for MDA using Django.

## GETTING STARTED

1. load dependencies: You will need python3, Django (install via pip/pip3)
2. download code
3. make manage.py executable
4. migrate the database (python3 manage.py migrate)
5. start the server (python3 manage.py runserver)
6. server runs locally at  http://127.0.0.1:8000/
7. optional: let the project run on a webserver

## HOW TO USE

The navbar has 3 subcategories: input, results and howto (which contains this file)

### input

#### sequence

You can enter a sequence (in FASTA format) or upload a sequence file (FASTA).
If the file contains >1 sequence, only the first one will be used.

#### primers

Primers are also added in FASTA format, here you could input as many primers as you like.
The covid primers are a set of predefined primers.

If you typed in the sequence and/or primers manually via the textarea:
Before changing anything in the settings area, you should press the button "submit sequence and primers".
This will save those and also print a list of all primers (each being showed forward and reverse).

#### settings

In settings you could choose:
- number of produced products:
    All primer products are calculated and out of these products will be chosen at random until the number of produced products is reached.
    If ticking the "produce each possible primer product once"-checkbox, each primer product will be computed exactly once.
- global termination probability:
    The probability of a complete primer product to be terminated prematurely.
- local termination probability:
    If a primer product is terminated prematurely, this probability goes through the sequence. Wih each step there is this probability to stop the sequence at this position.
- chimerism model:
    It could be choosen which chimera model should be used. Explanations of each model see below.
- chimerism probability
    The probability that a produced sequence is chimeric.

After this you could press "start simulation" and are redirected to the result page. 

#### chimerism models
##### model A
Two random primer products (if you ticked "produce each possible primer product once" the first product is not random but the currently calculated product is used) are chosen.
A random number p between 0 and 1 is generated which determines the used fraction of the first product (p) and the second product (1-p).

##### model B
One random primer product (if you ticked "produce each possible primer product once" the product is not random but the currently calculated product is used) is chosen.
A random number p between 0 and 1 is generated which determines the used fraction of the first product (p).
Out of all primer products, the one which anneals to the fraction of the first product with the lowest number of mismatches is used as second primer product,
which makes up for the rest of the length of the resulting product.

##### model C
One random primer product (if you ticked "produce each possible primer product once" the product is not random but the currently calculated product is used) is chosen.
A random number p between 0 and 1 is generated which determines the used fraction of the first product (p).
All primer products get a probability to be chosen which is proportional to its distance to the first primer products beginning.
With this a second primer product is chosen, the nearer it is to the original product the more likely it is to be chosen.
The second product makes up for the rest of the length of the resulting product.

### results

The sequence is shown as a black line with the sequence length added at the right end.
Forward primers are shown above the line as a blue triangle, reverse primers are below and shown as red triangles.
The primer products which are produced under the given settings are printed below.
No zigzags show a product which is consisting of one primer product only.
From left to right there could be seen: the beginning position of the product, the forward primer (mismatches are dark and fat), the start and end position of the sequence in between the forward and reverse primer, the reverse primer (mismatches are dark and fat), the end position of the product.
A single zigzag line shows a prematurely terminated sequence.
A pair of double zigzags shows a chimerism with a break at the zigzags position.

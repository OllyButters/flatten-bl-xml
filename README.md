# flatten-bl-xml

Prototype flattening of XML from the scanned in books from the British Library. 

This was part of the JISC funded AMASED project (2015), see doi:10.6084/m9.figshare.1319503.v4 and doi:10.6084/m9.figshare.1480941.v6 for more info.

The idea here is to take an XML file representing a scanned in page (ALTO format?), parse it to then
build the relevant table structures in opal using its API, then to import all of the data into it. This is a proof of principle,
so needs some work to tidy up (proper passwords, better error handling etc) before it could be used in production,
but it worked on the sample of books we had.

See https://github.com/obiba/opal for info on opal.

Olly Butters
